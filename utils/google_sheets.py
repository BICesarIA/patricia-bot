from datetime import datetime
import os
import json
import base64
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
import gspread

load_dotenv()

creds_base64 = os.getenv("GOOGLE_SHEET_CREDENTIALS")
creds_json = base64.b64decode(creds_base64).decode("utf-8")
creds_dict = json.loads(creds_json)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)


def delete_old_messages(from_number):
    sheet = client.open("data").worksheet("Sheet1")

    all_rows = sheet.get_all_values()
    headers = all_rows[0]
    new_rows = [row for row in all_rows if row[1] != from_number or row == headers]
    sheet.clear()
    sheet.append_row(headers)
    for row in new_rows[1:]:
        sheet.append_row(row)


def write_on_sheet_file(data):
    if data["typeResponse"] == "gpt":
        sheet = client.open("data").worksheet("Sheet1")
        isFirstMesage = save_new_phone_number_if_needed(data["from"])

        new_row = [
            "PRIMERO!" if isFirstMesage else "",
            data["from"],
            data["incoming_msg"]["content"] if data["incoming_msg"] else "",
            data["response"]["content"] if data["response"] else "",
            data["created_at"],
        ]
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
    cedulas_sheet = client.open("data").worksheet("Cedulas")
    numbers = cedulas_sheet.col_values(1)

    if phone_number not in numbers:
        cedulas_sheet.append_row([phone_number, datetime.now().isoformat()])
        return True
    return False
