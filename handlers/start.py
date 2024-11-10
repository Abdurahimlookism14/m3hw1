from aiogram import Router, F, types
from aiogram.filters import Command

start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    msg = f"Привет, {name}"
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Наш инстаргам",
                    url="https://instagram.com/geeks"
                ),
                types.InlineKeyboardButton(
                    text="Наш сайт",
                    url="https://geeks.kg"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="О Нас",
                    callback_data="about"
                )
            ]
        ]
    )
    await message.answer(msg, reply_markup=kb)
    # await bot.send_message(
    #     chat_id=message.from_user.id,
    #     text=msg,
    # )

# @start_router.callback_query(lambda cb: cb.data == "about")
@start_router.callback_query(F.data == "about")
async def about_us(callback: types.CallbackQuery):
    await callback.message.answer("О нас")





