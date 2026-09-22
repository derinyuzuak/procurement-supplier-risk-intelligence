from __future__ import annotations
import numpy as np
import pandas as pd


def percentile_score(values: pd.Series) -> pd.Series:
    return values.rank(pct=True, method='average').mul(100)


def supplier_delivery(df: pd.DataFrame) -> pd.DataFrame:
    valid = df[df['delivery_delta_days'].between(-365, 365)].copy()
    return valid.groupby('vendor', as_index=False).agg(
        shipments=('record_id','size'),
        on_time_rate=('on_or_before_schedule','mean'),
        late_rate=('on_or_before_schedule', lambda x: 1 - x.mean()),
        p90_delay_days=('delivery_delta_days', lambda s: s.quantile(.90)),
    )


def comparable_price_variance(df: pd.DataFrame) -> pd.DataFrame:
    x = df[(df['pack_price_usd'] > 0) & df['shipment_year'].notna()].copy()
    keys = ['item_description','dosage_form','pack_size','country','shipment_year']
    x['cohort_n'] = x.groupby(keys)['vendor'].transform('nunique')
    x = x[x['cohort_n'].ge(2)].copy()
    x['cohort_median_price'] = x.groupby(keys)['pack_price_usd'].transform('median')
    x['price_variance_ratio'] = x['pack_price_usd'].div(x['cohort_median_price']).sub(1)
    x['positive_price_variance'] = x['price_variance_ratio'].clip(lower=0)
    return x.groupby('vendor', as_index=False).agg(
        comparable_lines=('record_id','size'),
        mean_positive_price_variance=('positive_price_variance','mean'),
    )


def product_dependency(df: pd.DataFrame) -> pd.DataFrame:
    by_product = df.groupby(['item_description','vendor'], as_index=False)['line_value_usd'].sum()
    by_product['product_total'] = by_product.groupby('item_description')['line_value_usd'].transform('sum')
    by_product['vendor_product_share'] = by_product['line_value_usd'].div(by_product['product_total'])
    return by_product.groupby('vendor', as_index=False).agg(max_product_dependency=('vendor_product_share','max'), products_served=('item_description','nunique'))
