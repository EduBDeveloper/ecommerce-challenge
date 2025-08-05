from pydantic import BaseModel, EmailStr, Field, validator
from typing import List
from datetime import datetime
from pydantic import field_validator
# CUSTOMER

class CustomerCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=100, description="Nombre completo del cliente")
    email: EmailStr

    @field_validator('full_name')
    def name_must_be_alpha(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError("El nombre completo solo puede contener letras y espacios")
        return v


class CustomerResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True


# USER 
class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str):
        if not v or len(v.strip()) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres.")
        if not v.isalnum():
            raise ValueError("El nombre de usuario solo puede contener letras y números.")
        return v.strip()

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str):
        if not v or len(v.strip()) < 3:
            raise ValueError("La contraseña debe tener al menos 3 caracteres.")
        if " " in v:
            raise ValueError("La contraseña no debe contener espacios.")
        return v.strip()


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# API KEY 

class ApiKeyResponse(BaseModel):
    id: int
    key: str

    class Config:
        from_attributes = True


# PRODUCT

from pydantic import BaseModel, field_validator

class ProductCreate(BaseModel):
    name: str
    price: float

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        if len(v.strip()) > 100:
            raise ValueError("El nombre del producto no puede tener más de 100 caracteres.")
        if not v.replace(" ", "").isalnum():
            raise ValueError("El nombre del producto solo puede contener letras, números y espacios.")
        return v.strip()

    @field_validator('price')
    @classmethod
    def validate_price(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("El precio del producto debe ser mayor a 0.")
        return v



class ProductResponse(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True


# ORDER ITEM

class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0, description="ID válido del producto")
    quantity: int = Field(..., gt=0, description="Cantidad debe ser mayor a 0")

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


# ORDER
from pydantic import BaseModel, Field, field_validator
from typing import List

class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]

    @field_validator("customer_id")
    @classmethod
    def validate_customer_id(cls, v):
        if v <= 0:
            raise ValueError("Debe proporcionar un ID válido del cliente.")
        return v

    @field_validator("items")
    @classmethod
    def validate_items(cls, v: List[OrderItemCreate]) -> List[OrderItemCreate]:
        if not v or len(v) == 0:
            raise ValueError("Debe contener al menos un ítem en la orden.")
        product_ids = [item.product_id for item in v]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError("No se permiten productos repetidos en los ítems de la orden.")
        return v



class OrderResponse(BaseModel):
    id: int
    customer_id: int
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
