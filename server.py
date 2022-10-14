from dotenv import load_dotenv

from table import Table

from pprint import pprint
import os


# Получение данных из переменных окружения
load_dotenv()
SPREADHEET_ID = os.getenv('SPREADHEET_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


# pprint(
#     Table(SPREADHEET_ID).append_expense(
#         'Нулевая трата', 'Тестовоrferfwefе название', 0
#     )
# )


