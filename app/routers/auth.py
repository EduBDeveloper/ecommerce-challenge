# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import get_db
from app import crud, auth as auth_utils
from datetime import timedelta
from app.settings import settings
import traceback

router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Inicia sesión con nombre de usuario y contraseña.
    Retorna un JWT válido para autenticación en los endpoints protegidos.
    """
    try:
        print("📥 Login recibido")
        print("👤 Username:", form_data.username)
        # ⚠️ En producción evita loguear contraseñas en texto claro
        print("🔑 Password:", form_data.password)

        user = await crud.get_user_by_username(db, form_data.username)

        if user:
            print("✅ Usuario encontrado:", user.username)
        else:
            print("❌ Usuario no encontrado")

        password_ok = False
        if user:
            password_ok = await crud.verify_user_password(user, form_data.password)
            print("🔐 ¿Contraseña válida?", password_ok)

        if not user or not password_ok:
            # No será atrapado por el except general
            raise HTTPException(status_code=400, detail="Credenciales inválidas")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = auth_utils.create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )

        print("✅ Token generado")
        return {"access_token": token, "token_type": "bearer"}

    except HTTPException:
        # Las excepciones intencionadas de 400 pasan tal cual
        raise
    except Exception as e:
        print("🔥 ERROR INTERNO EN LOGIN:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error interno")
