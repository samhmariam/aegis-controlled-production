"""Query tokenisation and the deterministic fallback ranker.

Tokenisation is the injection boundary for retrieval: after it, a claim description cannot
contain an FTS operator, a quote, or SQL, because only [a-z0-9]+ survives.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

_TOKEN = re.compile(r"[a-z0-9]+")
MIN_TOKEN_LENGTH = 2
MAX_QUERY_TOKENS = 12


def query_tokens(raw: str) -> tuple[str, ...]:
    """Distinct, order-preserving, lowercase alphanumeric tokens, capped."""
    seen: dict[str, None] = {}
    for token in _TOKEN.findall(raw.casefold()):
        if len(token) < MIN_TOKEN_LENGTH:
            continue
        seen.setdefault(token, None)
        if len(seen) == MAX_QUERY_TOKENS:
            break
    return tuple(seen)


def fts_match_expression(tokens: Sequence[str]) -> str:
    """Build an FTS5 MATCH expression. Safe because every token is [a-z0-9]+ already."""
    return " OR ".join(f'"{token}"' for token in tokens)


def rank_by_token_overlap(
    tokens: Sequence[str], candidates: Sequence[tuple[str, str]]
) -> tuple[str, ...]:
    """Deterministic fallback ranking.

    Score is the number of distinct query tokens appearing as whole tokens in the clause.
    Zero-score clauses are dropped; ties break on clause_id ascending, so the result does not
    depend on the order rows came back from SQLite.
    """
    wanted = set(tokens)
    scored: list[tuple[int, str]] = []
    for clause_id, text in candidates:
        overlap = len(wanted & set(_TOKEN.findall(text.casefold())))
        if overlap:
            scored.append((-overlap, clause_id))
    return tuple(clause_id for _, clause_id in sorted(scored))


def build_excerpt(text: str, tokens: Sequence[str], *, width: int) -> str:
    """A bounded, verbatim, contiguous substring of the stored clause text.

    Verbatim matters: citation verification asserts `excerpt in stored_text`. Any ellipsis,
    normalisation or re-wrapping inside the returned span breaks that check. The trailing
    .strip() is safe — a stripped substring is still a substring — and it matches
    StrictModel's str_strip_whitespace, which would otherwise trim the value after validation
    and desynchronise it from what we checked.
    """
    if len(text) <= width:
        return text.strip()

    folded = text.casefold()
    hits = [pos for pos in (folded.find(token) for token in tokens) if pos >= 0]
    centre = min(hits) if hits else 0

    start = max(0, centre - width // 3)
    end = min(len(text), start + width)
    if start > 0:
        space = text.find(" ", start)
        start = start + 1 if space < 0 else space + 1
    if end < len(text):
        space = text.rfind(" ", start, end)
        if space > start:
            end = space
    return text[start:end].strip()
