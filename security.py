import os
import jwt
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from database import AsyncSessionLocal
from models import User
load_dotenv()
SECRET_KEY= os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="невалидный токен")
    except Exception:
        raise HTTPException(status_code=401, detail="токен истек или недействителен")
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User)).filter_by(id=user_id).options(selectinload(User.cars))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="пользователь не найден")
    return user
