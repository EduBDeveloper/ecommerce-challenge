from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, crud
from app.dependencies import get_db, get_current_user_dep, verify_api_key
from typing import List

router = APIRouter()

#Crear pedido (protegido)
@router.post(
    "/",
    response_model=schemas.OrderResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user_dep), Depends(verify_api_key)]
)
async def create_order(order_in: schemas.OrderCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea un nuevo pedido con productos asociados.

    Requiere autenticación y una API Key. 
    
    Puedes autorizar el acceso haciendo clic en el ícono del candado (arriba a la derecha)
    o en el botón "Authorize" al inicio de esta página (Username - Password).
    """
    order = await crud.create_order(db, order_in)
    return order
    

#Obtener pedido por ID (público)
@router.get("/{order_id}", response_model=schemas.OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    """
    Obtiene un pedido existente por su ID.

    No requiere autenticación.
    """
    order = await crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order
    