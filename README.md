# Discord Wrapped 

A Discord bot that tracks server activity and generates monthly recaps — like Spotify Wrapped, but for your server.

## Features (in progress)

- [x] Monthly leaderboard (messages, words sent)
- [x] Most used words per user and server-wide
- [x] Voice channel time tracking
- [ ] Most active days and hours
- [ ] Auto-post recap on the 1st of each month
- [ ] Moderation tools (ban, kick, warn, mute)

## Tech Stack

- **Bot** — [discord.py](https://discordpy.readthedocs.io/)
- **API** — [FastAPI](https://fastapi.tiangolo.com/)
- **Database** — SQLite (via aiosqlite)

## Project Structure

```
discord-wrapped/
├── bot/
│   ├── cogs/
│   │   ├── moderation.py   # Ban, kick, warn, mute
│   │   ├── tracker.py      # Message & voice event logging
│   │   └── recap.py        # Recap commands & auto-post
│   └── main.py             # Bot entrypoint
├── api/
│   ├── routes/
│   │   ├── stats.py        # Leaderboard & word count endpoints
│   │   └── recap.py        # Monthly summary endpoint
│   └── main.py             # FastAPI entrypoint
├── database/
│   └── db.py               # Database setup & queries
├── .env.example            # Environment variable template
├── requirements.txt
└── README.md
```

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/discord-wrapped.git
cd discord-wrapped
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your Discord bot token
```

### 5. Run the bot
```bash
python bot/main.py
```

## Getting a Discord Bot Token

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Click **New Application** → give it a name
3. Go to **Bot** → click **Add Bot**
4. Copy the token → paste into your `.env` file
5. Under **Privileged Gateway Intents**, enable:
   - Server Members Intent
   - Message Content Intent


## License

MIT
