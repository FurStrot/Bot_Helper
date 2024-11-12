from google_tabl import get_attendance
from telebot import types
from datetime import date

import telebot
import text


current_date = date.today()


def show_information_user(message: telebot.types.Message, bot: telebot.TeleBot, user_id, user_name):
    si_keyboard = types.InlineKeyboardMarkup()

    btn_exit = types.InlineKeyboardButton(text="Выйти в меню", callback_data="back_to_menu")
    si_keyboard.add(btn_exit)

    if user_id in text.name_student:
        name = text.name_student[user_id]

        attendance_count = get_attendance(name)

        if attendance_count:
            active, state_home, not_active = attendance_count
            try:
                procent = active + state_home + not_active
                total_procent = active/procent * 100

                bot.edit_message_text(
                    f"Абитуриент, <b>{name}</b> имеет следующую посещаемость:\n\n"
                    f"<code><b>Присутствовал(а):</b> {active} - раз\n"
                    f"<b>Пропускал(а) по УП:</b> {state_home} - раз\n"
                    f"<b>Отсутствовал(а):</b> {not_active} - раз</code>\n\n"
                    f"<code><b>Процент посещаемости: {int(total_procent)}%\n\n</b></code>"
                    f"<b>Дата:</b> {current_date}",
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    reply_markup=si_keyboard,
                    parse_mode="HTML"
                )
            except Exception as error:
                print(error)

                total_procent = 0
                bot.edit_message_text(
                    f"Абитуриент, <b>{name}</b> имеет следующую посещаемость:\n\n"
                    f"<code><b>Присутствовал(а):</b> {active} - раз\n"
                    f"<b>Пропускал(а) по УП:</b> {state_home} - раз\n"
                    f"<b>Отсутствовал(а):</b> {not_active} - раз</code>\n\n"
                    f"<code><b>Процент посещаемости: {int(total_procent)}%\n\n</b></code>"
                    f"<b>Дата:</b> {current_date}",
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    reply_markup=si_keyboard,
                    parse_mode="HTML"
                )

        else:
            bot.send_message(message.chat.id, f"Не удалось получить данные о посещяемости для {name}.",
                             reply_markup=si_keyboard)
    else:
        bot.send_message(message.chat.id, "Ваш ID не найден в базе.\n\nЕсли вы являетесь учеником группы ИС-24-07 "
                                          "обратитесь за помощью к разработчику - (@furstrot)")