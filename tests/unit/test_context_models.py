from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from aegis.context.models import ClauseExcerpt, ContextBundle, PolicyClause
from aegis.domain.models import ClaimType

EFFECTIVE_FROM = datetime(2026, 9, 1, 0, 0, tzinfo=UTC)
EFFECTIVE_TO = datetime(2026, 10, 1, 0, 0, tzinfo=UTC)


@pytest.fixture
def valid_clause() -> PolicyClause:
    return PolicyClause.sealed(
        clause_id="clause-collision-001",
        policy_id="policy-motor-001",
        tenant_id="tenant-example-001",
        policy_version="v1",
        line_of_business=ClaimType.MOTOR,
        effective_from=EFFECTIVE_FROM,
        effective_to=EFFECTIVE_TO,
        text="Collision damage is covered subject to the policy excess.",
    )


def valid_bundle_payload(valid_clause: PolicyClause) -> dict[str, object]:
    return {
        "claim_id": "claim-example-001",
        "tenant_id": "tenant-example-001",
        "policy_id": "policy-motor-001",
        "policy_version": "v1",
        "clause_ids": (valid_clause.clause_id,),
        "excerpts": (
            ClauseExcerpt(
                clause_id=valid_clause.clause_id,
                excerpt="Collision damage is covered.",
                source_content_hash=valid_clause.content_hash,
            ),
        ),
        "retrieval_query": "collision damage coverage",
        "retrieved_at": datetime(2026, 9, 6, 12, 0, tzinfo=UTC),
        "limitations": (),
    }


def test_valid_clause_parses(valid_clause: PolicyClause) -> None:
    parsed = PolicyClause.model_validate(valid_clause.model_dump())

    assert parsed == valid_clause


def test_sealed_clause_verifies_against_recomputed_hash(valid_clause: PolicyClause) -> None:
    round_tripped = PolicyClause.model_validate(valid_clause.model_dump())

    assert round_tripped.content_hash == valid_clause.content_hash


def test_tampered_clause_text_fails_hash_check(valid_clause: PolicyClause) -> None:
    payload = valid_clause.model_dump()
    payload["text"] = "Collision damage is not covered."

    with pytest.raises(ValidationError, match="content_hash does not match clause content"):
        PolicyClause.model_validate(payload)


def test_effective_to_before_effective_from_is_rejected(valid_clause: PolicyClause) -> None:
    payload = valid_clause.model_dump()
    payload["effective_to"] = EFFECTIVE_FROM

    with pytest.raises(ValidationError, match="effective_to must be after effective_from"):
        PolicyClause.model_validate(payload)


def test_is_effective_at_boundaries(valid_clause: PolicyClause) -> None:
    open_ended_clause = PolicyClause.sealed(
        clause_id="clause-open-ended-001",
        policy_id="policy-motor-001",
        tenant_id="tenant-example-001",
        policy_version="v1",
        line_of_business=ClaimType.MOTOR,
        effective_from=EFFECTIVE_FROM,
        text="This clause remains effective until replaced.",
    )

    assert valid_clause.is_effective_at(EFFECTIVE_FROM)
    assert valid_clause.is_effective_at(EFFECTIVE_TO - timedelta(microseconds=1))
    assert not valid_clause.is_effective_at(EFFECTIVE_TO)
    assert not valid_clause.is_effective_at(EFFECTIVE_FROM - timedelta(microseconds=1))
    assert open_ended_clause.is_effective_at(EFFECTIVE_FROM + timedelta(days=3650))


@pytest.mark.parametrize(
    ("clause_ids", "excerpt_clause_id"),
    [
        (("clause-collision-001",), "clause-unmatched-001"),
        ((), "clause-collision-001"),
    ],
)
def test_bundle_excerpt_without_matching_clause_id_is_rejected(
    valid_clause: PolicyClause,
    clause_ids: tuple[str, ...],
    excerpt_clause_id: str,
) -> None:
    payload = valid_bundle_payload(valid_clause)
    payload["clause_ids"] = clause_ids
    payload["excerpts"] = (
        ClauseExcerpt(
            clause_id=excerpt_clause_id,
            excerpt="Collision damage is covered.",
            source_content_hash=valid_clause.content_hash,
        ),
    )

    with pytest.raises(ValidationError, match="each declared clause_id needs exactly one excerpt"):
        ContextBundle.model_validate(payload)


def test_bundle_duplicate_clause_ids_are_rejected(valid_clause: PolicyClause) -> None:
    payload = valid_bundle_payload(valid_clause)
    payload["clause_ids"] = (valid_clause.clause_id, valid_clause.clause_id)

    with pytest.raises(ValidationError, match="clause_ids contains duplicates"):
        ContextBundle.model_validate(payload)


def test_empty_bundle_without_limitations_is_rejected(valid_clause: PolicyClause) -> None:
    payload = valid_bundle_payload(valid_clause)
    payload["clause_ids"] = ()
    payload["excerpts"] = ()

    with pytest.raises(
        ValidationError, match="an empty bundle must record why no clause was retrieved"
    ):
        ContextBundle.model_validate(payload)


def test_empty_bundle_with_a_limitation_is_accepted(valid_clause: PolicyClause) -> None:
    payload = valid_bundle_payload(valid_clause)
    payload["clause_ids"] = ()
    payload["excerpts"] = ()
    payload["limitations"] = ("No relevant clause found.",)

    bundle = ContextBundle.model_validate(payload)

    assert bundle.clause_ids == ()
    assert bundle.limitations == ("No relevant clause found.",)


def test_empty_bundle_with_blank_limitation_is_rejected(valid_clause: PolicyClause) -> None:
    payload = valid_bundle_payload(valid_clause)
    payload["clause_ids"] = ()
    payload["excerpts"] = ()
    payload["limitations"] = ("   ",)

    with pytest.raises(ValidationError, match="limitations"):
        ContextBundle.model_validate(payload)
