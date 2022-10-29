from google_sheets_api import SheetsAPI
from datetime import datetime, timedelta


class GoogleTable(SheetsAPI):
    """
    Класс для работы с таблицами аналитики
    """

    # Словарь диапазонов таблиц для функций
    __RANGE_DICT = {
        'MAX_ID': 'settings!H2',                # get_max_id(...)
        'CATEGORIES_DICT': 'settings!A2:B',     # get_dict_categories(...)
        'CATEGORIES_LIST': 'settings!B2:B',     # get_list_categories(...)
        'ID_TELEGRAM_DICT': 'settings!E2:F',    # get_dict_user_id(...)
        'ID_TELEGRAM_LIST': 'settings!E2:E',    # get_list_user_id(...)
        'APPEND_TABLE': 'input-api!A2:H',       # append_expense(...)
    }

    @staticmethod
    def convert_telegram_time(date: datetime):
        """
        Конвертирует формат даты телеграмма, в формат дд.мм.гггг
        """
        result = date + timedelta(hours=10)
        result = result.strftime('%d.%m.%Y')
        return result

    # Получение данных с таблиц

    def get_max_id(self):
        """
        Получение максимального id записи из таблицы
        """
        values = self.get_data(
            self.__RANGE_DICT['MAX_ID']
        )
        max_id = int(values['values'][0][0])
        return max_id

    def get_dict_categories(self):
        """
        Получение словаря категорий трат - {<имя категории>: <id категории>}
        """
        values = self.get_data(
            self.__RANGE_DICT['CATEGORIES_DICT']
        )
        values = values['values']

        result = dict()
        for index, name in values:
            result[name] = int(index)
        return result

    def get_list_categories(self):
        """
        Получение листа категорий трат
        """
        values = self.get_data(
            self.__RANGE_DICT['CATEGORIES_LIST']
        )
        values = values['values']
        return [i[0] for i in values]

    def get_dict_user_id(self):
        """
        Получение словаря - {<id пользователя>: <Имя пользователя>}
        """
        values = self.get_data(
            self.__RANGE_DICT['ID_TELEGRAM_DICT']
        )
        values = values['values']

        result = dict()
        for telegram_id, name in values:
            result[telegram_id] = name
        return result

    def get_list_user_id(self):
        """
        Получения списка всех id пользователей telegram, у которых есть права на бота
        """
        values = self.get_data(
            self.__RANGE_DICT['ID_TELEGRAM_LIST']
        )
        values = values['values']
        return [int(i[0]) for i in values]

    # Добавление данных в таблицы

    def _get_categoty_pair(self, category: str):
        """
        Возвращает пару (<id категории>, <имя категории>)
        Если такой категории трат нет в таблице вернет ('', '')
        """
        all_categories = self.get_dict_categories()

        if category in all_categories:
            return all_categories[category], category
        else:
            return '', ''

    def append_expense(
            self,
            date_add: datetime, category: str, expense_name: str, amount_expenses: int,
            comment: str = '', user_name: str = ''
    ):
        """
        Добавляет данные о трате
        """
        category_id, category_name = self._get_categoty_pair(category)
        date = self.convert_telegram_time(date_add)

        data = [
            [
                self.get_max_id() + 1,   # Получение максимального ID из Google Sheets
                date,                    # Время
                category_id,             # ID категории
                category_name,           # Название категории
                expense_name,            # Назввание траты
                amount_expenses,         # Сумма траты
                comment,                 # Комментарий
                user_name                # Имя пользователя
            ]
        ]
        return self.append_data(
            self.__RANGE_DICT['APPEND_TABLE'], data
        )
