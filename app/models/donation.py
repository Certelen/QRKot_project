from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import DateInvestModel


class Donation(DateInvestModel):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)

    def __repr__(self):
        return (f'Пожертвование c комментарием {self.comment} '
                f'{super().__repr__()}')
