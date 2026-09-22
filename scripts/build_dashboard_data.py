from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
source = pd.read_csv(ROOT / 'results' / 'supplier_decision_table.csv')
fields = ['supplier_alias','line_value_usd','shipments','spend_share','on_time_rate','late_rate','p90_delay_days','comparable_lines','mean_positive_price_variance','max_product_dependency','products_served','delivery_risk','commercial_risk','dependency_risk','observable_risk_score','action']
rows = source[fields].round(6).to_dict(orient='records')
(ROOT / 'dashboard' / 'data.js').write_text('window.SUPPLIER_DATA = ' + json.dumps(rows, indent=2) + ';\n', encoding='utf-8')
print(f'Wrote {len(rows)} anonymized supplier records.')
