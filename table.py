from google_sheets_api import Sheets_API


class Table(Sheets_API):
    """
    Класс для работы с таблицами аналитики
    """

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

    def append_expense(self):
        """
        Добавляет данные о трате
        """
        pass
