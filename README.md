# 💈 Barbershop Telegram Bot

A Telegram bot for booking appointments at a barbershop.

## Features
- Booking via FSM (5 steps)
- Service selection via inline keyboards
- Appointments stored in SQLite
- Admin panel (/admin)
- Instant admin notifications on new bookings

## Stack
Python · aiogram 3 · SQLite · aiosqlite · python-dotenv

## Setup
```bash
git clone https://github.com/NazarSikora/barbershop-bot
cd barbershop-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the root directory:
```
BOT_TOKEN=your_bot_token
ADMIN_ID=your_telegram_id
```

Run the bot:
```bash
python3 bot.py
```