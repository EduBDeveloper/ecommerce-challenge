import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.routers.auth import login
from app import crud, auth as auth_utils
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock
import jose

@pytest.mark.asyncio
async def test_login_success(monkeypatch):
    fake_user = type("U", (), {"username": "u", "hashed_password": "hashed"})()
    monkeypatch.setattr(crud, "get_user_by_username", AsyncMock(return_value=fake_user))
    monkeypatch.setattr(crud, "verify_user_password", AsyncMock(return_value=True))
    # Usa el util real para generar el token
    monkeypatch.setattr(auth_utils, "create_access_token", auth_utils.create_access_token)

    form = OAuth2PasswordRequestForm(username="u", password="p", scope="")
    resp = await login(form_data=form, db=AsyncMock())
    assert resp["token_type"] == "bearer"
    payload = jose.jwt.decode(
        resp["access_token"],
        auth_utils.SECRET_KEY,
        algorithms=[auth_utils.ALGORITHM]
    )
    assert payload["sub"] == "u"
    assert "exp" in payload

@pytest.mark.asyncio
async def test_login_invalid_user(monkeypatch):
    monkeypatch.setattr(crud, "get_user_by_username", AsyncMock(return_value=None))
    form = OAuth2PasswordRequestForm(username="x", password="y", scope="")
    with pytest.raises(HTTPException) as e:
        await login(form_data=form, db=AsyncMock())
    assert e.value.status_code == 400

@pytest.mark.asyncio
async def test_login_invalid_password(monkeypatch):
    fake_user = type("U", (), {"username": "u", "hashed_password": "hashed"})()
    monkeypatch.setattr(crud, "get_user_by_username", AsyncMock(return_value=fake_user))
    monkeypatch.setattr(crud, "verify_user_password", AsyncMock(return_value=False))
    form = OAuth2PasswordRequestForm(username="u", password="wrong", scope="")
    with pytest.raises(HTTPException) as e:
        await login(form_data=form, db=AsyncMock())
    assert e.value.status_code == 400
