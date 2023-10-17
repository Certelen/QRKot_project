from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from typing_extensions import Annotated


class DonationCreate(BaseModel):
    full_amount: Annotated[int, Field(gt=0)]
    comment: Optional[str]


class DonationDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationAllDB(DonationDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
