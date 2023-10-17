from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base

DEFAULT_INVESTED_AMOUNT = 0


class DateInvestModel(Base):

    def __init__(self, **kwargs):
        if 'invested_amount' not in kwargs:
            kwargs['invested_amount'] = DEFAULT_INVESTED_AMOUNT
        super(DateInvestModel, self).__init__(**kwargs)

    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('full_amount >= invested_amount')
    )
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=DEFAULT_INVESTED_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime)
    close_date = Column(DateTime)

    def __repr__(self):
        return (f'с суммой {self.full_amount} '
                f'из которых использовано {self.invested_amount}, '
                f'{self.create_date=}, {self.close_date=}')
