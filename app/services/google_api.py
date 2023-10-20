from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
ROW_COUNT = 100
COLUMN_COUNT = 3

SPREADSHEET_BODY = dict(
    properties=dict(
        title='Отчет закрытых проектов QRCat',
        locale='ru_RU',
    ),
    sheets=[dict(
        properties=dict(
            sheetType='GRID',
            sheetId=0,
            title='Лист1',
            gridProperties=dict(
                rowCount=ROW_COUNT,
                columnCount=COLUMN_COUNT
            )
        )
    )]
)

SPREADSHEET_TABLE = [
    ['Отчет от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    spreadsheets_copy = deepcopy(SPREADSHEET_BODY)
    (spreadsheets_copy
     ['properties']
     ['title']) = ('Отчет закрытых проектов QRCat от ' +
                   datetime.now().strftime(FORMAT))
    spreadsheet = (await wrapper_services.as_service_account(
        (await wrapper_services.discover(
            'sheets', 'v4'
        )).spreadsheets.create(json=spreadsheets_copy)
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
            fields="id")
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle,
        projects: list,
) -> None:
    max_column = 0
    spreadsheets_copy = deepcopy(SPREADSHEET_TABLE)
    spreadsheets_copy[0][1] = datetime.now().strftime(
        FORMAT)
    table_values = [
        *spreadsheets_copy,
        *[
            list(map(str, [
                project.name,
                str(project.close_date - project.create_date),
                project.description
            ]))
            for project in sorted(
                projects,
                key=lambda project: project.create_date - project.close_date,
                reverse=True
            )
        ],
    ]
    table_values_count = len(table_values)
    for table_value in table_values:
        max_column = max(len(table_value), max_column)
    if max_column > COLUMN_COUNT:
        raise ValueError(f'Длинна данных ({max_column}) '
                         f'больше колонок таблицы({COLUMN_COUNT})')
    if table_values_count > ROW_COUNT:
        raise ValueError(f'Количество данных ({table_values_count}) '
                         f'больше колонок таблицы({ROW_COUNT})')
    return (await wrapper_services.as_service_account(
        (await wrapper_services.discover(
            'sheets', 'v4'
        )).spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{table_values_count}C{max_column}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    ))
