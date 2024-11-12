from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
from telebot import types
from dotenv import load_dotenv

import threading
import os.path
import telebot
import logging
import queue
import text
import os


load_dotenv()
API_GOOGLE = os.getenv("google_id")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SAMPLE_SPREADSHEETS_ID = API_GOOGLE

SERVICE_ACCOUNT_FILE = 'credentials.json'

SAMPLE_RANGE_NAME = "List number!A4:AG28"

update_queue = queue.Queue()


def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(SERVICE_ACCOUNT_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_attendance(name):
    creds = get_credentials()
    try:
        service = build("sheets", "v4", credentials=creds)
        result = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEETS_ID, range=SAMPLE_RANGE_NAME).execute()
        values = result.get("values", [])

        active = 0
        state_home = 0
        not_active = 0
        for row in values:
            if len(row) > 0 and row[1] == name:
                for i in range(2, 32):
                    if i < len(row) and row[i].lower() == 'п':
                        active += 1
                    if i < len(row) and row[i].lower() == 'уп':
                        state_home += 1
                    if i < len(row) and row[i].lower() == 'от':
                        not_active += 1
        return active, state_home, not_active

    except HttpError as err:
        logging.error(f"Ошибка при получении посещаемости: {err}")
        return 0, 0, 0


def update_attendance_worker():
    while True:
        message, bot, user_id, mark = update_queue.get()
        try:
            update_attendance(message, bot, user_id, mark)
        finally:
            update_queue.task_done()


def update_attendance(message: telebot.types.Message, bot: telebot.TeleBot, user_id, mark):
    ua_keyboard = types.InlineKeyboardMarkup()
    btn_exit = types.InlineKeyboardButton(text="Выйти в меню", callback_data="back_to_menu")
    ua_keyboard.add(btn_exit)

    creds = get_credentials()
    try:
        service = build("sheets", "v4", credentials=creds)

        today = datetime.now()
        current_day = today.day

        result = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEETS_ID, range=SAMPLE_RANGE_NAME).execute()
        values = result.get("values", [])

        if user_id in text.name_student:
            name = text.name_student[user_id]
            print(f"Имя студента: {name}")
        else:
            return

        student_row_index = -1
        for row_index, row in enumerate(values):
            if len(row) > 1 and row[1].strip().lower() == name.lower():
                student_row_index = row_index + 4
                break

        if student_row_index == -1:
            bot.send_message(message.chat.id, "Студент не найден, обратитесь за помощью к @furstrot.")
            return

        day_column_index = current_day + 1

        if day_column_index < 1:
            return

        cell_to_update = f"List number!{chr(65 + day_column_index)}{student_row_index}"
        body = {"values": [[mark]]}

        service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEETS_ID,
                                               range=cell_to_update,
                                               valueInputOption="RAW",
                                               body=body).execute()
        print(f"Обновлено значение в ячейке {cell_to_update}")
        bot.edit_message_text(
            "Хорошо, я вас отметил, хорошего вам дня!",
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=ua_keyboard)

    except HttpError as err:
        logging.error(f"Ошибка при обновлении посещаемости: {err}")


def enqueue_update(message: telebot.types.Message, bot: telebot.TeleBot, user_id, mark):
    update_queue.put((message, bot, user_id, mark))


threading.Thread(target=update_attendance_worker, daemon=True).start()
