# app/auth.py

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.settings import settings

# Exponemos las constantes para los tests
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

# Configuración JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Hasher de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
