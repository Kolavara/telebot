# 🤖 Aryan — AI & Tech Research Telegram Bot

A personal AI research assistant on Telegram, powered by **Groq's LLaMA 3.1**, that scrapes Twitter/X accounts and delivers a **daily AI & Tech digest at 10pm** — hosted 24/7 for free.

---

## ✨ Features

- 🧠 **AI Chatbot** — Ask anything about AI & Tech, powered by Groq LLaMA 3.1
- 🐦 **Twitter Scraper** — Fetches tweets from your watchlist using cookie-based GraphQL (no paid API needed)
- 📬 **Daily Digest** — Automatically sends a summarized digest every night at 10pm
- 📋 **Watchlist Management** — Add/remove Twitter accounts via Telegram commands
- 💾 **Persistent Storage** — Watchlist saved to `watchlist.json`, survives restarts
- ☁️ **Free Hosting** — Deployed on Render, kept alive by UptimeRobot

---

## 🔑 Tokens & Credentials You Need

You need **4 credentials** to run this bot. Here's exactly where to get each one:

### 1. `TELEGRAM_BOT_TOKEN`
- Open Telegram → search **@BotFather**
- Send `/newbot` → follow the steps → copy the token it gives you
- Looks like: `7283746152:AAFx2k3...`

### 2. `GROQ_API_KEY`
- Go to **[console.groq.com](https://console.groq.com)**
- Sign up free → go to **API Keys** → create a new key
- Looks like: `gsk_abc123...`

### 3. `TWITTER_AUTH_TOKEN`
- Open **Chrome** → go to **[x.com](https://x.com)** and log in
- Press **F12** → go to **Application** tab → **Cookies** → `https://x.com`
- Find the cookie named `auth_token` → copy its value
- Looks like: `a1b2c3d4e5f6...`
- ⚠️ **Keep this secret — it's equivalent to your Twitter password**

### 4. `TWITTER_CT0`
- Same place as above (F12 → Application → Cookies → x.com)
- Find the cookie named `ct0` → copy its value
- Looks like: `abc123def456...`
- ⚠️ **This expires periodically — update it if Twitter scraping stops working**

---

## 🚀 Hosting Guide — Render + UptimeRobot (100% Free, No Card)

### Step 1 — Push code to GitHub
1. Create a new **GitHub repository**
2. Upload these files:
   - `agent.py`
   - `requirements.txt`
   - `watchlist.json`

### Step 2 — Deploy on Render
1. Go to **[render.com](https://render.com)** → sign up with Google (no card needed)
2. Click **New** → **Web Service**
3. Connect your GitHub account → select your repo
4. Fill in the settings:

| Field | Value |
|-------|-------|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Run Command | `python agent.py` |
| Instance Type | Free |

5. Scroll down to **Environment Variables** → add all 4 credentials:

| Key | Value |
|-----|-------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token |
| `GROQ_API_KEY` | Your Groq API key |
| `TWITTER_AUTH_TOKEN` | Your Twitter auth_token cookie |
| `TWITTER_CT0` | Your Twitter ct0 cookie |

6. Click **Create Web Service** → wait for deployment
7. You should see: `Your service is live 🎉`

---

### Step 3 — Keep it alive with UptimeRobot
Render's free tier sleeps after 15 minutes of inactivity. UptimeRobot pings it every 5 minutes to keep it awake.

1. Go to **[uptimerobot.com](https://uptimerobot.com)** → sign up free (no card)
2. Click **+ Add New Monitor**
3. Fill in:

| Field | Value |
|-------|-------|
| Monitor Type | HTTP(s) |
| Friendly Name | Aryan Bot |
| URL | Your Render URL (e.g. `https://yourbot.onrender.com`) |
| Monitoring Interval | Every 5 minutes |

4. Click **Create Monitor** ✅

UptimeRobot will now ping your bot every 5 minutes and email you if it ever goes down.

---

## 📁 File Structure

```
├── agent.py          # Main bot code
├── requirements.txt  # Python dependencies
├── watchlist.json    # Tracked Twitter accounts (auto-managed)
└── README.md         # This file
```

---

## 📦 requirements.txt

```
groq
python-telegram-bot
requests
schedule
python-dotenv
```

---

## 💬 Telegram Commands

| Command | Description |
|---------|-------------|
| `/list` | Show all tracked Twitter accounts |
| `/add <username>` | Add a Twitter account to your watchlist |
| `/remove <username>` | Remove a Twitter account from your watchlist |
| `/digest` | Trigger an instant Twitter summary |
| Any text | Ask Aryan anything about AI & Tech |

---

## 🔄 Updating Twitter Cookies

Twitter cookies expire every few weeks. If the bot stops fetching tweets:

1. Open Chrome → go to **x.com** → log in
2. Press **F12** → **Application** → **Cookies** → `https://x.com`
3. Copy the new values of `auth_token` and `ct0`
4. Go to **Render dashboard** → **Environment** → update the values
5. Render will auto-restart with the new cookies ✅

---

## 🏗️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Groq](https://groq.com) | LLM inference (LLaMA 3.1 8B) |
| [python-telegram-bot](https://python-telegram-bot.org) | Telegram interface |
| Twitter GraphQL API | Tweet scraping via browser cookies |
| [Render](https://render.com) | Free 24/7 hosting |
| [UptimeRobot](https://uptimerobot.com) | Keep-alive monitoring |

---

## ⚠️ Security Notes

- **Never commit your `.env` file** or paste credentials anywhere publicly
- Your `TWITTER_AUTH_TOKEN` gives full access to your Twitter account — keep it private
- If credentials are ever exposed, rotate them immediately:
  - Twitter: Settings → Security → Sessions → Log out all
  - Groq & Telegram: Regenerate from their dashboards

---

## 📝 License

MIT — free to use and modify.
