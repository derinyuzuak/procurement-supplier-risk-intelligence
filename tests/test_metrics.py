from pathlib import Path
import sys
import pytest
RAW=Path(__file__).resolve().parents[1]/'data/private/scms_delivery_history.csv'
pytestmark=pytest.mark.skipif(not RAW.exists(), reason='USAID source extract is local-only; run scripts/download_scms.py first.')
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from procurement_intelligence.data import load_scms
from procurement_intelligence.metrics import comparable_price_variance, product_dependency

def test_loaded_data_has_unique_ids_and_nonnegative_value():
    d=load_scms(RAW); assert d.record_id.is_unique; assert (d.line_value_usd >= 0).all()

def test_schedule_delta_is_calculated_from_dates():
    d=load_scms(RAW); row=d.dropna(subset=['scheduled_delivery_date','delivered_date']).iloc[0]; assert row.delivery_delta_days == (row.delivered_date-row.scheduled_delivery_date).days

def test_comparable_cohort_requires_multiple_vendors():
    d=load_scms(RAW); p=comparable_price_variance(d[d.is_external_vendor]); assert (p.comparable_lines > 0).all()

def test_dependency_is_bounded():
    d=load_scms(RAW); x=product_dependency(d[d.is_external_vendor]); assert x.max_product_dependency.between(0,1).all()
