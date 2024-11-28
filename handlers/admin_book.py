from aiogram import F, Router, types
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from bot_config import database


admin_book_router = Router()
admin_book_router.message.filter(
    F.from_user.id == 243154734
)

class Book(StatesGroup):
    name = State()
    author = State()
    price = State()
    genre = State()

class Genre(StatesGroup):
    name = State()
@admin_book_router.message(Command("newgenre"))
async def create_new_genre(message: types.Message, state: FSMContext):
    await state.set_state(Genre.name)
    await message.answer("Задайте название жанра:")
@admin_book_router.message(Genre.name)
async def process_name(message: types.Message, state: FSMContext):
    genre = message.text
    database.execute(
        query="""
            INSERT INTO genres(name) VALUES (?)
        """,
        params=(genre,)
    )
    await message.answer("Жанр добавлен в БД")
    await state.clear()

@admin_book_router.message(Command("newbook"), default_state)
async def create_newbook(message: types.Message, state: FSMContext):
    print(message.from_user.id)
    await state.set_state(Book.name)
    await message.answer("Задайте название книги:")

@admin_book_router.message(Book.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Book.author)
    await message.answer("Задайте автора книги:")

@admin_book_router.message(Book.author)
async def process_author(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    await state.set_state(Book.price)
    await message.answer("Задайте цену книги:")

@admin_book_router.message(Book.price)
async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    all_genres = database.fetch("SELECT * FROM genres")
    if not all_genres:
        await message.answer("Нет ни одного жанра")
        state.clear()
        return
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=genre["name"]) for genre in all_genres]
        ]
    )
    await state.set_state(Book.genre)
    await message.answer("Задайте жанр книги:")
    await message.answer("Задайте жанр книги:", reply_markup=kb)

@admin_book_router.message(Book.genre)
async def process_genre(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)
    print(message.text)
    genre_id = database.fetch(
        query="SELECT id FROM genres WHERE name = ?", # [{'id': 3}] []
        params=(message.text,)
    )
    if not genre_id:
        await message.answer("Вы напечатали неуществующий в базе данных жанр")
        return
    await state.update_data(genre=genre_id[0]["id"])
    data = await state.get_data()
    database.execute(
        query="""
            INSERT INTO books(name, author, price, genre)
            INSERT INTO books(name, author, price, genre_id)
            VALUES (?, ?, ?, ?)
        """,
        params=(
            data["name"],
            data["author"],
            data["price"],
            data["genre"]
        )
    )
    await message.answer("Книга добавлена")
    kb = types.ReplyKeyboardRemove()
    await message.answer("Книга добавлена", reply_markup=kb)