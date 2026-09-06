"""Application factory and the stable error envelope."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from aegis.api.routes import router


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


def create_app() -> FastAPI:
    app = FastAPI(title="AEGIS", version="0.1.0")
    app.include_router(router)
    app.add_exception_handler(RequestValidationError, _validation_handler)
    return app


app = create_app()
