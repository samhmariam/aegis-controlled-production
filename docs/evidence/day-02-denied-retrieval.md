# Day 2 Denied Retrieval Evidence

- **Evidence ID:** `evidence-day02-denied-0001`
- **Current commit:** `f07c357222f0f3593201e118679249590eaf340e`
- **Producing command:**
  `uv run python -c "from fastapi.testclient import TestClient; from aegis.api.app import app; client=TestClient(app); headers={'Authorization':'Bearer 1dJHYvMah8OKx0pzOF7wrfMNRw3817vo'}; paths=['/claims/claim-cd-0006/context','/claims/claim-zz-9999/context']; print([(path, (r:=client.get(path, params={'query':'excess'}, headers=headers)).status_code, r.json()) for path in paths])"`
- **Producing tests:**
  - `test_cross_tenant_request_returns_404_claim_not_accessible`
  - `test_nonexistent_claim_response_is_identical_to_inaccessible`

## Observed responses

| Request | Status | Body |
| --- | ---: | --- |
| Cross-tenant `claim-cd-0006` | `404` | `{"error_code": "claim_not_accessible", "details": []}` |
| Nonexistent `claim-zz-9999` | `404` | `{"error_code": "claim_not_accessible", "details": []}` |

The two responses have identical status, error code, and details. Tenant scope comes from the synthetic handler credential for `tenant-cotswold-demo-a`; the query string cannot override it.
