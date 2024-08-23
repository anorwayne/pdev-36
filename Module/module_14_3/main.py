from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import *
from keyboards import *

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands = ['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Выберите действие:", reply_markup = keyboard)

@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
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

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



