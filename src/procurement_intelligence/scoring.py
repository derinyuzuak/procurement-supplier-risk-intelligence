from __future__ import annotations
import pandas as pd
from .metrics import percentile_score


def build_risk_score(suppliers: pd.DataFrame) -> pd.DataFrame:
    x = suppliers.copy()
    x['delivery_risk'] = percentile_score(x['late_rate'])
    x['commercial_risk'] = percentile_score(x['mean_positive_price_variance'])
    x['dependency_risk'] = percentile_score(x['max_product_dependency'])
    # Financial exposure is deliberately not a component: it is the matrix axis.
    x['observable_risk_score'] = (0.45*x['delivery_risk'] + 0.35*x['commercial_risk'] + 0.20*x['dependency_risk']).round(1)
    return x


def action_from_evidence(row: pd.Series) -> str:
    if row['observable_risk_score'] >= 75 and row['spend_share'] >= .05:
        return 'DIVERSIFY'
    if row['commercial_risk'] >= 75 and row['comparable_lines'] >= 10:
        return 'RENEGOTIATE'
    if row['delivery_risk'] >= 75 and row['shipments'] >= 10:
        return 'DEVELOP'
    return 'PROTECT'
