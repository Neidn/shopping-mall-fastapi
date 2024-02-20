"""
Error handlers for the application
"""
from typing import Union

from fastapi import status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition

from pydantic import ValidationError

from starlette.requests import Request
from starlette.types import ExceptionHandler
from starlette.responses import JSONResponse

validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
    }
}


async def http_exception_handler(_: Request, exc: HTTPException) -> ExceptionHandler:
    """ http exception handling """
    # return JSONResponse(
    #     {"errors": [exc.detail]},
    #     status_code=exc.status_code,
    # )
    return ExceptionHandler(
        exc.status_code,
        detail=exc.detail,
    )


async def validation_exception_handler(_: Request,
                                       exc: Union[RequestValidationError, ValidationError]) -> ExceptionHandler:
    """ client request exception handling """
    # return JSONResponse(
    #     {"errors": exc.errors()},
    #     status_code=status.HTTP_400_BAD_REQUEST,
    # )

    return ExceptionHandler(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=exc.errors(),
    )
