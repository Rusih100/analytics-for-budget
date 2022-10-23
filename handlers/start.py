from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(commands=['start'])
async def process_start_command(message: Message):
    text = 'Привет, я твой бот для контроля финансов! \n' \
           'Для того чтобы добавить трату используй команду /add ' \
           'или /fast_add'
    await message.answer(
        text=text
    )