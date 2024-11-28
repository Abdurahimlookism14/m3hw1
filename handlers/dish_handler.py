from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Dispatcher

from database import Database

db = Database()


class DishForm(StatesGroup):
    waiting_for_dish_name = State()
    waiting_for_description = State()
    waiting_for_price = State()
    waiting_for_category = State()


async def cmd_add_dish(message: types.Message):
    await message.answer("Введите название блюда:")
    await DishForm.waiting_for_dish_name.set()


async def process_dish_name(message: types.Message, state: FSMContext):
    await state.update_data(dish_name=message.text)
    await message.answer("Введите описание блюда:")
    await DishForm.waiting_for_description.set()


async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите цену блюда:")
    await DishForm.waiting_for_price.set()


async def process_price(message: types.Message, state: FSMContext):

    await state.update_data(price=message.text)

    categories = db.execute("SELECT * FROM dish_categories").fetchall()

    if categories:
        keyboard = InlineKeyboardMarkup()
        for category in categories:
            keyboard.add(InlineKeyboardButton(category[1],
                                              callback_data=f"category_{category[0]}"))

        await message.answer("Выберите категорию блюда:", reply_markup=keyboard)
        await DishForm.waiting_for_category.set()
    else:
        await message.answer("Сначала добавьте категории.")
        await state.finish()


async def process_category_selection(callback_query:
types.CallbackQuery, state: FSMContext):
    category_id = callback_query.data.split('_')[1]
    await state.update_data(category_id=category_id)

    data = await state.get_data()
    db.execute("""
    INSERT INTO dishes (name, description, price, category_id)
    VALUES (?, ?, ?, ?)
    """, (data['dish_name'], data['description'], data['price'], category_id))

    await callback_query.message.answer(f"Блюдо '{data['dish_name']}' добавлено в базу данных.")
    await state.finish()


def register_handlers_dish(dp: Dispatcher):
    dp.register_message_handler(cmd_add_dish, Command("add_dish"))
    dp.register_message_handler(process_dish_name, state=DishForm.waiting_for_dish_name)
    dp.register_message_handler(process_description, state=DishForm.waiting_for_description)
    dp.register_message_handler(process_price, state=DishForm.waiting_for_price)
    dp.register_callback_query_handler(process_category_selection,
                                       lambda c: c.data.startswith('category_'),
                                state=DishForm.waiting_for_category)