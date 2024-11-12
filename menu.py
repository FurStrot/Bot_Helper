from telebot import types

import telebot

photo_cache = None


def menu(message: telebot.types.Message, bot: telebot.TeleBot):
    user_find_id = message.from_user.id
    user_find_name = message.from_user.username

    keyboard_menu = types.InlineKeyboardMarkup()
    btn_visiting = types.InlineKeyboardButton(text="Посещение", callback_data="visiting")
    btn_check_attendance = types.InlineKeyboardButton(text="Проверить посещаемость", callback_data="check_attendance")
    btn_exit = types.InlineKeyboardButton(text="Выйти", callback_data="exit")

    keyboard_menu.add(btn_visiting)
    keyboard_menu.add(btn_check_attendance)
    keyboard_menu.add(btn_exit)

    bot.send_message(message.chat.id, f"Привет! Я бот Лисёнок Хелпи.\n\n"
                                      f"Я создан, чтобы упростить и автоматизировать отслеживание твоего посещения. "
                                      f"Буду рад помочь!", reply_markup=keyboard_menu)

    return user_find_id, user_find_name


def menu_later(message: telebot.types.Message, bot: telebot.TeleBot):
    keyboard_menu_later = types.InlineKeyboardMarkup()
    btn_visiting = types.InlineKeyboardButton(text="Посещение", callback_data="visiting")
    btn_check_attendance = types.InlineKeyboardButton(text="Проверить посещаемость", callback_data="check_attendance")
    btn_exit = types.InlineKeyboardButton(text="Выйти", callback_data="exit")

    keyboard_menu_later.add(btn_visiting)
    keyboard_menu_later.add(btn_check_attendance)
    keyboard_menu_later.add(btn_exit)

    bot.edit_message_text(
        f"Привет! Я бот Лисёнок Хелпи.\n\n"
        f"Я создан, чтобы упростить и автоматизировать отслеживание твоего посещения. "
        f"Буду рад помочь!",
        chat_id=message.chat.id,
        message_id=message.message_id,
        reply_markup=keyboard_menu_later
    )