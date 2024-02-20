from fastapi.exceptions import HTTPException
from starlette import status

from typing import Dict

from fastapi.exceptions import HTTPException
from starlette import status


class UserCredentialException(HTTPException):
    def __init__(self, headers: Dict[str, str] = None) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers=headers,
        )


def token_credential_exception(scope: str) -> Exception:
    msg = f"Bearer token required for {scope}" if scope else "Bearer token required"

    return UserCredentialException(
        headers={"www-authenticate": msg}
    )


FailureSignInException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Incorrect username or password",
)

InactiveUserException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
)

ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="forbidden"
)
TodoNotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND)
