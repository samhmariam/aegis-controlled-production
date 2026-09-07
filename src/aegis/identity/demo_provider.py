"""NON-PRODUCTION identity. Maps opaque local demo credentials to Principal contracts.

This is not an identity provider. It performs no issuance, rotation, revocation, audience
binding or token validation. It exists so that business code consumes only the Principal
contract, and so that Day 2 can prove authorization without inventing crypto.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import sqlite3
from datetime import UTC, datetime, timedelta

from aegis.errors import IdentityInvalidError
from aegis.identity.principal import AuthenticationMethod, Principal, PrincipalType


def credential_digest(credential: str) -> str:
    return f"sha256:{hashlib.sha256(credential.encode('utf-8')).hexdigest()}"


class DemoIdentityProvider:
    """Resolves a demo credential to a Principal. Never logs or echoes the credential."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def authenticate(self, credential: str, *, now: datetime | None = None) -> Principal:
        if not credential:
            raise IdentityInvalidError("no credential supplied")
        moment = now or datetime.now(UTC)
        digest = credential_digest(credential)

        row = self._conn.execute(
            "SELECT principal_id, tenant_id, principal_type, scopes, roles,"
            " credential_sha256, lifetime_seconds"
            " FROM principals WHERE credential_sha256 = ?",
            (digest,),
        ).fetchone()
        if row is None or not hmac.compare_digest(str(row["credential_sha256"]), digest):
            raise IdentityInvalidError("credential is not recognised")

        return Principal(
            principal_id=str(row["principal_id"]),
            principal_type=PrincipalType(str(row["principal_type"])),
            tenant_id=str(row["tenant_id"]),
            scopes=frozenset(json.loads(str(row["scopes"]))),
            roles=frozenset(json.loads(str(row["roles"]))),
            authenticated_at=moment,
            expires_at=moment + timedelta(seconds=int(row["lifetime_seconds"])),
            authentication_method=AuthenticationMethod.DEMO_TOKEN,
        )
