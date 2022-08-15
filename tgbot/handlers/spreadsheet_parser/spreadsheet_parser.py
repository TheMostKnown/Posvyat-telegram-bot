import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def get_creds(creds_abs_path: str, token_abs_path: str) -> Credentials:
    """
    Parameter:
        creds_json : str
            google api credentials from config.py
        token_json : str
            google api token from config.py
    Returns:
        credentials for authorization in google api
    """

    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
              'https://www.googleapis.com/auth/drive']

    creds = None

    if os.path.exists(token_abs_path):
        creds = Credentials.from_authorized_user_file(token_abs_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_abs_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_abs_path, 'w') as token:
            token.write(creds.to_json())

    return creds


def get_data(
        spreadsheet_id: str,
        creds_abs_path: str = 'creds.json',
        token_abs_path: str = 'token.json'
) -> dict:
    """Function retrieves all non-empty rows from spreadsheet

    :param spreadsheet_id: id of google spreadsheet
    :type spreadsheet_id: str

    :param creds_abs_path: absolute path to the file with saved credentials
    :type creds_abs_path: str

    :param token_abs_path : absolute path to the file with saved auth token
    :type token_abs_path: str

    :return: all sheets' data in lists
    :rtype: dict
    """

    tables = dict()

    creds = get_creds(creds_abs_path, token_abs_path)

    service = build('sheets', 'v4', credentials=creds)

    request = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        includeGridData=True
    )
    response = request.execute()

    sheets = response['sheets']

    for sheet in sheets:
        sheet_title = sheet['properties']['title']

        tables[sheet_title] = []

        grid_data = sheet['data']

        for data in grid_data:
            if 'rowData' not in data.keys():
                continue

            rowData = data['rowData']

            for i, row in enumerate(rowData):

                if 'values' in row.keys():

                    for j, value in enumerate(row['values']):

                        if value and 'formattedValue' in value.keys():
                            row['values'][j] = value['formattedValue']
                        else:
                            row['values'][j] = None

                    tables[sheet_title].append(row['values'])

                else:
                    tables[sheet_title].append(None)

    return tables
