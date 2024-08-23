from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import *
from keyboards import *
from crud_functions import get_products_list, register_user

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

@dp.message_handler(commands = ['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Выберите действие:", reply_markup = keyboard)

@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    products = get_products_list()
    for product in products:
        await message.reply(product)
    product_images = [
        'https://img.freepik.com/free-photo/brain-booster-pills-container-still-life_23-2150760050.jpg',
        'https://img.freepik.com/free-photo/brain-booster-pills-container-still-life_23-2150760050.jpg',
        'https://img.freepik.com/free-photo/brain-booster-pills-container-still-life_23-2150760050.jpg',
        'https://img.freepik.com/free-photo/brain-booster-pills-container-still-life_23-2150760050.jpg'
    ]

    for i in range(1, 5):
        await message.reply(f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100} рублей')
        await bot.send_photo(message.chat.id, photo=product_images[i - 1])

    await message.reply("Выберите продукт для покупки:", reply_markup=inline_keyboard)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.reply("Вы успешно приобрели продукт!")

@dp.message_handler(text='Информация')
async def send_info(message: types.Message):
    await message.reply("Информация")

@dp.message_handler(text='Регистрация')
async def sing_up(message: types.Message):
    await message.reply("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text
    if not username.isalpha():
        await message.reply("Имя пользователя должно содержать только латинские буквы. Попробуйте снова.")
        return
    if register_user(username, "", 0):
        await state.update_data(username=username)
        await message.reply("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.reply("Пользователь существует, введите другое имя.")
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.reply("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    age = int(message.text)
    user_data = await state.get_data()
    username = user_data['username']
    email = user_data['email']
    register_user(username, email, age)
    await message.reply("Регистрация завершена! Добро пожаловать!")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



