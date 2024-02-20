"""
main.py
"""
from fastapi.applications import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from .core.exception_handlers import http_exception_handler, validation_exception_handler


def create_app() -> FastAPI:
    """ app factory method """
    app = FastAPI()

    origins = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:8080",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # app.add_exception_handler(HTTPException, http_exception_handler)
    # app.add_exception_handler(RequestValidationError, validation_exception_handler)

    return app
