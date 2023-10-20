from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.base import DateInvestModel
from app.models.charity_project import CharityProject


class CRUDProject(CRUDBase):

    async def get_close_projects(
            self,
            session: AsyncSession,
    ) -> Optional[list[DateInvestModel]]:
        close_projects = await session.execute(
            select(
                self.model
            ).where(
                self.model.fully_invested == 1
            )
        )
        return close_projects.scalars().all()


project_crud = CRUDProject(CharityProject)
