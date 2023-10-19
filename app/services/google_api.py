from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"

ROW_COUNT = 100
COLUMN_COUNT = 3

START_WORK_WITH_REPORT = datetime.now().strftime(FORMAT)

SPREADSHEET_BODY = dict(
    properties=dict(
        title=f'Отчет закрытых проектов QRCat от {START_WORK_WITH_REPORT}',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=ROW_COUNT,
            columnCount=COLUMN_COUNT
        )))])

SPREADSHEET_TABLE = [
    ['Отчет от', START_WORK_WITH_REPORT],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    spreadsheet = (await wrapper_services.as_service_account(
        (await wrapper_services.discover(
            'sheets', 'v4'
        )).spreadsheets.create(json=SPREADSHEET_BODY)
    ))
    return spreadsheet['spreadsheetId'], spreadsheet['spreadsheetUrl']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    await wrapper_services.as_service_account(
        (await wrapper_services.discover('drive', 'v3')).permissions.create(
            fileId=spreadsheet_id,
            json={
                'type': 'user',
                'role': 'writer',
                'emailAddress': settings.email
            },
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle,
        projects: list,
) -> None:
    table_values = [
        *SPREADSHEET_TABLE,
        *[list(map(str,
                   [project.name,
                    str(project.close_date - project.create_date),
                    project.description
                    ])) for project in projects],
    ]
    if len(table_values) > ROW_COUNT:
        table_values = table_values[:ROW_COUNT]
    return (await wrapper_services.as_service_account(
        (await wrapper_services.discover(
            'sheets', 'v4'
        )).spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{ROW_COUNT}C{COLUMN_COUNT}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    ))
