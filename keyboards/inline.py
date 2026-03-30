from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def services_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✂️ Стрижка — 250грн", callback_data="service_1")],
        [InlineKeyboardButton(text="🪒 Гоління — 150грн", callback_data="service_2")],
        [InlineKeyboardButton(text="✂️🪒 Комплекс — 350грн", callback_data="service_3")],
    ])
    return keyboard

def confirm_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Підтвердити", callback_data="confirm"),
            InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel"),
        ]
    ])
    return keyboard