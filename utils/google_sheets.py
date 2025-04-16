from datetime import datetime
import os
import json
import base64
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
import gspread
import pandas as pd

load_dotenv()

creds_base64 = os.getenv("GOOGLE_SHEET_CREDENTIALS")
creds_json = base64.b64decode(creds_base64).decode("utf-8")
creds_dict = json.loads(creds_json)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]

creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)


def read_sheet_inventario(sheet_file, sheet_tab):
    sheet = client.open(sheet_file).worksheet(sheet_tab)
    rows = sheet.get_all_values()
    return pd.DataFrame(rows[1:], columns=rows[0])


def delete_old_messages(from_number):
    sheet = client.open("Inventario").worksheet("Chats")

    all_rows = sheet.get_all_values()
    headers = all_rows[0]
    new_rows = [row for row in all_rows if row[1] != from_number or row == headers]
    sheet.clear()
    sheet.append_row(headers)
    for row in new_rows[1:]:
        sheet.append_row(row)


def update_last_message_timestamp(phone_number, last_message_date):
    sheet = client.open("Inventario").worksheet("Telefono")
    all_rows = sheet.get_all_values()

    rows = all_rows[1:]

    for i, row in enumerate(rows):
        if len(row) >= 1 and row[0] == phone_number:
            row_index = i + 2
            sheet.update_cell(row_index, 3, last_message_date)
            break


def write_on_sheet_file(data):
    sheet = client.open("Inventario").worksheet("Chats")
    isFirstMesage = save_new_phone_number_if_needed(data["from"])

    incoming_msg = (
        data["incoming_msg"]["content"]
        if data["typeResponse"] == "gpt"
        else data["incoming_msg"]
    )
    response = (
        data["response"]["content"]
        if data["typeResponse"] == "gpt"
        else data["response"]
    )

    all_rows = sheet.get_all_values()
    headers = all_rows[0]
    rows = all_rows[1:]

    old_message = [row for row in rows if len(row) < 2 or row[1] == data["from"]]
    if old_message and isFirstMesage == False:
        isFirstMesage = len(old_message[0][0]) > 0

    new_rows = [row for row in rows if len(row) < 2 or row[1] != data["from"]]

    sheet.clear()
    sheet.append_row(headers)
    for row in new_rows:
        sheet.append_row(row)

    new_row = [
        "PRIMERO" if isFirstMesage else "",
        data["from"],
        incoming_msg,
        response,
        data["created_at"],
    ]
    update_last_message_timestamp(data["from"], data["created_at"])
    sheet.append_row(new_row)
    sort_sheet_by_column(sheet, column_index=5)


def sort_sheet_by_column(sheet, column_index=1):
    data = sheet.get_all_values()
    header = data[0]
    rows = data[1:]

    sorted_rows = sorted(
        [row for row in rows if len(row) >= column_index],
        key=lambda x: x[column_index - 1],
    )

    sheet.clear()
    sheet.append_row(header)
    for row in sorted_rows:
        sheet.append_row(row)


def save_new_phone_number_if_needed(phone_number):
    cedulas_sheet = client.open("Inventario").worksheet("Telefono")
    numbers = cedulas_sheet.col_values(1)

    if phone_number not in numbers:
        created_at = datetime.strptime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        cedulas_sheet.append_row([phone_number, created_at])
        return True
    return False
