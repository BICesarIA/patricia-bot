import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name("sheetCredentials.json", scope)
client = gspread.authorize(creds)


def write_on_sheet_file(data):
    sheet = client.open("data").worksheet("Sheet1")
    new_row = [
        data["from"],
        data["incoming_msg"],
        data["response"],
        data["created_at"],
    ]
    sheet.append_row(new_row)
