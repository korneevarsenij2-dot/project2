import json
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database import AsyncSessionLocal, redis_client
from models import User
from schemas import UserRegisterSchema, UserLoginSchema, UserResponseSchema
from security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Авторизация и Профиль"])

# 1. Регистрация
@router.post("/register", response_model=UserResponseSchema)
async def register(user_data: UserRegisterSchema):
    async with AsyncSessionLocal() as session:
        hashed_pwd = hash_password(user_data.password)
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            balance=user_data.balance,
            hashed_password=hashed_pwd)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
# 2. Логин
@router.post("/login")
async def login(login_data: UserLoginSchema):
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(User).filter_by(email=login_data.email))
        user = res.scalars().first()
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="не верный email или password")
        token = create_access_token(data={"user_id":user.id})
        return {"access_token": token, "token_type": "bearer"}
@router.get("/me")
async def user_profile(current_user: User = Depends(get_current_user)):
    cache_key=f"user_profile:{current_user.id}"
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(User).filter_by(id=current_user.id).options(
            selectinload(User.supercars),
            selectinload(User.bikes)
        )
        )
        user = res.scalars().first()
        user_dict = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "balance": user.balance,
            "supercars": [{"id": s.id, "title": s.title, "price": s.price} for s in user.supercars],
            "bikes": [{"id": b.id, "title": b.title, "price": b.price} for b in user.bikes]
        }
        await redis_client.set(cache_key, json.dumps(user_dict), ex=60)
        return user_dict


