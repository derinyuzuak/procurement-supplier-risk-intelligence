from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
# Local runtime location; set PROCUREMENT_EXTRA_PACKAGES if using another environment.
extra = Path(__file__).resolve().parents[1] / 'work' / 'python_packages'
if extra.exists(): sys.path.insert(0, str(extra))
import pandas as pd
from procurement_intelligence.data import load_scms
from procurement_intelligence.metrics import supplier_delivery, comparable_price_variance, product_dependency
from procurement_intelligence.scoring import build_risk_score, action_from_evidence
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/'data/private/scms_delivery_history.csv'; OUT=ROOT/'results'; VIS=ROOT/'visuals'
OUT.mkdir(exist_ok=True); VIS.mkdir(exist_ok=True)
df=load_scms(RAW)
external=df[df.is_external_vendor].copy()
valid_delivery=external[external.delivery_delta_days.between(-365,365)]
quality=pd.DataFrame([{'metric':'Rows','value':len(df)}, {'metric':'Columns','value':len(df.columns)}, {'metric':'External-vendor eligible rows','value':len(external)}, {'metric':'Duplicate record IDs','value':int(df.record_id.duplicated().sum())}, {'metric':'Non-positive line values','value':int((df.line_value_usd<=0).sum())}, {'metric':'Valid delivery comparisons','value':len(valid_delivery)}, {'metric':'PO date coverage','value':round(df.po_sent_date.notna().mean(),4)}])
quality.to_csv(OUT/'data_quality_summary.csv',index=False)
contract=pd.DataFrame([
 ['Financial exposure','SUPPORTED','Positive line-item value has complete coverage; interpreted as observed value, not organizational spend.'],
 ['Supplier concentration','SUPPORTED','Vendor and line-item value are present; intermediary-labelled rows are excluded from supplier action analysis.'],
 ['Product/category dependency','SUPPORTED','Item description and value support vendor share within observed item descriptions.'],
 ['Comparable unit-price variance','CONDITIONAL','Only exact product-form-pack-country-year cohorts with at least two vendors are compared. This is a benchmark signal, not a savings estimate.'],
 ['Schedule adherence proxy','CONDITIONAL','Scheduled and delivered dates are populated, but source guidance cautions against direct lead-time conclusions. Used as a shipment-level proxy, not a supplier SLA claim.'],
 ['Lead-time risk','UNSUPPORTED','PO date coverage is incomplete and source guidance warns against direct lead-time conclusions.'],
 ['Quality risk','UNSUPPORTED','No verified quality, rejection, or defect field.'],
 ['Compliance risk','UNSUPPORTED','No verified compliance or contract-performance field.'],
],columns=['business_concept','status','evidence_and_limit'])
contract.to_csv(OUT/'analytical_contract.csv',index=False)
spend=external.groupby('vendor',as_index=False).agg(line_value_usd=('line_value_usd','sum'),shipments=('record_id','size'))
spend['spend_share']=spend.line_value_usd/spend.line_value_usd.sum()
alias_map=spend.sort_values('line_value_usd',ascending=False)[['vendor']].reset_index(drop=True)
alias_map['supplier_alias']=[f'Supplier {i:02d}' for i in range(1,len(alias_map)+1)]
spend=spend.merge(alias_map,on='vendor',how='left')
delivery=supplier_delivery(external); price=comparable_price_variance(external); dependency=product_dependency(external)
suppliers=spend.merge(delivery,on=['vendor','shipments'],how='left').merge(price,on='vendor',how='left').merge(dependency,on='vendor',how='left')
# Suppliers without sufficient comparator evidence are deliberately excluded from score/action recommendations.
eligible=suppliers[(suppliers.comparable_lines.fillna(0)>=10)&(suppliers.shipments>=10)&suppliers.late_rate.notna()].copy()
scored=build_risk_score(eligible)
scored['action']=scored.apply(action_from_evidence,axis=1)
scored=scored.sort_values('line_value_usd',ascending=False).reset_index(drop=True)
# no public vendor identity is written
public_cols=['supplier_alias','line_value_usd','shipments','spend_share','on_time_rate','p90_delay_days','late_rate','comparable_lines','mean_positive_price_variance','max_product_dependency','products_served','delivery_risk','commercial_risk','dependency_risk','observable_risk_score','action']
scored[public_cols].to_csv(OUT/'supplier_decision_table.csv',index=False)
concentration=spend.sort_values('line_value_usd',ascending=False).head(15).copy()
concentration[['supplier_alias','line_value_usd','spend_share','shipments']].to_csv(OUT/'spend_concentration.csv',index=False)
# visual 1 concentration
fig,ax=plt.subplots(figsize=(10,5)); x=concentration.sort_values('line_value_usd'); ax.barh(x.supplier_alias,x.line_value_usd/1e6,color='#0f766e'); ax.set(xlabel='Observed line-item value (USD, millions)',title='Top supplier concentration (anonymized)'); fig.tight_layout(); fig.savefig(VIS/'spend_concentration.png',dpi=180); plt.close(fig)
# visual 3 actions
fig,ax=plt.subplots(figsize=(8,4)); a=scored.action.value_counts().reindex(['PROTECT','DEVELOP','RENEGOTIATE','DIVERSIFY'],fill_value=0); ax.bar(a.index,a.values,color=['#15803d','#2563eb','#b45309','#c2410c']); ax.set(ylabel='Eligible suppliers',title='Evidence-based supplier action distribution'); fig.tight_layout(); fig.savefig(VIS/'supplier_action_map.png',dpi=180); plt.close(fig)
# visual 4 product dependency
fig,ax=plt.subplots(figsize=(9,5)); x=scored.nlargest(15,'max_product_dependency').sort_values('max_product_dependency'); ax.barh(x.supplier_alias,x.max_product_dependency,color='#7c3aed'); ax.set(xlabel='Largest observed share within one item description',title='Product dependency signal'); ax.xaxis.set_major_formatter(lambda v,pos:f'{v:.0%}'); fig.tight_layout(); fig.savefig(VIS/'dependency_analysis.png',dpi=180); plt.close(fig)
summary={'source_rows':int(len(df)),'eligible_external_supplier_rows':int(len(external)),'scored_suppliers':int(len(scored)),'observed_value_usd':float(external.line_value_usd.sum()),'delivery_comparison_coverage':float(len(valid_delivery)/len(external)),'comparable_line_coverage':float(scored.comparable_lines.sum()/len(external)),'source_period':{'start':str(df.scheduled_delivery_date.min().date()),'end':str(df.scheduled_delivery_date.max().date())},'action_counts':scored.action.value_counts().to_dict()}
(OUT/'analysis_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))


