from aiogram import Router, types
from aiogram.filters import Command


picture_router = Router()

@picture_router.message(Command("picture"))
async def picture_handler(message: types.Message):
    photo = types.FSInputFile("images/character.jpg")
    await message.answer_photo(
        photo=photo,
        caption="good mc"
    )
    await message.reply_photo(
        photo=photo,
        caption="good mc"
    )