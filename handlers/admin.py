from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import aiosqlite

from config import BOT_TOKEN, ADMIN_ID
from database.db import DB_PATH

router = Router()

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    # Перевіряємо чи це адмін
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У тебе немає доступу до цієї команди.")
        return

    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
            SELECT 
                users.name,
                users.phone,
                services.name,
                appointments.date,
                appointments.status
            FROM appointments
            JOIN users ON appointments.user_id = users.telegram_id
            JOIN services ON appointments.service_id = services.id
            ORDER BY appointments.id DESC
            LIMIT 10
        """) as cursor:
            rows = await cursor.fetchall()

    if not rows:
        await message.answer("📭 Записів поки немає.")
        return

    text = "📋 Останні записи:\n\n"
    for row in rows:
        name, phone, service, date, status = row
        text += (
            f"👤 {name}\n"
            f"📞 {phone}\n"
            f"✂️ {service}\n"
            f"📅 {date}\n"
            f"🔘 Статус: {status}\n"
            f"──────────────\n"
        )

    await message.answer(text)