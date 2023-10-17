from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from sqlalchemy import select
from app.models.base import DateInvestModel


class CRUDProject(CRUDBase):

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> Optional[DateInvestModel]:
        close_projects = await session.execute(
            select(self.model).where(
                self.model.fully_invested == 1
            )
        )
        return close_projects.scalars().all()


project_crud = CRUDProject(CharityProject)
