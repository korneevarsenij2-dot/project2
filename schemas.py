from pydantic import BaseModel, Field, EmailStr, field_validator

class UserRegisterSchema(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=6)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class  SupercarResponseSchema(BaseModel):
    id: int
    title: str
    price: int
    model_config = {"from_attributes": True}

class BikeResponseSchema(BaseModel):
    id: int
    title: str
    price: int
    model_config = {"from_attributes": True}

class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    balance: int
    supercars: list[SupercarResponseSchema] = []
    bikes: list[BikeResponseSchema] = []
    model_config = {"from_attributes": True}

class BuySupercarSchema(BaseModel):
    supercar_id: int = Field(gt=0)

class BuyBikeSchema(BaseModel):
    bike_id: int = Field(gt=0)

