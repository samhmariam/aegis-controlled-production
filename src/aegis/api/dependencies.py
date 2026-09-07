"""Request-scoped wiring. The principal is derived here and nowhere else."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, Header

from aegis.config import Settings, get_settings
from aegis.context.service import ContextService
from aegis.errors import IdentityInvalidError
from aegis.identity.demo_provider import DemoIdentityProvider
from aegis.identity.principal import Principal
from aegis.persistence.connection import connect
from aegis.persistence.policy_repository import PolicyRepository

BEARER = "bearer"


def get_connection(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Iterator[sqlite3.Connection]:
    conn = connect(settings.demo_database_path, read_only=True)
    try:
        yield conn
    finally:
        conn.close()


def current_principal(
    conn: Annotated[sqlite3.Connection, Depends(get_connection)],
    authorization: Annotated[str | None, Header()] = None,
) -> Principal:
    """Tenant scope originates here, from the credential. Nothing else may set it."""
    if authorization is None:
        raise IdentityInvalidError("missing Authorization header")
    scheme, _, credential = authorization.partition(" ")
    if scheme.lower() != BEARER or not credential:
        raise IdentityInvalidError("expected a bearer credential")
    return DemoIdentityProvider(conn).authenticate(credential.strip())


def get_context_service(
    conn: Annotated[sqlite3.Connection, Depends(get_connection)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> ContextService:
    return ContextService(
        PolicyRepository(conn),
        max_clauses=settings.retrieval_max_clauses,
        excerpt_chars=settings.retrieval_excerpt_chars,
    )
