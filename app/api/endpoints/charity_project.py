from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_amount_more_invest,
                                check_project_name_duplicate,
                                check_project_open, check_project_whith_invest)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import donation_crud, project_crud
from app.models import CharityProject
from app.schemas.charity_project import ProjectCreate, ProjectDB, ProjectUpdate
from app.services.invest import new_invest

router = APIRouter()


@router.post(
    '/',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def create_new_project(
        project: ProjectCreate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    await check_project_name_duplicate(session, project)
    new_project = await project_crud.create(session, project, False)
    await project_crud.save_session(
        session,
        new_project,
        new_invest(new_project, await donation_crud.get_open(session))
    )
    print(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[ProjectDB],
    response_model_exclude_none=True,
)
async def get_all_project(
        session: AsyncSession = Depends(get_async_session),
) -> list[CharityProject]:
    all_project = await project_crud.get_multi(session)
    return all_project


@router.patch(
    '/{project_id}',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
        project_id: int,
        obj_in: ProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    project = await project_crud.get(session, project_id)
    check_project_open(project)
    await check_project_name_duplicate(session, obj_in)
    if obj_in.full_amount is not None:
        check_amount_more_invest(obj_in, project)
        if project.invested_amount == obj_in.full_amount:
            project.invested_amount = obj_in.full_amount
            project.fully_amount = True
            project.close_date = datetime.today()
    project = await project_crud.update(
        session, project, obj_in,
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    project = await project_crud.get(session, project_id)
    check_project_whith_invest(project)
    check_project_open(project)
    project = await project_crud.remove(session, project)
    return project
