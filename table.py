from google_sheets_api import Sheets_API
from datetime import datetime
from pytz import timezone


class Table(Sheets_API):
    """
    Класс для работы с таблицами аналитики
    """

    @staticmethod
    def get_now_time():
        """
        Возвращает строку текущей даты
        """
        zone = timezone('Asia/Vladivostok')
        now_time = datetime.now(zone)
        result = now_time.strftime('%d.%m.%Y')
        return str(result)

    # Получение данных с таблиц

    def get_max_id(self):
        """
        Получение максимального id записи из таблицы
        """
        values = self.get_data('settings!G2')
        max_id = int(values['values'][0][0])
        return max_id

    def get_list_categories(self):
        """
        Получение словаря категорий трат - {<имя категории>: <id категории>}
        """
        values = self.get_data('settings!A2:B')
        values = values['values']

        result = dict()
        for index, name in values:
            result[name] = int(index)
        return result

    # Добавление данных в таблицы

    def append_expense(
            self, category: str, expense_name: str, amount_expenses: int, comment: str = '', user: str = ''
    ):
        """
        Добавляет данные о трате
        """
        data = [
            [
                self.get_max_id() + 1,
                self.get_now_time(),
                '',
                category,
                expense_name,
                amount_expenses,
                comment,
                user
            ]
        ]
        return self.append_data('input-api!A2:H', data)
