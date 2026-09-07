# Day 2 Context Bundle Evidence

- **Evidence ID:** `evidence-day02-context-0001`
- **Claim:** `claim-cm-0001`
- **Tenant:** `tenant-cotswold-demo-a`
- **Current commit:** `f07c357222f0f3593201e118679249590eaf340e`
- **Producing command:**
  `uv run python -c "import json; from fastapi.testclient import TestClient; from aegis.api.app import app; response=TestClient(app).get('/claims/claim-cm-0001/context', params={'query':'excess'}, headers={'Authorization':'Bearer 1dJHYvMah8OKx0pzOF7wrfMNRw3817vo'}); print(json.dumps({'status_code':response.status_code,'body':response.json()}, indent=2, sort_keys=True))"`
- **Observed status:** `200`, `retrieved`

## Bundle

```json
{
  "claim_id": "claim-cm-0001",
  "tenant_id": "tenant-cotswold-demo-a",
  "policy_id": "policy-cm-motor-0001",
  "policy_version": "v2",
  "clause_ids": ["clause-cm-motor-0001-excess"],
  "retrieval_query": "excess",
  "excerpts": [
    {
      "clause_id": "clause-cm-motor-0001-excess",
      "excerpt": "A standard excess of 250.00 GBP applies to every motor claim unless the loss is a total theft reported within 24 hours.",
      "source_content_hash": "sha256:a28da1c8cfe919ce5d6689205dc56e9d72018065bfd6321adb1dc836c58ff9dc"
    }
  ],
  "limitations": [
    "retrieval method: sqlite fts5 bm25; lexical only, no semantic matching",
    "the query was reduced to alphanumeric tokens before search, so operators and punctuation in the query text are not honoured",
    "policy version was selected by claim loss date; a superseded version is refused, never substituted"
  ]
}
```

The selected version is `v2`; no newer version was substituted for the claim's loss date.
