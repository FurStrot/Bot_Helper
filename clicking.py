from datetime import datetime
from telebot import types

import check_active
import google_tabl
import students
import telebot
import menu


def callback_query(call: types.CallbackQuery, bot: telebot.TeleBot, user_context):
    user_id = user_context["id"]
    user_name = user_context["name"]

    if call.data == "visiting":
        students.handle_id(call.message, bot, user_id, user_name)

    elif call.data == "check_attendance":
        check_active.show_information_user(call.message, bot, user_id, user_name)

    elif call.data == "exit":
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "present":
        google_tabl.enqueue_update(call.message, bot, user_id, "п")

    elif call.data == "not present":
        google_tabl.enqueue_update(call.message, bot, user_id, "уп")

    elif call.data == "back_to_menu":
        menu.menu_later(call.message, bot)
