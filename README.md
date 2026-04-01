# 💈 Barbershop Telegram Bot

A Telegram bot for automated client booking at a barbershop.
Eliminates the need for an administrator to manage appointments.

## Features
- 6-step booking flow via inline keyboards
- Service selection with prices
- Master selection by specialization
- Real-time slot availability — no double bookings
- Working hours: 10:00–19:00, 1-hour slots
- SQLite database for storing all appointments
- Admin panel with booking history (/admin)
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

Create `.env` file:
```
BOT_TOKEN=your_bot_token
ADMIN_ID=your_telegram_id
```

Run:
```bash
python3 bot.py
```
