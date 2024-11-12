from telebot import types

import telebot
import text


def handle_id(message: telebot.types.Message, bot: telebot.TeleBot, user_id, user_name):
    handle_keyboard = types.InlineKeyboardMarkup()

    btn_present = types.InlineKeyboardButton(text="Присудствую", callback_data="present")
    btn_not_present = types.InlineKeyboardButton(text="Отсудствую по УП", callback_data="not present")
    btn_exit = types.InlineKeyboardButton(text="◀ Вернутся", callback_data="back_to_menu")

    handle_keyboard.add(btn_present)
    handle_keyboard.add(btn_not_present)
    handle_keyboard.add(btn_exit)

    print(f"Присудствие {user_id} - {user_name}")

    if user_id in text.name_student:
        name = text.name_student[user_id]

        # Обновляем текст сообщения и клавиатуру
        try:
            bot.edit_message_text(
                text=f"Вы успешно автаризированы, как {name}\n\nВыберите нужный вам пункт:",
                chat_id=message.chat.id,
                message_id=message.message_id,
                reply_markup=handle_keyboard
            )
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Ошибка при редактировании сообщения: {e}")
    else:
        bot.send_message(message.chat.id,
                         "Ваш ID не найден в базе.\n\nЕсли вы являетесь учеником группы ИС-24-07 "
                         "обратитесь за помощью к разработчику - (@furstrot)")