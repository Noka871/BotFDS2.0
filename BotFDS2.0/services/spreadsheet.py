import gspread
from oauth2client.service_account import ServiceAccountCredentials

def export_to_sheet(data):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Dubbing Reports").sheet1
    sheet.clear()
    sheet.append_rows(data)