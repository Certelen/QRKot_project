from datetime import datetime

from app.models.base import DateInvestModel


def new_invest(
    target: DateInvestModel,
    sources: list[DateInvestModel],
) -> list[DateInvestModel]:
    """Функция для распределения неинвестированных средств по объектам,
    при создании нового объекта
    """
    now_source = 0
    for source in sources:
        refill = min(source.full_amount - source.invested_amount,
                     target.full_amount - target.invested_amount)
        for invested in source, target:
            invested.invested_amount += refill
            if invested.invested_amount == invested.full_amount:
                invested.fully_invested = True
                invested.close_date = datetime.today()
        now_source += 1
        if target.fully_invested:
            break
    return sources[:now_source]
