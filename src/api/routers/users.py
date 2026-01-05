from datetime import datetime, timedelta, timezone

import anyio
from fastapi import APIRouter, HTTPException, Depends
from google.auth.transport import requests as grequests
from google.oauth2 import id_token
from starlette.requests import Request
from starlette.responses import Response

from src.api.depends import get_user_repository, get_uow, get_current_user
from src.api.schemas.profiles import ProfileRead
from src.api.schemas.users import TokenSchema, UserRead
from src.app.uow import UoW
from src.repositories import UserRepository
from src.services.jwt_service import encode_jwt

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/auth")
async def login_via_google(
        request: Request,
        response: Response,
        data: TokenSchema,
        user_repository: UserRepository = Depends(get_user_repository),
        uow: UoW = Depends(get_uow),
):
    settings = request.app.state.settings

    try:
        idinfo = await anyio.to_thread.run_sync(
            id_token.verify_oauth2_token,
            data.token,
            grequests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google Token")

    user_email = idinfo["email"]
    user_name = idinfo.get("name")

    async with uow:
        db_user = await user_repository.get_by_email(user_email)
        if not db_user:
            db_user = await user_repository.create(email=user_email, fullname=user_name)

    now = datetime.now(timezone.utc)
    access_token = await encode_jwt(
        {"id": db_user.id, "exp": int((now + timedelta(minutes=5)).timestamp())},
        key=settings.JWT_ACCESS_TOKEN_SECRET_KEY,
    )
    refresh_token = await encode_jwt(
        {"id": db_user.id, "exp": int((now + timedelta(days=7)).timestamp())},
        key=settings.JWT_REFRESH_TOKEN_SECRET_KEY,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
        httponly=True,
        path="/",
    )

    print(access_token)

    return {"name": user_name, "access_token": access_token}


@router.get("/me", response_model=UserRead)
async def get_me(
        current_user=Depends(get_current_user),
):
    return UserRead(
        id=current_user.id,
        email=current_user.email,
        fullname=current_user.fullname,
        profile=ProfileRead.from_orm(current_user.profile) if current_user.profile else None,
    )
