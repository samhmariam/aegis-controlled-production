"""Typed domain errors. Every one maps to a stable error_code at the HTTP boundary."""

from __future__ import annotations


class AegisError(Exception):
    """Base for every AEGIS domain error. Carries a stable machine-readable code."""

    error_code = "internal_error"


class UnsafeDestinationError(AegisError):
    """The configured database destination is not a writable demo destination."""

    error_code = "unsafe_destination"


class SeedConflictError(AegisError):
    """A fixture row exists with different content than the authoritative fixture."""

    error_code = "seed_conflict"


class IdentityInvalidError(AegisError):
    """The credential is absent, unknown, malformed or expired."""

    error_code = "identity_invalid"


class ClaimNotAccessibleError(AegisError):
    """The claim is not accessible to this principal.

    Deliberately carries no detail. This is the single response for wrong tenant, unentitled
    claim, missing scope and nonexistent claim, so the caller cannot use it as an existence
    oracle. It equalises response content, not response timing.
    """

    error_code = "claim_not_accessible"


class PolicyVersionUnavailableError(AegisError):
    """No usable policy version applies to the claim. Never resolved by substitution."""

    def __init__(self, error_code: str, policy_id: str) -> None:
        super().__init__(error_code)
        self.error_code = error_code
        self.policy_id = policy_id
