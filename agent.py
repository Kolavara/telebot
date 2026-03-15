# ↓ PASTE HERE — very first lines of the file
import os
import schedule
import time
import threading
import asyncio
import requests
import json
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

# ---- PING SERVER (for Render/UptimeRobot) ----
class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Dwight is alive.")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
    def log_message(self, format, *args):
        pass

def run_ping_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), PingHandler)
    print(f"🌐 Ping server on port {port}")
    server.serve_forever()

Thread(target=run_ping_server, daemon=True).start()

# ---- LOAD ENV ----
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AUTH_TOKEN = os.getenv("TWITTER_AUTH_TOKEN")
CT0 = os.getenv("TWITTER_CT0")
YOUR_TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "123456789")

WATCHLIST_FILE = "watchlist.json"

DEFAULT_ACCOUNTS = [
    "demishassabis",
    "karpathy",
    "AnthropicAI",
]

def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        try:
            with open(WATCHLIST_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_ACCOUNTS.copy()

def save_watchlist(accounts):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(accounts, f)

TWITTER_ACCOUNTS = load_watchlist()
SUMMARY_TIME = "22:00"
client = Groq(api_key=GROQ_API_KEY)

ARYAN_PROMPT = """You are Aryan, an elite AI & Tech researcher.
You ONLY care about Artificial Intelligence, machine learning, LLMs, and tech.
If asked about anything outside AI & Tech, say:
'That is irrelevant to the mission. Ask me about AI and Tech.'
For research questions, provide:
- A sharp summary
- Key facts and recent developments
- Your strong, confident take
You are thorough, intense, and never stop until the answer is complete."""

def ask_groq(system, user_msg, max_tokens=1000):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg}
        ]
    )
    return response.choices[0].message.content

def get_twitter_session():
    session = requests.Session()
    cookies = {"auth_token": AUTH_TOKEN, "ct0": CT0}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "x-csrf-token": CT0 or "",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-active-user": "yes",
        "x-twitter-client-language": "en",
        "Referer": "https://x.com/",
        "Origin": "https://x.com",
    }
    session.headers.update(headers)
    session.cookies.update(cookies)
    return session

def get_user_id(session, username):
    url = "https://api.x.com/graphql/Yka-W8dz7RaEuQNkroPkYw/UserByScreenName"
    variables = {"screen_name": username, "withSafetyModeUserFields": True}
    features = {
        "hidden_profile_subscriptions_enabled": True,
        "rweb_tipjar_consumption_enabled": True,
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": False,
        "subscriptions_verification_info_is_identity_verified_enabled": True,
        "subscriptions_verification_info_verified_since_enabled": True,
        "highlights_tweets_tab_ui_enabled": True,
        "responsive_web_twitter_article_notes_tab_enabled": True,
        "subscriptions_feature_can_gift_premium": True,
        "creator_subscriptions_tweet_preview_api_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "responsive_web_graphql_timeline_navigation_enabled": True,
    }
    params = {"variables": json.dumps(variables), "features": json.dumps(features)}
    r = session.get(url, params=params, timeout=15)
    print(f"  UserByScreenName @{username}: HTTP {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        try:
            return data["data"]["user"]["result"]["rest_id"]
        except (KeyError, TypeError):
            return None
    return None

def get_user_tweets(session, user_id, count=5):
    url = "https://api.x.com/graphql/Y9WM4Id6UcGFE8Z-hbnixw/UserTweets"
    variables = {
        "userId": user_id,
        "count": count,
        "includePromotedContent": False,
        "withQuickPromoteEligibilityTweetFields": True,
        "withVoice": True,
        "withV2Timeline": True,
    }
    features = {
        "rweb_tipjar_consumption_enabled": True,
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": False,
        "creator_subscriptions_tweet_preview_api_enabled": True,
        "responsive_web_graphql_timeline_navigation_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "communities_web_enable_tweet_community_results_fetch": True,
        "c9s_tweet_anatomy_moderator_badge_enabled": True,
        "articles_preview_enabled": True,
        "responsive_web_edit_tweet_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "longform_notetweets_consumption_enabled": True,
        "responsive_web_twitter_article_tweet_consumption_enabled": True,
        "tweet_awards_web_tipping_enabled": False,
        "creator_subscriptions_quote_tweet_preview_enabled": False,
        "freedom_of_speech_not_reach_fetch_enabled": True,
        "standardized_nudges_misinfo": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
        "rweb_video_timestamps_enabled": True,
        "longform_notetweets_rich_text_read_enabled": True,
        "longform_notetweets_inline_media_enabled": True,
        "responsive_web_enhance_cards_enabled": False,
    }
    params = {"variables": json.dumps(variables), "features": json.dumps(features)}
    r = session.get(url, params=params, timeout=15)
    print(f"  UserTweets: HTTP {r.status_code}")
    if r.status_code != 200:
        return []
    tweets = []
    try:
        data = r.json()
        timeline = data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]
        for instruction in timeline:
            entries = instruction.get("entries", [])
            for entry in entries:
                try:
                    tweet_result = entry["content"]["itemContent"]["tweet_results"]["result"]
                    if "tweet" in tweet_result:
                        tweet_result = tweet_result["tweet"]
                    legacy = tweet_result.get("legacy", {})
                    text = legacy.get("full_text", "")
                    if text and not text.startswith("RT @"):
                        tweets.append(text)
                except (KeyError, TypeError):
                    continue
    except (KeyError, TypeError) as e:
        print(f"  Parse error: {e}")
    return tweets[:count]

