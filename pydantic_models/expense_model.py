from pydantic import BaseModel, validator
from datetime import datetime

from google_table import GoogleTable
from settings import settings


# Получение данных из переменных окружения
SPREADHEET_ID = settings.SPREADHEET_ID.get_secret_value()

# Обертка для работы с таблицами
GOOGLE_TABLE = GoogleTable(SPREADHEET_ID)


class ExpenseModel(BaseModel):
    date_add: datetime
    category_name: str
    expense_name: str
    amount_expenses: int

    comment: int = ''
    user_id: int = ''

    @validator('amount_expenses')
    def check_amount_expenses(cls, value):
        if value < 0:
            raise ValueError('amount_expenses >= 0')
        return value

    @validator('category_name')
    def check_category_name(cls, value):
        if value not in GOOGLE_TABLE.get_list_categories():
            raise ValueError('category not found')
        return value
