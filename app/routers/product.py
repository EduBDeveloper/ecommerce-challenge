from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, crud
from app.dependencies import get_db, get_current_user_dep, verify_api_key
from typing import List
from app.external import get_inventory_for_product
from app.settings import settings

router = APIRouter()

#Crear producto (protegido)
@router.post(
    "/",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user_dep), Depends(verify_api_key)]
)
async def create_product(product_in: schemas.ProductCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea un nuevo producto.

    Requiere autenticación y API Key .
   
    Puedes autorizar el acceso haciendo clic en el ícono del candado (arriba a la derecha)
    o en el botón "Authorize" al inicio de esta página (Username - Password).

    """
    product = await crud.create_product(db, product_in)
    return product
    
#Listar productos (público)
@router.get("/", response_model=List[schemas.ProductResponse])
async def list_products(db: AsyncSession = Depends(get_db)):
    """
    Lista todos los productos disponibles.

    No requiere autenticación.
    """
    return await crud.list_products(db)
    
#Consultar inventario externo
@router.get("/{product_id}")
async def get_inventory(product_id: int):
    """
    Consulta el inventario de un producto desde un servicio externo.

    No requiere autenticación.
    """
    data = await get_inventory_for_product(product_id)
    if not data:
        raise HTTPException(status_code=404, detail="Producto no encontrado en inventario externo")
    return data
   