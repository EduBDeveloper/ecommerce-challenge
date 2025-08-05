from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, crud, models
from app.dependencies import get_db

router = APIRouter()

#  REGISTRO DE USUARIO 
@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Registra un nuevo usuario con credenciales.

    No requiere autenticación.
    """
    db_user = await crud.get_user_by_username(db, user_in.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    
    user = await crud.create_user(db, user_in)
    return user
    
#  GENERAR API KEY 
@router.post("/{user_id}/api-key", response_model=schemas.ApiKeyResponse)
async def generate_api_key(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Genera una nueva API Key para un usuario existente.
    """
    user = await crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return await crud.create_api_key(db, user_id)
    