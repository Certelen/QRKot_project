from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud, project_crud
from app.models import Donation, User
from app.schemas.donation import DonationAllDB, DonationCreate, DonationDB
from app.services.invest import new_invest

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
        donation: DonationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
) -> Donation:
    new_donation = await donation_crud.create(session, donation, False, user)
    await donation_crud.save_session(
        session,
        new_donation,
        new_invest(new_donation, await project_crud.get_open(session))
    )
    return new_donation


@router.get('/my',
            response_model=list[DonationDB],
            response_model_exclude_none=True)
async def get_user_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
) -> list[Donation]:
    donations = await donation_crud.get_user_donations(user, session)
    return donations


@router.get('/',
            response_model=list[DonationAllDB],
            response_model_exclude_none=True,
            dependencies=[Depends(current_superuser)],)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
) -> list[Donation]:
    donations = await donation_crud.get_multi(session)
    return donations
