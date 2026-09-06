# ADR 006: Tool Execution Outcome Semantics

## Status

Accepted

## Context

A tool call can time out after the request has left AEGIS but before the caller
receives a definitive response. The timeout therefore does not prove that the
tool did not run, and it does not prove that the requested effect happened.
Treating that observation as either failure or success would make the audit
record dishonest and could cause a retry to duplicate a consequential effect.

## Decision

`ToolStatus.UNCERTAIN` is the explicit result for an invocation whose effect
cannot be determined. It asserts neither that the effect happened nor that it
did not happen. An uncertain result:

1. Must not carry an `effect_id`, because AEGIS has not established an effect
   that it can identify or claim as its own result.
2. Must carry a machine-readable error code describing why the outcome is
   unknown, such as a timeout.
3. May be retried only under an idempotency key. A retryable uncertain result
   without an idempotency key is invalid because the retry could create a
   duplicate effect.
4. Must be surfaced as an unresolved operational state until a duplicate-safe
   retry, provider reconciliation, or human investigation establishes what
   happened.

The idempotency key binds the original attempt and any retry to the same
logical operation. A provider or tool adapter must use that key to return the
original result or a `duplicate` result rather than execute the effect again.
Without that guarantee, the caller must not retry the uncertain invocation.

## Consequences

- A tool timeout is represented honestly rather than silently classified as
  success or failure.
- Callers must distinguish "no effect observed" from "effect did not happen";
  the former is not evidence for the latter.
- Retry policy becomes part of the tool contract. Tools that cannot provide
  idempotent replay must hand uncertain outcomes to reconciliation or a human.
- Audit and operations surfaces must retain uncertain outcomes until their
  disposition is known; clearing the alert is not evidence that the original
  effect was absent.

## Verification

The implementation is in `src/aegis/tools/models.py`. Unit tests must verify
that uncertain results cannot claim an effect ID, require an error code, and
are rejected as retryable when no idempotency key is present. Integration tests
must verify that retrying with the same idempotency key returns the original
effect or a `duplicate` result without creating a second effect.