def check_user_exists(username):
    session = get_twitter_session()
    return get_user_id(session, username) is not None

def fetch_tweets(username, count=5):
    try:
        if not AUTH_TOKEN or not CT0:
            return None
        session = get_twitter_session()
        user_id = get_user_id(session, username)
        if not user_id:
            return None
        tweets = get_user_tweets(session, user_id, count)
        if not tweets:
            return None
        result = f"@{username}:\n"
        for text in tweets:
            clean_text = text[:400].replace("*", "").replace("_", "")
            result += f"- {clean_text}\n"
        print(f"  ✅ Got {len(tweets)} tweets for @{username}")
        return result
    except Exception as e:
        print(f"❌ Error for @{username}: {e}")
        return None

def build_twitter_digest():
    all_tweets = ""
    valid_count = 0
    print(f"Building digest for {len(TWITTER_ACCOUNTS)} accounts...")
    for account in TWITTER_ACCOUNTS:
        print(f"Fetching @{account}...")
        tweet_data = fetch_tweets(account)
        if tweet_data:
            all_tweets += tweet_data + "\n"
            valid_count += 1
    if valid_count == 0:
        return "Could not fetch any tweets. Your Twitter cookies may have expired.\n\nTo fix:\n1. Open Chrome and go to x.com\n2. Press F12 > Application > Cookies > x.com\n3. Copy auth_token and ct0\n4. Update your environment variables\n5. Restart the bot"
    summary_prompt = "You are a sharp AI & Tech analyst. Summarize these tweets into a clean daily digest. Group by theme, highlight the most important insights, keep it concise and punchy."
    return ask_groq(summary_prompt, f"Today's tweets:\n\n{all_tweets}\n\nWrite the digest.")

