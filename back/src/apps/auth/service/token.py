import jwt
import time
from typing import Optional

from ....core.config import settings
from ..model.domain.token import TokenData
from ..exceptions import token_credential_exception
from ..constants import TokenType


async def create_access_token(
        user_id: str,
        scopes: list[str],
        expires_in: int = settings.access_token_expire_seconds,
) -> (str, TokenType):
    # Create Access Token
    init_time = int(time.time())
    to_encode = {
        "user_id": user_id,
        "token_type": TokenType.BEARER,
        "scopes": scopes,
        "created_at": init_time,
    }
    expire = init_time + expires_in
    to_encode.update({"expire_at": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=settings.private_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt, TokenType.BEARER


async def decode_token(token: str) -> Optional[TokenData]:
    # Decode Token
    token_data = None

    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.public_key,
            algorithms=[settings.jwt_algorithm],
        )

        token_data = TokenData(
            user_id=payload.get("user_id"),
            token_type=payload.get("token_type"),
            scopes=payload.get("scopes"),
            created_at=payload.get("created_at"),
            expire_at=payload.get("expire_at"),
        )

    except jwt.PyJWTError as err:
        raise err
    except Exception as err:
        print(err)
        raise Exception("Could not validate credentials")
    finally:
        return token_data
