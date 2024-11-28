from aiogram import Bot, Dispatcher
from dotenv import dotenv_values

token = dotenv_values(".env")["7921028291:AAG0bZXmTxwFl4NH_MIkwzhRJmOJk3tFPlA"]
bot = Bot(token=token)
dp = Dispatcher()
