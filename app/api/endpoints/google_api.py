from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.services.google_api import (
    spreadsheets_create, set_user_permissions, spreadsheets_update_value)

from app.crud import project_crud

GOOGLE_SPREADSHEETS_LINK = 'https://docs.google.com/spreadsheets/d/'


router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

):
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(
        spreadsheetid,
        wrapper_services,
        await project_crud.get_projects_by_completion_rate(session)
    )
    return f'Ссылка на документ: {GOOGLE_SPREADSHEETS_LINK + spreadsheetid}'
