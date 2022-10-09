from google_sheets_api import Sheets_API


class Table(Sheets_API):
    """
    Класс для работы с таблицами аналитики
    """

    def get_max_id(self):
        """
        Получение максимального id записи из таблицы
        """
        values = self.get_data('settings!G2')
        max_id = int(values['values'][0][0])
        return max_id
