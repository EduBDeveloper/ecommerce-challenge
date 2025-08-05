from fastapi import Depends, Header, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import get_user_by_username, get_api_key
from app.models import User, SessionLocal
from collections.abc import AsyncGenerator 
from fastapi.security import OAuth2PasswordBearer


# Clave secreta y algoritmo para firmar JWT
SECRET_KEY = "supersecreto"  # En producción, usar una clave más robusta desde entorno
ALGORITHM = "HS256"


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provee una sesión asíncrona de base de datos para inyección de dependencias.
    """
    async with SessionLocal() as session:
        yield session


async def get_current_user(token: str, db: AsyncSession) -> User:
    """
    Decodifica y valida el JWT recibido. Retorna el usuario autenticado.
    Lanza HTTPException si el token es inválido o el usuario no existe.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user_dep(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    return await get_current_user(token, db)


async def verify_api_key(
    x_api_key: str = Header(..., alias="X-API-Key"),
    db: AsyncSession = Depends(get_db)
):
    """
    Verifica la validez de la API Key enviada en el header X-API-Key.
    Lanza HTTPException si no es válida.
    """
    api_key = await get_api_key(db, x_api_key)
    if not api_key:
        raise HTTPException(status_code=403, detail="API Key inválida")
