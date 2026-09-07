"""Application factory and the stable error envelope."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from aegis.api.routes import router
from aegis.errors import (
    AegisError,
    ClaimNotAccessibleError,
    IdentityInvalidError,
    PolicyVersionUnavailableError,
)


def _validation_handler(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, RequestValidationError):
        raise exc
    details = [
        {"field": ".".join(str(part) for part in err["loc"][1:]) or "body", "code": err["type"]}
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"error_code": "claim_schema_invalid", "details": details},
    )


_STATUS_BY_ERROR: dict[type[AegisError], int] = {
    IdentityInvalidError: 401,
    ClaimNotAccessibleError: 404,
    PolicyVersionUnavailableError: 409,
}


def _domain_handler(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, AegisError):
        raise exc
    status = _STATUS_BY_ERROR.get(type(exc), 500)
    # error_code only. No exception text: a SQLite path or table name in a body is a leak.
    return JSONResponse(
        status_code=status, content={"error_code": exc.error_code, "details": []}
    )



def create_app() -> FastAPI:
    app = FastAPI(title="AEGIS", version="0.1.0")
    app.include_router(router)
    app.add_exception_handler(RequestValidationError, _validation_handler)

    for error_type in _STATUS_BY_ERROR:
        app.add_exception_handler(error_type, _domain_handler)

    return app


app = create_app()
