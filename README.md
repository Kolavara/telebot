🤖 Aryan — AI & Tech Research Telegram Bot
A personal AI research assistant on Telegram, powered by Groq's LLaMA 3.1, that scrapes Twitter/X accounts and delivers a daily AI & Tech digest at 10pm — hosted 24/7 for free.

✨ Features

🧠 AI Chatbot — Ask anything about AI & Tech, powered by Groq LLaMA 3.1
🐦 Twitter Scraper — Fetches tweets from your watchlist using cookie-based GraphQL (no paid API needed)
📬 Daily Digest — Automatically sends a summarized digest every night at 10pm
📋 Watchlist Management — Add/remove Twitter accounts via Telegram commands
💾 Persistent Storage — Watchlist saved to watchlist.json, survives restarts
☁️ Free Hosting — Deployed on Render, kept alive by UptimeRobot


🔑 Tokens & Credentials You Need
You need 4 credentials to run this bot. Here's exactly where to get each one:
1. TELEGRAM_BOT_TOKEN

Open Telegram → search @BotFather
Send /newbot → follow the steps → copy the token it gives you
Looks like: 7283746152:AAFx2k3...

2. GROQ_API_KEY

Go to console.groq.com
Sign up free → go to API Keys → create a new key
Looks like: gsk_abc123...

3. TWITTER_AUTH_TOKEN

Open Chrome → go to x.com and log in
Press F12 → go to Application tab → Cookies → https://x.com
Find the cookie named auth_token → copy its value
Looks like: a1b2c3d4e5f6...
⚠️ Keep this secret — it's equivalent to your Twitter password

4. TWITTER_CT0

Same place as above (F12 → Application → Cookies → x.com)
Find the cookie named ct0 → copy its value
Looks like: abc123def456...
⚠️ This expires periodically — update it if Twitter scraping stops working


🚀 Hosting Guide — Render + UptimeRobot (100% Free, No Card)
Step 1 — Push code to GitHub

Create a new GitHub repository
Upload these files:

agent.py
requirements.txt
watchlist.json



Step 2 — Deploy on Render

Go to render.com → sign up with Google (no card needed)
Click New → Web Service
Connect your GitHub account → select your repo
Fill in the settings:

FieldValueRuntimePython 3Build Commandpip install -r requirements.txtRun Commandpython agent.pyInstance TypeFree

Scroll down to Environment Variables → add all 4 credentials:

KeyValueTELEGRAM_BOT_TOKENYour Telegram bot tokenGROQ_API_KEYYour Groq API keyTWITTER_AUTH_TOKENYour Twitter auth_token cookieTWITTER_CT0Your Twitter ct0 cookie

Click Create Web Service → wait for deployment
You should see: Your service is live 🎉


Step 3 — Keep it alive with UptimeRobot
Render's free tier sleeps after 15 minutes of inactivity. UptimeRobot pings it every 5 minutes to keep it awake.

Go to uptimerobot.com → sign up free (no card)
Click + Add New Monitor
Fill in:

FieldValueMonitor TypeHTTP(s)Friendly NameAryan BotURLYour Render URL (e.g. https://yourbot.onrender.com)Monitoring IntervalEvery 5 minutes

Click Create Monitor ✅

UptimeRobot will now ping your bot every 5 minutes and email you if it ever goes down.

📁 File Structure
├── agent.py          # Main bot code
├── requirements.txt  # Python dependencies
├── watchlist.json    # Tracked Twitter accounts (auto-managed)
└── README.md         # This file

📦 requirements.txt
groq
python-telegram-bot
requests
schedule
python-dotenv

💬 Telegram Commands
CommandDescription/listShow all tracked Twitter accounts/add <username>Add a Twitter account to your watchlist/remove <username>Remove a Twitter account from your watchlist/digestTrigger an instant Twitter summaryAny textAsk Aryan anything about AI & Tech

🔄 Updating Twitter Cookies
Twitter cookies expire every few weeks. If the bot stops fetching tweets:

Open Chrome → go to x.com → log in
Press F12 → Application → Cookies → https://x.com
Copy the new values of auth_token and ct0
Go to Render dashboard → Environment → update the values
Render will auto-restart with the new cookies ✅


🏗️ Tech Stack
ToolPurposeGroqLLM inference (LLaMA 3.1 8B)python-telegram-botTelegram interfaceTwitter GraphQL APITweet scraping via browser cookiesRenderFree 24/7 hostingUptimeRobotKeep-alive monitoring

⚠️ Security Notes

Never commit your .env file or paste credentials anywhere publicly
Your TWITTER_AUTH_TOKEN gives full access to your Twitter account — keep it private
If credentials are ever exposed, rotate them immediately:

Twitter: Settings → Security → Sessions → Log out all
Groq & Telegram: Regenerate from their dashboards




📝 License
MIT — free to use and modify.
