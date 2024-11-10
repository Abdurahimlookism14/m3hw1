from aiogram import Router, types

echo_router = Router()

@echo_router.message()
async def echo_handler(message: types.Message):
    # обработчик всех сообщений
    # await message.answer(message.text)
    await message.reply("Я вас не понимаю!")