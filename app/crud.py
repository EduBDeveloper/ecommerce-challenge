from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert
from sqlalchemy.orm import selectinload
from app import models, schemas
from typing import List
from passlib.context import CryptContext
import uuid
from app.queue import publish_order_created
from fastapi import HTTPException


#Hasher para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# AUTH 

def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt."""
    return pwd_context.hash(password)


async def verify_user_password(db_user: models.User, plain_password: str) -> bool:
    try:
        if not db_user.hashed_password:
            return False
        return pwd_context.verify(plain_password, db_user.hashed_password)
    except Exception as e:
        print("Error al verificar contraseña:", e)
        return False
    
#  USERS 

async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    """Crea un nuevo usuario en la base de datos."""
    hashed_pw = hash_password(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
    
async def get_user_by_username(db: AsyncSession, username: str) -> models.User | None:
    """Obtiene un usuario por su nombre de usuario."""
    result = await db.execute(select(models.User).where(models.User.username == username))
    return result.scalars().first()
   
async def get_user_by_id(db: AsyncSession, user_id: int) -> models.User | None:
    """Obtiene un usuario por su ID."""
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalars().first()
    
#  API KEYS 

async def create_api_key(db: AsyncSession, user_id: int) -> models.ApiKey:
    """Genera una nueva API Key para un usuario."""
    key = str(uuid.uuid4())
    api_key = models.ApiKey(key=key, user_id=user_id)
    db.add(api_key)
    await db.commit()
    await db.refresh(api_key)
    return api_key
    
async def get_api_key(db: AsyncSession, key: str) -> models.ApiKey | None:
    """Obtiene una API Key a partir de su valor."""
    result = await db.execute(select(models.ApiKey).where(models.ApiKey.key == key))
    return result.scalars().first()
   
#  CUSTOMERS

async def create_customer(db: AsyncSession, customer: schemas.CustomerCreate) -> models.Customer:
    """Crea un nuevo cliente."""

    # 1. Verificar si ya existe un cliente con el mismo email
    result = await db.execute(select(models.Customer).where(models.Customer.email == customer.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Ya existe un cliente con ese email.")

    # 2. (Opcional) Normalizar email (evita duplicados por mayúsculas o espacios)
    customer.email = customer.email.strip().lower()

    # 3. (Opcional) Validar nombre vacío o con caracteres inválidos (ya lo hacés probablemente en el schema)
    # Pero por seguridad podrías limpiar el nombre:
    customer.full_name = customer.full_name.strip()

    # Crear cliente
    new_customer = models.Customer(**customer.dict())
    db.add(new_customer)
    await db.commit()
    await db.refresh(new_customer)
    return new_customer
    
async def get_customer_by_id(db: AsyncSession, customer_id: int) -> models.Customer | None:
    """Obtiene un cliente por su ID."""
    result = await db.execute(select(models.Customer).where(models.Customer.id == customer_id))
    return result.scalars().first()
 
#  PRODUCTS 

async def create_product(db: AsyncSession, product: schemas.ProductCreate) -> models.Product:
    """Crea un nuevo producto."""
     # Verificar si ya existe un producto con ese nombre
    existing = await db.execute(select(models.Product).where(models.Product.name == product.name))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="Ya existe un producto con ese nombre.")
    new_product = models.Product(**product.dict())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product
    
async def list_products(db: AsyncSession) -> List[models.Product]:
    """Lista todos los productos disponibles."""
    result = await db.execute(select(models.Product))
    return result.scalars().all()
    
#  ORDERS 

async def create_order(db: AsyncSession, order: schemas.OrderCreate) -> models.Order:
    """
    Crea un nuevo pedido y publica un mensaje en RabbitMQ.

    Args:
        db (AsyncSession): Sesión de base de datos.
        order (OrderCreate): Datos del pedido.

    Returns:
        Order: Pedido creado.
    """
    new_order = models.Order(customer_id=order.customer_id)
    db.add(new_order)
    await db.flush()  

    items = [
        models.OrderItem(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity)
        for item in order.items
    ]
    db.add_all(items)

    await db.commit()

    #Solución al error MissingGreenlet
    await db.refresh(new_order, attribute_names=["items"])

    #Publicar en RabbitMQ
    await publish_order_created({
        "order_id": new_order.id,
        "customer_id": new_order.customer_id,
        "items": [
            {"product_id": item.product_id, "quantity": item.quantity}
            for item in order.items
        ]
    })

    return new_order

async def get_order_by_id(db: AsyncSession, order_id: int) -> models.Order | None:
    """Obtiene un pedido por su ID, incluyendo los ítems."""
    result = await db.execute(
        select(models.Order)
        .options(selectinload(models.Order.items))  
        .where(models.Order.id == order_id)
    )
    return result.scalars().first()
