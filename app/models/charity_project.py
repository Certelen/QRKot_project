from sqlalchemy import Column, String

from app.core.config import MAX_NAME_IN_REPR, MAX_SYM_NAME
from app.models.base import DateInvestModel


class CharityProject(DateInvestModel):
    name = Column(String(MAX_SYM_NAME), unique=True, nullable=False)
    description = Column(String, nullable=False)

    def __repr__(self):
        return f'Проект {self.name[:MAX_NAME_IN_REPR]} {super().__repr__()}'
