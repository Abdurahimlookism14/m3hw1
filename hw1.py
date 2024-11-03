import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import dotenv_values

token = dotenv_values(".env")["7921028291:AAG0bZXmTxwFl4NH_MIkwzhRJmOJk3tFPlA"]
bot = Bot(token=token)
dp = Dispatcher()

unique_users = set()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    user_id = message.from_user.id

    unique_users.add(user_id)
    user_count = len(unique_users)

    msg = f"Привет, {name}, наш бот обслуживает уже {user_count} пользователя."
    await message.answer(msg)


@dp.message(Command("myinfo"))
async def myinfo_handler(message: types.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username or "Не указан"

    msg = f"Ваш id: {user_id}\nВаше имя: {first_name}\nВаш юзернейм: {username}"
    await message.answer(msg)

@dp.message(Command("random"))
async def random_name_handler(message: types.Message):
    names = ("Игорь", "Анастасия", "Владимир", "Екатерина", "Сергей")
    random_name = random.choice(names)
    await message.answer(f"Случайное имя: {random_name}")

@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(message.text)

async def main():

    await dp.start_polling(bot)

if __name__ == 'main':
    asyncio.run(main())
