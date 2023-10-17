from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator
from typing_extensions import Annotated

from app.core.config import MAX_SYM_NAME


class ProjectCreate(BaseModel):
    name: str
    description: str
    full_amount: Annotated[int, Field(gt=0)]

    @validator('name')
    def name_cannot_be_null(cls, value) -> str:
        """Проверка: Поле имени не пустое"""
        if value is None or not value:
            raise ValueError('Имя не может быть пустым!')
        return value

    @validator('name')
    def name_cannot_be_big(cls, value) -> str:
        """Проверка: Имя не больше 100 символов"""
        if len(value) > MAX_SYM_NAME:
            raise ValueError('Имя не может быть больше 100 символов!')
        return value

    @validator('description')
    def description_cannot_be_null(cls, value) -> str:
        """Проверка: Поле описания не пустое"""
        if value is None or not value:
            raise ValueError('Описание не может быть пустым!')
        return value


class ProjectUpdate(ProjectCreate):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[Annotated[int, Field(gt=0)]]

    class Config:
        extra = Extra.forbid


class ProjectDB(ProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
