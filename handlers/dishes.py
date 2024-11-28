from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Command
from bot_config import Database

dishes_router = Router()
db = Database()



class Dishes(StatesGroup):
    name = State()
    description = State()
    price = State()


admin_keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton("Добавить блюдо")]],
    resize_keyboard=True
)


@dishes_router.message(Command("add_dish"))
async def start_dish_addition(message: types.Message):
    if message.from_user.id == message.from_user.id:
        await message.answer("Введите название блюда:")
        await Dishes.name.set()
    else:
        await message.answer("У вас нет прав на добавление блюда.")


@dishes_router.message(Dishes.name)
async def get_dish_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание блюда:")
    await Dishes.description.set()


@dishes_router.message(Dishes.description)
async def get_dish_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите цену блюда:")
    await Dishes.price.set()


@dishes_router.message(Dishes.price)
async def get_dish_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(price=price)

        data = await state.get_data()

        db.execute('''
        INSERT INTO dishes (name, description, price)
        VALUES (?, ?, ?)
        ''', (data['name'], data['description'], data['price']))

        await message.answer(
            f"Блюдо {data['name']} добавлено в меню!\nОписание: {data['description']}\nЦена: {data['price']}₽")
        await state.clear()
    except ValueError:
        await message.answer("Цена должна быть числом. Пожалуйста, введите корректное значение.")
        await Dishes.price.set()


@dishes_router.message(Command("show_dishes"))
async def show_dishes(message: types.Message):
    if message.from_user.id == message.from_user.id:
        dishes = db.execute("SELECT * FROM dishes").fetchall()
        if dishes:
            dish_list = "\n".join([f"{dish[1]}: {dish[2]} - {dish[3]}₽" for dish in dishes])
            await message.answer(f"Меню:\n{dish_list}")
        else:
            await message.answer("Меню пусто.")
    else:
        await message.answer("У вас нет прав на просмотр меню.")