"""
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .core.config import settings
from .core.database import Base, engine

from .main import create_app

from .route import api_router

Base.metadata.create_all(bind=engine)
app = create_app()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(exc)
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(exc)
    return PlainTextResponse(str(exc), status_code=400)

app.include_router(api_router, prefix=f"{settings.api_version_prefix}")
