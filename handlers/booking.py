from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import BOT_TOKEN, ADMIN_ID
from keyboards.inline import (
    services_keyboard,
    masters_keyboard,
    slots_keyboard,
    confirm_keyboard
)
from database.db import (
    add_user,
    add_appointment,
    get_services,
    get_masters,
    get_available_slots
)

router = Router()


class BookingStates(StatesGroup):
    choosing_service = State()
    choosing_master = State()
    entering_date = State()
    choosing_slot = State()
    entering_phone = State()
    confirming = State()


@router.message(Command("book"))
async def cmd_book(message: Message, state: FSMContext):
    services = await get_services()
    await state.set_state(BookingStates.choosing_service)
    await message.answer(
        "Обери послугу:",
        reply_markup=services_keyboard(services)
    )


@router.callback_query(
    BookingStates.choosing_service,
    F.data.startswith("service_")
)
async def process_service(callback: CallbackQuery, state: FSMContext):
    service_id = callback.data.split("_")[1]
    await state.update_data(service_id=service_id)

    masters = await get_masters()
    await state.set_state(BookingStates.choosing_master)
    await callback.message.answer(
        "Обери майстра:",
        reply_markup=masters_keyboard(masters)
    )
    await callback.answer()


@router.callback_query(
    BookingStates.choosing_master,
    F.data.startswith("master_")
)
async def process_master(callback: CallbackQuery, state: FSMContext):
    master_id = callback.data.split("_")[1]
    await state.update_data(master_id=master_id)

    await state.set_state(BookingStates.entering_date)
    await callback.message.answer(
        "Введи дату запису:\n"
        "Наприклад: 25.04.2026"
    )
    await callback.answer()


@router.message(BookingStates.entering_date)
async def process_date(message: Message, state: FSMContext):
    date = message.text
    data = await state.get_data()
    master_id = int(data['master_id'])

    slots = await get_available_slots(master_id, date)

    if not slots:
        await message.answer(
            "😔 На цю дату немає вільних годин.\n"
            "Спробуй іншу дату:"
        )
        return

    await state.update_data(date=date)
    await state.set_state(BookingStates.choosing_slot)
    await message.answer(
        f"Вільні години на {date}:",
        reply_markup=slots_keyboard(slots)
    )


@router.callback_query(
    BookingStates.choosing_slot,
    F.data.startswith("slot_")
)
async def process_slot(callback: CallbackQuery, state: FSMContext):
    time = callback.data.split("slot_")[1]
    await state.update_data(time=time)

    await state.set_state(BookingStates.entering_phone)
    await callback.message.answer(
        "Введи номер телефону:\n"
        "Наприклад: +380991234567"
    )
    await callback.answer()


@router.message(BookingStates.entering_phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()

    await state.set_state(BookingStates.confirming)
    await message.answer(
        f"Перевір свій запис:\n\n"
        f"📞 Телефон: {data['phone']}\n"
        f"📅 Дата: {data['date']}\n"
        f"🕐 Час: {data['time']}\n\n"
        f"Все вірно?",
        reply_markup=confirm_keyboard()
    )


@router.callback_query(BookingStates.confirming, F.data == "confirm")
async def process_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await add_user(
        telegram_id=callback.from_user.id,
        name=callback.from_user.full_name,
        phone=data['phone']
    )
    await add_appointment(
        user_id=callback.from_user.id,
        master_id=int(data['master_id']),
        service_id=int(data['service_id']),
        date=data['date'],
        time=data['time']
    )

    await state.clear()

    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(
        ADMIN_ID,
        f"🔔 Новий запис!\n\n"
        f"👤 {callback.from_user.full_name}\n"
        f"📞 {data['phone']}\n"
        f"📅 {data['date']}\n"
        f"🕐 {data['time']}"
    )

    await callback.message.answer(
        "✅ Запис підтверджено!\n\n"
        "Ми зв'яжемося з вами для підтвердження.\n"
        "Дякуємо що обрали нас! 💈"
    )
    await callback.answer()


@router.callback_query(BookingStates.confirming, F.data == "cancel")
async def process_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        "❌ Запис скасовано.\n"
        "Якщо захочеш записатися — натисни /book"
    )
    await callback.answer()