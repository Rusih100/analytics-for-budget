from table import Table
from pprint import pprint


SPREADHEET_ID = '1n2YeegCltLcsHskPTohPY70aXd-7VlOj5AYTDEFyR_o'

pprint(
    Table(SPREADHEET_ID).append_expense(
        'Тест', 'Тестовое название', 0
    )
)