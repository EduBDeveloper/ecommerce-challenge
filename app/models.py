from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, declarative_base, validates
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import os

#Conexión a DB
from app.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

#Modelo User con validación
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    api_keys = relationship("ApiKey", back_populates="user")

    @validates("username")
    def validate_username(self, key, value):
        if not value:
            raise ValueError("Username no puede estar vacío.")
        return value

    @validates("hashed_password")
    def validate_password(self, key, value):
        if not value:
            raise ValueError("Password no puede estar vacío.")
        return value

#Modelo API Key
class ApiKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="api_keys")

#Producto con validaciones
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)

    @validates("name")
    def validate_name(self, key, value):
        if not value:
            raise ValueError("El nombre del producto no puede estar vacío.")
        return value

    @validates("price")
    def validate_price(self, key, value):
        if value is None or value < 0:
            raise ValueError("El precio debe ser mayor o igual a 0.")
        return value

#Cliente con validación de email
class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    orders = relationship("Order", back_populates="customer")

    @validates("email")
    def validate_email(self, key, value):
        if not value:
            raise ValueError("El email del cliente no puede estar vacío.")
        return value

#Orden
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")

#Ítem de Orden con validación de cantidad
class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

    @validates("quantity")
    def validate_quantity(self, key, value):
        if value is None or value <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        return value

#Async session getter
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
