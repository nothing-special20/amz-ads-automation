from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account
import requests
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

GOOGLE_SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

GOOGLE_SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE")
GOOGLE_SHEET_MAX_RANGE = str(os.environ.get("GOOGLE_SHEET_MAX_RANGE"))

creds = None
creds = service_account.Credentials.from_service_account_file(
        GOOGLE_SERVICE_ACCOUNT_FILE, scopes=GOOGLE_SCOPES)

SPREAD_COLS_BASE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

SPREAD_COLS = SPREAD_COLS_BASE
SPREAD_COLS.extend(['a' + x for x in SPREAD_COLS_BASE])


GOOGLE_SHEETS_SERVICE = build('sheets', 'v4', credentials=creds)

def google_append_sheet(values, spreadsheet_id):
    try:
        end_col = SPREAD_COLS[len(values[0])]

        SHEET_RANGE = 'A1:'+ end_col + GOOGLE_SHEET_MAX_RANGE

        # Call the Sheets API
        GOOGLE_SHEETS_SERVICE.spreadsheets().values().append(spreadsheetId=spreadsheet_id, 
                                                range=SHEET_RANGE, 
                                                valueInputOption="USER_ENTERED", 
                                                body={"values": values}).execute()

        if not values:
            print('No data found.')

    except HttpError as err:
        print(err)

def google_create_sheet(values, file_name):
    try:
        spreadsheet = {
            'properties': {
                'title': file_name
            }
        }
        request = GOOGLE_SHEETS_SERVICE.spreadsheets().create(body=spreadsheet)
        response = request.execute()
        spreadsheet_id = response['spreadsheetId']
        #
        end_col = SPREAD_COLS[len(values[0])]

        SHEET_RANGE = 'A1:'+ end_col + '1'

        # Call the Sheets API
        GOOGLE_SHEETS_SERVICE.spreadsheets().values().update(spreadsheetId=spreadsheet_id, 
                                                range=SHEET_RANGE, 
                                                valueInputOption="USER_ENTERED", 
                                                body={"values": values}).execute()

        return spreadsheet_id

    except HttpError as err:
        print(err)

def google_share_file(real_file_id, email):
    """Batch permission modification.
    Args:
        real_file_id: file Id
        real_user: User ID
        real_domain: Domain of the user ID
    Prints modified permissions

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    try:
        # create gmail api client
        service = build('drive', 'v3', credentials=creds)
        ids = []
        file_id = real_file_id

        def callback(request_id, response, exception):
            if exception:
                # Handle error
                print(exception)
            else:
                print(f'Request_Id: {request_id}')
                print(F'Permission Id: {response.get("id")}')
                ids.append(response.get('id'))

        # pylint: disable=maybe-no-member
        batch = service.new_batch_http_request(callback=callback)
        user_permission = {
            "type": "user",
            "role": "writer",
            "emailAddress": email
        }
        batch.add(service.permissions().create(fileId=file_id,
                                               body=user_permission,
                                               fields='id',))
        batch.execute()

    except HttpError as error:
        print(F'An error occurred: {error}')
        ids = None

    return ids
