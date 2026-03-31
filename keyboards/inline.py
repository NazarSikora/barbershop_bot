from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def services_keyboard(services: list):
    buttons = []
    for service in services:
        service_id, name, price = service
        buttons.append([
            InlineKeyboardButton(
                text=f"{name} — {price}грн",
                callback_data=f"service_{service_id}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def masters_keyboard(masters: list):
    buttons = []
    for master in masters:
        master_id, name, specialization = master
        buttons.append([
            InlineKeyboardButton(
                text=f"{name} | {specialization}",
                callback_data=f"master_{master_id}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def slots_keyboard(slots: list):
    buttons = []
    row = []
    for i, slot in enumerate(slots):
        row.append(
            InlineKeyboardButton(
                text=slot,
                callback_data=f"slot_{slot}"
            )
        )
        # По три кнопки в рядку
        if len(row) == 3:
            buttons.append(row)
            row = []

    # Залишок якщо кнопок не кратно трьом
    if row:
        buttons.append(row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def confirm_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Підтвердити",
                callback_data="confirm"
            ),
            InlineKeyboardButton(
                text="❌ Скасувати",
                callback_data="cancel"
            ),
        ]
    ])
    return keyboard