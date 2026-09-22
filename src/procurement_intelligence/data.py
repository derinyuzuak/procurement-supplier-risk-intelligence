"""Small, reusable preparation helpers. Analytical choices stay in notebooks."""
from __future__ import annotations
from pathlib import Path
import pandas as pd

RENAME = {
    'ID':'record_id','Country':'country','Vendor':'vendor','Product Group':'product_group',
    'Item Description':'item_description','Dosage':'dosage','Dosage Form':'dosage_form',
    'Unit of Measure (Per Pack)':'pack_size','Line Item Quantity':'quantity',
    'Line Item Value':'line_value_usd','Pack Price':'pack_price_usd','Unit Price':'unit_price_usd',
    'PO Sent to Vendor Date':'po_sent_date','Scheduled Delivery Date':'scheduled_delivery_date',
    'Delivered to Client Date':'delivered_date','Shipment Mode':'shipment_mode',
    'Freight Cost (USD)':'freight_usd','Line Item Insurance (USD)':'insurance_usd',
}
DATE_COLUMNS = ['po_sent_date','scheduled_delivery_date','delivered_date']


def load_scms(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path).rename(columns=RENAME)
    for column in DATE_COLUMNS:
        df[column] = pd.to_datetime(df[column], format='%d-%m-%Y', errors='coerce')
    df['vendor'] = df['vendor'].str.strip()
    intermediary_label = 'SCMS ' + 'from RDC'
    df['is_external_vendor'] = ~df['vendor'].eq(intermediary_label)
    df['delivery_delta_days'] = (df['delivered_date'] - df['scheduled_delivery_date']).dt.days
    df['on_or_before_schedule'] = df['delivery_delta_days'].le(0)
    df['shipment_year'] = df['scheduled_delivery_date'].dt.year
    return df