# ---- HANDLE TELEGRAM MESSAGES ----
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global YOUR_TELEGRAM_CHAT_ID
    if not update.message:
        return
    if update.message.chat_id:
        chat_id_str = str(update.message.chat_id)
        if YOUR_TELEGRAM_CHAT_ID == "123456789":
            YOUR_TELEGRAM_CHAT_ID = chat_id_str
            print(f"🔒 Auto-saved Telegram Chat ID: {YOUR_TELEGRAM_CHAT_ID}")
    if not update.message.text:
        return
    user_msg = update.message.text.strip()
    print("✅ Message received:", user_msg)

    if user_msg.lower() == "/list":
        if not TWITTER_ACCOUNTS:
            await update.message.reply_text("📋 Your watchlist is currently empty.")
            return
        accounts = "\n".join([f"• @{a}" for a in TWITTER_ACCOUNTS])
        await update.message.reply_text(f"📋 Your watchlist:\n{accounts}")
        return

    if user_msg.lower().startswith("/add "):
        new_account = user_msg[5:].strip().replace("@", "")
        if new_account:
            await update.message.reply_text(f"🔍 Checking if @{new_account} exists...")
            loop = asyncio.get_event_loop()
            exists = await loop.run_in_executor(None, check_user_exists, new_account)
            if not exists:
                await update.message.reply_text(f"❌ Username @{new_account} doesn't exist on Twitter/X.")
                return
            if new_account.lower() not in [a.lower() for a in TWITTER_ACCOUNTS]:
                TWITTER_ACCOUNTS.append(new_account)
                save_watchlist(TWITTER_ACCOUNTS)
                await update.message.reply_text(f"✅ Added @{new_account} to the watchlist!")
            else:
                await update.message.reply_text(f"ℹ️ @{new_account} is already in the watchlist.")
        return

    if user_msg.lower().startswith("/remove "):
        remove_account = user_msg[8:].strip().replace("@", "")
        if remove_account:
            original_len = len(TWITTER_ACCOUNTS)
            TWITTER_ACCOUNTS[:] = [a for a in TWITTER_ACCOUNTS if a.lower() != remove_account.lower()]
            if len(TWITTER_ACCOUNTS) < original_len:
                save_watchlist(TWITTER_ACCOUNTS)
                await update.message.reply_text(f"🗑️ Removed @{remove_account} from the watchlist!")
            else:
                await update.message.reply_text(f"⚠️ Could not find @{remove_account} in the watchlist.")
        return

    if user_msg.lower() == "/digest":
        if not TWITTER_ACCOUNTS:
            await update.message.reply_text("⚠️ Your watchlist is empty! Add accounts using /add username")
            return
        await update.message.reply_text("⏳ Fetching tweets... give me a moment.")
        loop = asyncio.get_event_loop()
        digest = await loop.run_in_executor(None, build_twitter_digest)
        try:
            await update.message.reply_text(f"🤖 *AI & Tech Digest*\n\n{digest}", parse_mode='Markdown')
        except Exception:
            await update.message.reply_text(f"🤖 AI & Tech Digest\n\n{digest}")
        return

    if not user_msg.startswith("/"):
        reply = ask_groq(ARYAN_PROMPT, user_msg)
        await update.message.reply_text(reply)

# ---- SCHEDULER ----
def run_scheduler():
    def job():
        if YOUR_TELEGRAM_CHAT_ID == "123456789":
            print("⚠️ No chat ID saved yet — skipping digest")
            return
        print("📨 Sending 10pm digest...")
        digest = build_twitter_digest()
        def send_it():
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            data = {"chat_id": YOUR_TELEGRAM_CHAT_ID, "text": f"🤖 Daily AI & Tech Digest\n\n{digest}"}
            requests.post(url, json=data)
        threading.Thread(target=send_it).start()

    schedule.every().day.at(SUMMARY_TIME).do(job)
    while True:
        schedule.run_pending()
        time.sleep(30)

# ---- MAIN ----
def main():
    if not TELEGRAM_TOKEN or not GROQ_API_KEY:
        print("❌ Missing tokens!")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(CommandHandler("start", handle_message))

    t_sched = threading.Thread(target=run_scheduler, daemon=True)
    t_sched.start()

    print("🚀 Aryan is online!")
    print(f"📋 Watchlist: {', '.join(['@'+a for a in TWITTER_ACCOUNTS])}")
    print(f"🍪 Cookies: auth_token={'✅' if AUTH_TOKEN else '❌'}, ct0={'✅' if CT0 else '❌'}")
    app.run_polling()

if __name__ == "__main__":
    main()
