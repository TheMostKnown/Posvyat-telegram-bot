from tgbot.handlers.spreadsheet_parser.spreadsheet_parser import get_data
from tgbot.config import settings

test_sheets_id = settings.GOOGLE_TABLE_ID


def test_parser():

    sheets_data = get_data(
        spreadsheet_id=test_sheets_id,
        creds_file_name=settings.GOOGLE_CREDS_PATH,
        token_file_name=settings.GOOGLE_TOKEN_PATH
    )

    sheet = sheets_data['Лист1']
    print(sheet)

    assert (sheet[0][0] == 'Клоун обыкновенный')
    assert (sheet[0][1] == '1')
    assert (sheet[0][2] == 'Зарегался')


def test_guest_filter():

    def get_guests_status(
            spreadsheet_id: str,
            sheet_name: str,
            vk_link_column: int,
            status_column: int,
            creds_file_name: str,
            token_file_name: str
    ) -> dict:
        guests = dict()

        try:
            guest_sheet = get_data(
                spreadsheet_id,
                creds_file_name,
                token_file_name
            )[sheet_name]

            for row in guest_sheet:

                if row[vk_link_column]:

                    if row[status_column]:

                        guests[row[vk_link_column]] = row[status_column]
                    else:
                        guests[vk_link_column] = ''

        except AttributeError as e:
            print(f'{AttributeError}: No such key in spreadsheet')

        return guests

    sheets_data = get_guests_status(
        spreadsheet_id=test_sheets_id,
        sheet_name='Лист1',
        vk_link_column=0,
        status_column=2,
        creds_file_name=settings.GOOGLE_CREDS_PATH,
        token_file_name=settings.GOOGLE_TOKEN_PATH
    )

    print(sheets_data)


if __name__ == '__main__':
    test_parser()
