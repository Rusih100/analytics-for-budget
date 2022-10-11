from google_sheets_api import Sheets_API
from datetime import datetime
from pytz import timezone


class Table(Sheets_API):
    """
    Класс для работы с таблицами аналитики
    """

    # Временная зона
    __TIMEZONE = 'Asia/Vladivostok'

    # Словарь диапазонов таблиц для функций
    __RANGE_DICT = {
        'MAX_ID': 'settings!H2',           # get_max_id(...)
        'CATEGORIES': 'settings!A2:B',     # get_dict_categories(...)
        'ID_TELEGRAM': 'settings!E2:E',    # get_list_user_id(...)
        'APPEND_TABLE': 'input-api!A2:H',  # append_expense(...)
    }

    def get_now_time(self):
        """
        Возвращает строку текущей даты
        """
        zone = timezone(self.__TIMEZONE)
        now_time = datetime.now(zone)
        result = now_time.strftime('%d.%m.%Y')
        return str(result)

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
            self.__RANGE_DICT['CATEGORIES']
        )
        values = values['values']

        result = dict()
        for index, name in values:
            result[name] = int(index)
        return result

    def get_list_user_id(self):
        """
        Получения списка всех id пользователей telegram, у которых есть права на бота
        """
        values = self.get_data(
            self.__RANGE_DICT['ID_TELEGRAM']
        )
        values = values['values']
        return [int(i) for i in values]

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
            self, category: str, expense_name: str, amount_expenses: int, comment: str = '', user: str = ''
    ):
        """
        Добавляет данные о трате
        """
        category_id, category_name = self._get_categoty_pair(category)
        data = [
            [
                self.get_max_id() + 1,
                self.get_now_time(),
                category_id,
                category_name,
                expense_name,
                amount_expenses,
                comment,
                user  # TODO: от Telegram bot
            ]
        ]
        return self.append_data(
            self.__RANGE_DICT['APPEND_TABLE'], data
        )
