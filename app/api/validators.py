from http import HTTPStatus
from typing import Union

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.schemas.charity_project import ProjectCreate, ProjectUpdate


async def check_project_name_duplicate(
        session: AsyncSession,
        project: Union[ProjectCreate, ProjectUpdate]
) -> None:
    """Проверка: Проект с таким именем не существует в БД."""
    db_project = await session.execute(
        select(CharityProject).where(
            CharityProject.name == project.name
        )
    )
    db_project = db_project.scalars().first()
    if db_project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


def check_project_open(
        project: CharityProject
) -> None:
    """Проверка: Удаляемый проект не закрыт."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )


def check_project_whith_invest(
        project: CharityProject
) -> None:
    """Проверка: Удаляемый проект без внесенных средств."""
    if project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


def check_amount_more_invest(
        obj_in: ProjectUpdate,
        project: CharityProject
) -> None:
    """
    Проверка: Цель изменяемого проекта больше,
    чем текущие внесеные средства.
    """
    if project.invested_amount > obj_in.full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Требуемая сумма не может быть меньше уже имеющейся'
        )
