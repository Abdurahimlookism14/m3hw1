from aiogram import Bot, Dispatcher
from dotenv import dotenv_values

from database.database import Database
token = dotenv_values(".env")["AAG0bZXmTxwFl4NH_MIkwzhRJmOJk3tFPlA"]
bot = Bot(token=token)
dp = Dispatcher()
dp = Dispatcher()
database = Database("database.sqlite")










