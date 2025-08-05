from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, crud
from app.dependencies import get_db, get_current_user_dep, verify_api_key
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter()

# Crear cliente (protegido)
@router.post(
    "/",
    response_model=schemas.CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer(
    customer_in: schemas.CustomerCreate,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),  
    _=Depends(get_current_user_dep),
    _2=Depends(verify_api_key)
):
    """
    Crea un nuevo cliente en el sistema.

    Requiere autenticación y una API Key. 
    
    Puedes autorizar el acceso haciendo clic en el ícono del candado (arriba a la derecha)
    o en el botón "Authorize" al inicio de esta página (Username - Password).
    """
    customer = await crud.create_customer(db, customer_in)
    return customer


# Obtener cliente por ID (público)
@router.get("/{customer_id}", response_model=schemas.CustomerResponse)
async def get_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    """
    Obtiene información de un cliente por su ID.

    No requiere autenticación.
    """
    customer = await crud.get_customer_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return customer
