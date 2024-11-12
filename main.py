from dotenv import load_dotenv

import clicking
import telebot
import menu
import os


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(token=BOT_TOKEN)

user_contexts = {}


@bot.message_handler(commands=["start"])
def start_bot(message: telebot.types.Message):
    user_id, user_name = menu.menu(message, bot)
    user_contexts[message.chat.id] = {"id": user_id, "name": user_name}


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call: telebot.types.CallbackQuery):
    user_context = user_contexts.get(call.message.chat.id)
    if user_context:
        clicking.callback_query(call, bot, user_context)
    else:
        bot.answer_callback_query(call.id, "Контекст пользователя не найден.")


if __name__ == "__main__":
    bot.polling(non_stop=True)
