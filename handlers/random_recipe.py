import random
from aiogram import Router, types

recipe_router = Router()

recipes = [
    {"name": "Пицца Маргарита", "image": "images/pizza.jpg", "description": "Ингредиенты: сыр, томаты, базилик."},
    {"name": "Бургер", "image": "images/burger.jpg", "description": "Ингредиенты: булочка, котлета, салат, сыр."},
    {"name": "Паста Карбонара", "image": "images/pasta.jpg", "description": "Ингредиенты: паста, бекон, сыр, яйца."}
]

@recipe_router.message(commands=["recipe"])
async def random_recipe(message: types.Message):
    recipe = random.choice(recipes)
    with open(recipe["image"], "rb") as photo:
        await message.answer_photo(
            photo=photo,
            caption=f"<b>{recipe['name']}</b>\n{recipe['description']}"
        )