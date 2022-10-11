from dotenv import load_dotenv

from table import Table

from telebot.types import Message
import telebot

from pprint import pprint
import os


# Получение данных из переменных окружения
load_dotenv()
SPREADHEET_ID = os.getenv('SPREADHEET_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(func=lambda x: True)
def all_message(message: Message):
    bot.send_message(chat_id=message.chat.id, text=str(message.from_user.id))


bot.infinity_polling()

# pprint(
#     Table(SPREADHEET_ID).append_expense(
#         'Нулевая трата', 'Тестовоrferfwefе название', 0
#     )
# )


