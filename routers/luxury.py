from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database import AsyncSessionLocal, redis_client
from models import User, Supercar, Bike
from schemas import UserResponseSchema, BuySupercarSchema, BuyBikeSchema
from security import get_current_user
from services.external_api import get_usd_rate

router = APIRouter(prefix="/luxury", tags=["Покупка Luxury Технику"])

# 1. живой пересчет цены тачки в доллары через httpx
@router.get("/price_usd/{price_rub}")
async def get_price_in_usd(price_rub: int):
    usd_rate = await get_usd_rate()
    price_usd = round(price_rub / usd_rate, 2)
    return {
        "price_rub": price_rub,
        "current_usd_rate": usd_rate,
        "price_usd": f"{price_usd}"
    }


# 1. ПОКУПКА СУПЕРКАРА
@router.post("buy_supercar", response_model=UserResponseSchema)
async def supercar(
    supercar_data: BuySupercarSchema,
    current_user: User = Depends(get_current_user)):
    async with AsyncSessionLocal() as session:
        user_res = await session.execute(select(User).filter_by(id=current_user.id).options(
            selectinload(User.supercars),
            selectinload(User.bikes)
        )
        )
        user = user_res.scalars().first()
        car_res = await session.execute(select(Supercar).filter_by(id=supercar_data.supercar_id))
        car = car_res.scalars().first()
        if not car:
            raise HTTPException(status_code=404, detail="не найден суперкар")
        if user.balance < car.price:
            raise HTTPException(status_code=400, detail="недостаточно средств")
        user.balance -= car.price
        car.user_id = user.id
        await session.commit()
        await session.refresh(user)
        cache_key = f"user_profile:{user.id}"
        await redis_client.delete(cache_key)
        return user

@router.post("buy_bike", response_model=UserResponseSchema)
async def bike(
    bike_data: BuyBikeSchema,
    current_user: User = Depends(get_current_user)):
    async with AsyncSessionLocal() as session:
        user_res = await session.execute(select(User).filter_by(id=current_user.id).options(
            selectinload(User.supercars),
            selectinload(User.bikes)
        )
        )
        user = user_res.scalars().first()
        car_res = await session.execute(select(Bike).filter_by(id=bike_data.bike_id))
        car = car_res.scalars().first()
        if not car:
            raise HTTPException(status_code=404, detail="не найден")
        if user.balance < car.price:
            raise HTTPException(status_code=400, detail="недостаточно средств")
        user.balance -= car.price
        car.user_id = user.id
        await session.commit()
        await session.refresh(user)
        cache_key=f"user_profile:{user.id}"
        await redis_client.delete(cache_key)
        return user
