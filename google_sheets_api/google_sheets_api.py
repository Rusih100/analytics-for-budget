import httplib2
import apiclient.discovery

from oauth2client.service_account import ServiceAccountCredentials
from typing import List


class SheetsAPI:
    """
    Небольшая обертка для работы с API Google Sheets
    """

    def __init__(self, spreadheet_id: str, credentials_file: str = 'google-api-key.json'):
        """
        Конструктор принимающий id таблицы и файл с ключами доступа (по умолчанию - 'google-api-key.json')
        """
        # ID Google Sheets документа (можно взять из его URL)
        self.__spreadheet_id = spreadheet_id

        # Файл, полученный в Google Developer Console
        self.__credentials_file = credentials_file

        # Авторизуемся и получаем service — экземпляр доступа к API
        self.__credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.__credentials_file, [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
        )
        self.__httpAuth = self.__credentials.authorize(httplib2.Http())
        self.__service = apiclient.discovery.build('sheets', 'v4', http=self.__httpAuth)

    def get_data(self, table_range: str, major_dimension: str = 'ROWS'):
        """
        Получение данных с таблицы:
            table_range - строка диапазона в формате 'base!A2:H'
            major_dimension - ROWS или COLUMNS
        """
        values = self.__service.spreadsheets().values().get(
            spreadsheetId=self.__spreadheet_id,
            range=table_range,
            majorDimension=major_dimension
        ).execute()
        return values

    def append_data(self, table_range: str, data: List[List]):
        """
        Добавление данных в таблицу:
            table_range - строка диапазона в формате 'base!A2:H'
            data - данные в виде списка списков
        """
        request = self.__service.spreadsheets().values().append(
            spreadsheetId=self.__spreadheet_id,
            range=table_range,
            valueInputOption='USER_ENTERED',
            body={
                'values': data
            }
        )
        response = request.execute()
        return response
