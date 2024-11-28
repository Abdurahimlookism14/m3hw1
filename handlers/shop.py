from aiogram import F, Router, types
from aiogram.filters import Command

from bot_config import database
from pprint import pprint

shop_router = Router()


@shop_router.message(Command("books"))
async def show_all_books(message: types.Message):
    all_books = database.fetch(
        query="SELECT * FROM books"
    all_genres = database.fetch("SELECT * FROM genres")
    if not all_genres:
        await message.answer("Нет ни одного жанра")
        return
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=genre["name"]) for genre in all_genres]
        ]
    )
    await message.answer("Выберите жанр литературы", reply_markup=kb)
def check_genre_filter(message: types.Message):
    print("inside genre filter")
    all_genres = database.fetch(
        query="SELECT name FROM genres WHERE name = ?", #
        params=(message.text,)
    ) # [{'name': 'Приключение'}]
    if all_genres:
        return True
    return False
@shop_router.message(check_genre_filter)
async def show_books_by_genre(message: types.Message):
    all_books = database.fetch(
        query="SELECT * FROM books JOIN genres ON books.genre_id = genres.id WHERE genres.name = ?",
        params=(message.text, )
    )
    # [{'author': 'Дж К Роулинг',
    # 'genre_id': 3,
    # 'id': 1,
    # 'name': 'Гарри поттер',
    # 'price': 2133}]
    # []
    pprint(all_books)
    if not all_books:
        await message.answer("Извините, книг данного жанра нет")
        return
    await message.answer("Книги из нашего каталога:")
    for book in all_books:
        await message.answer(f"Название: {book['name']}\nЦена: {book['price']}")