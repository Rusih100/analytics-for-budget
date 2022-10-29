from aiogram import Router
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext

from settings import settings
from google_table import GoogleTable

from pydantic.error_wrappers import ValidationError
from pydantic_models.expense_model import ExpenseModel


# Получение данных из переменных окружения
SPREADHEET_ID = settings.SPREADHEET_ID.get_secret_value()

# Обертка для работы с таблицами
GOOGLE_TABLE = GoogleTable(SPREADHEET_ID)


router = Router()


class FastAdd(StatesGroup):
    expense_input = State()


@router.message(commands=['fast_add'])
async def process_start_command(message: Message, state: FSMContext):
    text_start = 'Чтобы добавить трату, отправь мне сообщение в следующем формате:'
    await message.answer(
        text=text_start
    )

    text_middle = 'Категория траты\n' \
                  'Название траты\n' \
                  'Сумма траты'
    await message.answer(
        text=text_middle,
    )
    await state.set_state(FastAdd.expense_input)


@router.message(FastAdd.expense_input)
async def expense_input(message: Message, state: FSMContext):

    text = message.text.split('\n')
    user_id = message.from_user.id
    date_add = message.date

    try:
        category_name = text[0]
        expense_name = text[1]
        amount_expenses = text[2]

        expense = ExpenseModel(
            date_add=date_add,
            category_name=category_name,
            expense_name=expense_name,
            amount_expenses=amount_expenses,
            user_id=user_id
        )

        GOOGLE_TABLE.append_expense(
            date_add=expense.date_add,
            category=expense.category_name,
            expense_name=expense.expense_name,
            amount_expenses=expense.amount_expenses,
            user_id=expense.user_id
        )

    except IndexError:
        await message.answer(
            text='Проверьте корректность ввода'
        )

    except ValidationError as exception:
        # Получение места ошибки
        error = exception.raw_errors[0].loc_tuple()[0]
        if error == 'category_name':
            await message.answer(
                text='Данной категории трат нет в исходной таблице'
            )
        if error == 'amount_expenses':
            await message.answer(
                text='Сумма расходов должна быть положительным числом'
            )

    else:
        await message.answer(
            text='Даные успешно добавлены'
        )
        await state.clear()

