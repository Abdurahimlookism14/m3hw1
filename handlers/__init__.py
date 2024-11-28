from aiogram import Router, F
from .start import start_router
from .shop import shop_router
from .picture import picture_router
from .other_messages import echo_router
from .opros_dialog import opros_router
from .admin_book import admin_book_router

from aiogram import Dispatcher
from .category_handler import register_handlers_category
from .dish_handler import register_handlers_dish

def register_all_handlers(dp: Dispatcher):
    register_handlers_category(dp)
    register_handlers_dish(dp)

private_router = Router()

private_router.include_router(start_router)
private_router.include_router(picture_router)
private_router.include_router(opros_router)
private_router.include_router(admin_book_router)
private_router.include_router(shop_router)

private_router.include_router(echo_router)
private_router.message.filter(F.chat.type == "private")
private_router.callback_query.filter(F.chat.type == "private")