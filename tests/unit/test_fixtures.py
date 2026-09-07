import json
import re
from collections import defaultdict
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from aegis.context.models import PolicyClause
from aegis.domain.models import ClaimSubmission
from aegis.persistence.fixtures import PolicyFixture

SYNTHETIC_DATA_DIR = Path("data/synthetic")
FORBIDDEN = {
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "long_digit_run": r"\b\d{13,19}\b",
    "uk_ni_number": r"\b[A-CEGHJ-PR-TW-Z]{2}\d{6}[A-D]\b",
    "iban": r"\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b",
    "aws_key": r"\bAKIA[0-9A-Z]{16}\b",
    "openai_key": r"\bsk-[A-Za-z0-9]{20,}\b",
    "private_key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
}


@dataclass(frozen=True)
class FixtureData:
    policies: list[dict[str, Any]]
    clauses: list[dict[str, Any]]
    claims: list[dict[str, Any]]
    invalid_claims: list[dict[str, Any]]
    file_contents: dict[Path, str]


@pytest.fixture(scope="module")
def fixture_data() -> FixtureData:
    file_contents = {
        path: path.read_text(encoding="utf-8") for path in SYNTHETIC_DATA_DIR.glob("*.json")
    }
    parsed = {path.name: json.loads(content) for path, content in file_contents.items()}
    assert all(isinstance(value, list) for value in parsed.values())

    return FixtureData(
        policies=parsed["policies.json"],
        clauses=parsed["policy-clauses.json"],
        claims=parsed["claims.json"],
        invalid_claims=parsed["claims-invalid.json"],
        file_contents=file_contents,
    )


def test_all_policies_parse(fixture_data: FixtureData) -> None:
    policies = [PolicyFixture.model_validate(policy) for policy in fixture_data.policies]

    assert len(policies) == len(fixture_data.policies)


def test_all_clauses_parse(fixture_data: FixtureData) -> None:
    clauses = [PolicyClause.model_validate(clause) for clause in fixture_data.clauses]

    assert len(clauses) == len(fixture_data.clauses)


def test_all_valid_claims_parse(fixture_data: FixtureData) -> None:
    claims = [ClaimSubmission.model_validate(claim) for claim in fixture_data.claims]

    assert len(claims) == len(fixture_data.claims)


def test_expected_counts(fixture_data: FixtureData) -> None:
    assert len({policy["tenant_id"] for policy in fixture_data.policies}) == 2
    assert len({policy["policy_id"] for policy in fixture_data.policies}) == 6
    assert len(fixture_data.claims) == 12


@pytest.mark.parametrize("case_index", range(5))
def test_invalid_claims_fail_for_the_stated_reason(
    fixture_data: FixtureData, case_index: int
) -> None:
    case = fixture_data.invalid_claims[case_index]

    with pytest.raises(ValidationError) as exc_info:
        ClaimSubmission.model_validate(case["payload"])

    error = exc_info.value.errors()[0]
    assert error["type"] == case["expected_error"]
    expected_field = case["expected_field"]
    if expected_field:
        assert expected_field in error["loc"]


def test_cross_tenant_policy_reference_is_detected(fixture_data: FixtureData) -> None:
    cross_tenant_case = next(
        case
        for case in fixture_data.invalid_claims
        if case["expected_error"] == "referential_integrity"
    )
    claim = ClaimSubmission.model_validate(cross_tenant_case["payload"])

    assert not any(
        policy["policy_id"] == claim.policy_id and policy["tenant_id"] == claim.tenant_id
        for policy in fixture_data.policies
    )


def test_referential_integrity(fixture_data: FixtureData) -> None:
    policy_versions = {
        (policy["policy_id"], policy["tenant_id"], policy["policy_version"])
        for policy in fixture_data.policies
    }
    policy_owners = {(policy_id, tenant_id) for policy_id, tenant_id, _ in policy_versions}

    for claim_payload in fixture_data.claims:
        claim = ClaimSubmission.model_validate(claim_payload)
        assert (claim.policy_id, claim.tenant_id) in policy_owners

    for clause_payload in fixture_data.clauses:
        clause = PolicyClause.model_validate(clause_payload)
        assert (clause.policy_id, clause.tenant_id, clause.policy_version) in policy_versions


def test_ids_are_unique_per_entity_type(fixture_data: FixtureData) -> None:
    assert len({claim["claim_id"] for claim in fixture_data.claims}) == len(fixture_data.claims)
    policy_versions = {
        (policy["policy_id"], policy["policy_version"]) for policy in fixture_data.policies
    }
    assert len(policy_versions) == len(fixture_data.policies)
    assert len({clause["clause_id"] for clause in fixture_data.clauses}) == len(
        fixture_data.clauses
    )


def test_policy_versions_and_dates_are_coherent(fixture_data: FixtureData) -> None:
    policies_by_id: dict[str, list[PolicyFixture]] = defaultdict(list)
    for policy_payload in fixture_data.policies:
        policy = PolicyFixture.model_validate(policy_payload)
        policies_by_id[policy.policy_id].append(policy)

    for policies in policies_by_id.values():
        ordered = sorted(policies, key=lambda policy: policy.effective_from)
        for older, newer in pairwise(ordered):
            assert older.effective_to is not None
            assert older.effective_to <= newer.effective_from
        assert all(policy.effective_to is not None for policy in ordered[:-1])


def test_no_real_identifiers_in_synthetic_data(fixture_data: FixtureData) -> None:
    for path, content in fixture_data.file_contents.items():
        for pattern_name, pattern in FORBIDDEN.items():
            match = re.search(pattern, content)
            if match is not None:
                line_number = content.count("\n", 0, match.start()) + 1
                pytest.fail(f"{path}: {pattern_name} matched on line {line_number}")


def test_injection_fixture_is_present_and_labelled(fixture_data: FixtureData) -> None:
    injection_claim = next(
        claim for claim in fixture_data.claims if claim["claim_id"] == "claim-cm-0012-injection"
    )

    assert "ignore prior instructions" in injection_claim["description"].lower()
