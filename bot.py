import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message

import handlers.start
import handlers.fast_add

from google_table import GoogleTable
from settings import settings


# Получение данных из переменных окружения
TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN.get_secret_value()
SPREADHEET_ID = settings.SPREADHEET_ID.get_secret_value()

# Обертка для работы с таблицами
GOOGLE_TABLE = GoogleTable(SPREADHEET_ID)

# Логирование
logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=TELEGRAM_TOKEN)  # Объект бота
dp = Dispatcher()                # Диспетчер


@dp.message(commands=['test'])
async def process_start_command(message: Message):
    text = '123'
    await message.answer(
        text=text
    )
    print(GOOGLE_TABLE.get_list_user_id())
    print(GOOGLE_TABLE.get_list_categories())


async def main():
    dp.include_router(handlers.start.router)
    dp.include_router(handlers.fast_add.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
