import logging
from handlers.bot_config import bot, dp
from handlers.start import start_router
from handlers.picture import picture_router
from handlers.other_messages import echo_router
from handlers.opros_dialog import opros_router


async def main():
    dp.include_router(start_router)
    dp.include_router(picture_router)
    dp.include_router(opros_router)
    # в самом конце
    dp.include_router(echo_router)

    # запуск бота:
    await dp.start_polling(bot)


import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import dotenv_values





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
    names = ("shelly", "chico", "wartander", "brawlstars", "sergay")
    random_name = random.choice(names)
    await message.answer(f"Случайное имя: {random_name}")

@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(message.text)

async def main():

    await dp.start_polling(bot)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())