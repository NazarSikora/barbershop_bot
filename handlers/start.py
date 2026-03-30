from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database.db import add_user

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await add_user(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name,
        phone="невідомо"
    )
    await message.answer(
        f"Привіт, {message.from_user.full_name}! 👋\n\n"
        "Я бот барбершопу. Ось що я вмію:\n"
        "/start — почати спочатку\n"
        "/help — допомога\n"
        "/book — записатися до майстра"
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Як записатися:\n\n"
        "1. Натисни /book\n"
        "2. Обери послугу\n"
        "3. Вкажи дату та час\n"
        "4. Підтверди запис\n\n"
        "Якщо виникли питання — звертайся!"
    )