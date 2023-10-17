from datetime import datetime

from aiogoogle import Aiogoogle
from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    spreadsheet_body = {
        'properties': {'title': 'Отчет закрытых проектов QRCat',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 11}}}]
    }
    return (await wrapper_services.as_service_account(
        (await wrapper_services.discover(
            'sheets', 'v4'
        )).spreadsheets.create(json=spreadsheet_body)
    ))['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    await wrapper_services.as_service_account(
        (await wrapper_services.discover('drive', 'v3')).permissions.create(
            fileId=spreadsheetid,
            json={
                'type': 'user',
                'role': 'writer',
                'emailAddress': settings.email
            },
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        wrapper_services: Aiogoogle,
        projects: list,
) -> None:
    table_values = [
        ['Отчет от', datetime.now().strftime(FORMAT)],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        table_values.append([
            project.name,
            str((project.close_date - project.create_date)),
            project.description
        ])
    return (await wrapper_services.as_service_account(
        (await wrapper_services.discover(
            'sheets', 'v4'
        )).spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    ))['spreadsheetId']
