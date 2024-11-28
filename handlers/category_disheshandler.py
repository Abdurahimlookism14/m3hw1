from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher

from database import Database  

db = Database()


class CategoryForm(StatesGroup):
    waiting_for_category_name = State()


async def cmd_add_category(message: types.Message):
    await message.answer("Введите название категории (например, 'Супы', 'Салаты'):")
    await CategoryForm.waiting_for_category_name.set()


async def process_category_name(message: types.Message, state: FSMContext):
    category_name = message.text
    db.execute("INSERT INTO dish_categories (category_name) VALUES (?)", (category_name,))

    await message.answer(f"Категория '{category_name}' добавлена в базу данных.")

    await state.finish()


def register_handlers_category(dp: Dispatcher):
    dp.register_message_handler(cmd_add_category, Command("add_category"))
    dp.register_message_handler(process_category_name,
    state=CategoryForm.waiting_for_category_name)