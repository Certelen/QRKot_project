from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.base import DateInvestModel
from app.models.charity_project import CharityProject


class CRUDProject(CRUDBase):

    async def get_projects_by_completion_rate(
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
        return sorted(
            close_projects.scalars().all(),
            key=lambda project: project.create_date - project.close_date,
            reverse=True)


project_crud = CRUDProject(CharityProject)
