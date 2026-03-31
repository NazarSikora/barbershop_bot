from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from database.db import add_user

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await add_user(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name,
        phone="невідомо"
    )
    await message.answer(
        f"Вітаємо, {message.from_user.full_name}! 💈\n\n"
        "Ласкаво просимо до <b>Barbershop Classic</b> — "
        "місця де чоловіки стають ще кращими.\n\n"
        "✂️ Професійні майстри\n"
        "🕐 Працюємо з 10:00 до 19:00\n"
        "📍 Львів, вул. Шевченка 1\n\n"
        "Щоб записатися — натисни /book\n"
        "Допомога — /help",
        parse_mode="HTML"
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Як записатися:\n\n"
        "1. Натисни /book\n"
        "2. Обери послугу\n"
        "3. Обери майстра\n"
        "4. Вкажи дату\n"
        "5. Обери вільний час\n"
        "6. Підтверди запис\n\n"
        "Якщо виникли питання — звертайся!"
    )