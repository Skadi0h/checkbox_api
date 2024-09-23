import uuid
from datetime import datetime, timedelta
from typing import Any

import jwt

from fastapi import HTTPException
from checkbox_api.config import JWT_CONFIG


def create_access_token(
        *,
        user_id: uuid.UUID,
        expires_delta: timedelta | None = None
) -> str:
    to_encode = {
        'user_id': str(user_id)
    }
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=JWT_CONFIG.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_CONFIG.secret_key, algorithm=JWT_CONFIG.algorithm)
    return encoded_jwt


def decode_access_token(*, token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, JWT_CONFIG.secret_key, algorithms=[JWT_CONFIG.algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

