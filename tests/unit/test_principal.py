from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from aegis.identity.principal import AuthenticationMethod, Principal, PrincipalType

AUTHENTICATED_AT = datetime(2026, 9, 6, 12, 0, tzinfo=UTC)
EXPIRES_AT = datetime(2026, 9, 6, 13, 0, tzinfo=UTC)


def valid_principal_payload() -> dict[str, object]:
    return {
        "principal_id": "principal-example-001",
        "principal_type": "user",
        "tenant_id": "tenant-example-001",
        "scopes": ("claims:read", "claims:submit"),
        "authenticated_at": AUTHENTICATED_AT,
        "expires_at": EXPIRES_AT,
        "authentication_method": "demo_token",
    }


def test_valid_principal_parses() -> None:
    principal = Principal.model_validate(valid_principal_payload())

    assert principal.principal_id == "principal-example-001"
    assert principal.principal_type is PrincipalType.USER
    assert principal.scopes == frozenset({"claims:read", "claims:submit"})
    assert principal.roles == frozenset()
    assert principal.authentication_method is AuthenticationMethod.DEMO_TOKEN


def test_empty_scopes_are_rejected() -> None:
    payload = valid_principal_payload()
    payload["scopes"] = ()

    with pytest.raises(ValidationError, match="scopes"):
        Principal.model_validate(payload)


@pytest.mark.parametrize(
    "expires_at",
    [
        AUTHENTICATED_AT,
        AUTHENTICATED_AT - timedelta(seconds=1),
    ],
)
def test_expires_at_not_after_authenticated_at_is_rejected(expires_at: datetime) -> None:
    payload = valid_principal_payload()
    payload["expires_at"] = expires_at

    with pytest.raises(ValidationError, match="expires_at must be after authenticated_at"):
        Principal.model_validate(payload)


def test_is_expired_before_and_after_expiry() -> None:
    principal = Principal.model_validate(valid_principal_payload())

    assert not principal.is_expired(EXPIRES_AT - timedelta(microseconds=1))
    assert principal.is_expired(EXPIRES_AT)
    assert principal.is_expired(EXPIRES_AT + timedelta(seconds=1))


def test_unknown_principal_type_is_rejected() -> None:
    payload = valid_principal_payload()
    payload["principal_type"] = "service_account"

    with pytest.raises(ValidationError) as exc_info:
        Principal.model_validate(payload)

    assert any(error["type"] == "enum" for error in exc_info.value.errors())
