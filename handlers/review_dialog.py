

"""тут 4 и 5 дзшки"""


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

ratings = {"Отлично": 5, "Хорошо": 4, "Удовлетворительно": 3, "Плохо": 2, "Ужасно": 1}

rating_keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton(text) for text in ratings.keys()]],
    resize_keyboard=True, one_time_keyboard=True
)

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
    await message.answer("Ваш телефон или Instagram:")
    await state.set_state(RestourantReview.contact)

@review_router.message(RestourantReview.contact)
async def get_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await message.answer("Дата посещения (например, 2024-11-28):")
    await state.set_state(RestourantReview.visit_date)

@review_router.message(RestourantReview.visit_date)
async def get_visit_date(message: types.Message, state: FSMContext):
    if "-" in message.text and len(message.text.split("-")) == 3:
        await state.update_data(visit_date=message.text)
        await message.answer("Оцените качество еды:", reply_markup=rating_keyboard)
        await state.set_state(RestourantReview.food_rating)
    else:
        await message.answer("Некорректная дата! Введите в формате YYYY-MM-DD.")

@review_router.message(RestourantReview.food_rating)
@review_router.message(RestourantReview.cleanliness_rating, state=RestourantReview.cleanliness_rating)
async def get_rating(message: types.Message, state: FSMContext):
    if message.text in ratings:
        current_state = await state.get_state()
        await state.update_data({current_state.split(":")[-1]: ratings[message.text]})
        if current_state == RestourantReview.food_rating.state:
            await message.answer("Оцените чистоту:", reply_markup=rating_keyboard)
            await state.set_state(RestourantReview.cleanliness_rating)
        else:
            await message.answer("Дополнительные комментарии:", reply_markup=ReplyKeyboardRemove())
            await state.set_state(RestourantReview.extra_comments)
    else:
        await message.answer("Пожалуйста, выберите оценку из предложенных вариантов.")

@review_router.message(RestourantReview.extra_comments)
async def get_extra_comments(message: types.Message, state: FSMContext):
    data = await state.get_data()
    reviewed_users.add(message.from_user.id)
    await message.answer(
        f"Спасибо за отзыв!\n"
        f"Имя: {data['name']}\nКонтакт: {data['contact']}\n"
        f"Дата посещения: {data['visit_date']}\n"
        f"Еда: {data['food_rating']} ⭐️\nЧистота: {data['cleanliness_rating']} ⭐️\n"
        f"Комментарий: {message.text}"
    )
    await state.clear()
