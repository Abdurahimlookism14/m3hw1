from aiogram import Router, F, types
from aiogram.filters import Command
group_router = Router()
BAD_WORDS = ("дурак", "тупой")
@group_router.message(Command("ban", prefix="!"))
async def ban_user(message: types.Message):
    # print(message.text)
    # print(message.reply_to_message)
    if not message.reply_to_message:
        await message.answer("Надо сделать реплай на чье-то сообщение")
    else:
        id = message.reply_to_message.from_user.id
        await message.bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=id
        )
@group_router.message(F.text)
async def check_bad_words(message: types.Message):
    for word in BAD_WORDS:
        if word in message.text.lower():
            await message.answer("Нельзя так выражаться")
            await message.delete()
            break
@group_router.message(F.photo)
async def delete_images(message: types.Message):
    await message.delete()
    await message.answer("Нельзя картики и гифки")