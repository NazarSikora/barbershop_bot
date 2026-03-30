from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.inline import services_keyboard, confirm_keyboard
from database.db import add_user, add_appointment, get_services

router = Router()

class BookingStates(StatesGroup):
    choosing_service = State()
    entering_name = State()
    entering_phone = State()
    entering_date = State()
    confirming = State()


@router.message(Command("book"))
async def cmd_book(message: Message, state: FSMContext):
    await state.set_state(BookingStates.choosing_service)
    await message.answer(
        "Обери послугу:",
        reply_markup=services_keyboard()
    )

@router.callback_query(
    BookingStates.choosing_service,
    F.data.startswith("service_")
)
async def process_service(callback: CallbackQuery, state: FSMContext):
    await state.update_data(service_id=callback.data.split("_")[1])
    await state.set_state(BookingStates.entering_name)
    await callback.message.answer("Введи своє ім'я:")
    await callback.answer()


@router.message(BookingStates.entering_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BookingStates.entering_phone)
    await message.answer("Введи номер телефону:\nНаприклад: +380991234567")


@router.message(BookingStates.entering_phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(BookingStates.entering_date)
    await message.answer("Введи дату запису:\nНаприклад: 25.01.2025")


@router.message(BookingStates.entering_date)
async def process_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)

    data = await state.get_data()

    await state.set_state(BookingStates.confirming)
    await message.answer(
        f"Перевір свій запис:\n\n"
        f"👤 Ім'я: {data['name']}\n"
        f"📞 Телефон: {data['phone']}\n"
        f"📅 Дата: {data['date']}\n\n"
        f"Все вірно?",
        reply_markup=confirm_keyboard()
    )



@router.callback_query(BookingStates.confirming, F.data == "confirm")
async def process_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()


    await add_user(
        telegram_id=callback.from_user.id,
        name=data['name'],
        phone=data['phone']
    )
    await add_appointment(
        user_id=callback.from_user.id,
        service_id=int(data['service_id']),
        date=data['date'],
        time="—"
    )


    await state.clear()

    await callback.message.answer(
        "✅ Запис підтверджено!\n\n"
        "Ми зв'яжемося з вами для підтвердження часу.\n"
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