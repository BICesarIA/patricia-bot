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
