# Interactive review dashboard

This browser-based dashboard needs no installation, cloud account or data upload.

## Run locally

From the repository root:

```powershell
python scripts/build_dashboard_data.py
python -m http.server 8765
```

Open `http://127.0.0.1:8765/dashboard/`.

## What it does

- Portfolio view: fixed-size supplier markers on a Risk x Observed Value matrix.
- Supplier evidence: selector, review hypothesis, management question, observed value and risk components.
- Decision boundary: visible reminder that the output is not a supplier-switch recommendation.

`data.js` contains only the anonymized, derived supplier decision table. It does not contain raw SCMS rows or supplier identities.
