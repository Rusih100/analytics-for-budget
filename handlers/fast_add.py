from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext

router = Router()


@router.message(commands=['fast_add'])
async def process_start_command(message: Message):
    text_start = 'Чтобы добавить трату, отправь мне сообщение в следующем формате:'
    await message.answer(
        text=text_start
    )

    text_middle = 'Категория траты\n' \
                  'Название траты\n' \
                  'Сумма траты'
    await message.answer(
        text=text_middle
    )

    text_end = 'P.S. Категории, название и сумма обязательно должны разделены переносом, иначе КРАХ!'
    await message.answer(
        text=text_end
    )


