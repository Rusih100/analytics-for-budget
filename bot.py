import asyncio
import logging
from aiogram import Bot, Dispatcher

import handlers.start
import handlers.fast_add
from settings import settings

from table import Table

from pprint import pprint


# Получение данных из переменных окружения
SPREADHEET_ID = settings.SPREADHEET_ID.get_secret_value()
TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN.get_secret_value()

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=TELEGRAM_TOKEN)  # Объект бота
dp = Dispatcher()                # Диспетчер


async def main():
    dp.include_router(handlers.start.router)
    dp.include_router(handlers.fast_add.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())



# pprint(
#     Table(SPREADHEET_ID).append_expense(
#         'Нулевая трата', 'Тестовоrferfwefе название', 0
#     )
# )