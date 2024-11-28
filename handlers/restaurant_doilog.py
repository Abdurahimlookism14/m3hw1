from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

review_router = Router()
reviewed_users = set()

class RestourantReview(StatesGroup):
    name = State()
    contact = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

@review_router.callback_query(F.data == "review")
async def start_review(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id in reviewed_users:
        await callback.message.answer("Вы уже оставляли отзыв!")
        await state.clear()
    else:
        await callback.message.answer("Как вас зовут?")
        await state.set_state(RestourantReview.name)

@review_router.message(RestourantReview.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажите ваш телефон или Instagram:")
    await state.set_state(RestourantReview.contact)

@review_router.message(RestourantReview.contact)
async def get_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await message.answer("Когда вы посещали наше заведение? (например, 2024-11-28)")
    await state.set_state(RestourantReview.visit_date)

@review_router.message(RestourantReview.visit_date)
async def get_visit_date(message: types.Message, state: FSMContext):
    await state.update_data(visit_date=message.text)
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton(str(i)) for i in range(1, 6)]],
        resize_keyboard=True, one_time_keyboard=True
    )
    await message.answer("Оцените качество еды (1-5):", reply_markup=keyboard)
    await state.set_state(RestourantReview.food_rating)

@review_router.message(RestourantReview.food_rating)
async def get_food_rating(message: types.Message, state: FSMContext):
    await state.update_data(food_rating=message.text)
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton(str(i)) for i in range(1, 6)]],
        resize_keyboard=True, one_time_keyboard=True
    )
    await message.answer("Оцените чистоту (1-5):", reply_markup=keyboard)
    await state.set_state(RestourantReview.cleanliness_rating)

@review_router.message(RestourantReview.cleanliness_rating)
async def get_cleanliness_rating(message: types.Message, state: FSMContext):
    await state.update_data(cleanliness_rating=message.text)
    await message.answer("Есть ли у вас дополнительные комментарии?",
    reply_markup=ReplyKeyboardRemove())
    await state.set_state(RestourantReview.extra_comments)

@review_router.message(RestourantReview.extra_comments)
async def get_extra_comments(message: types.Message, state: FSMContext):
    data = await state.get_data()
    reviewed_users.add(message.from_user.id)
    await message.answer(
        f"Спасибо за ваш отзыв\n"
        f"Имя: {data['name']}\n"
        f"Контакт: {data['contact']}\n"
        f"Дата посещения: {data['visit_date']}\n"
        f"Качество еды: {data['food_rating']}\n"
        f"Чистота: {data['cleanliness_rating']}\n"
        f"Комментарий: {message.text}"
    )
    await state.clear()