import nbformat as nbf
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
nbdir=ROOT/'notebooks'

def make(name,title,cells):
    nb=nbf.v4.new_notebook()
    nb['metadata']={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.12'}}
    nb.cells=[nbf.v4.new_markdown_cell(f'# {title}\n\nThis notebook is an analytical working paper. It reads the local USAID SCMS extract and writes only anonymized derived outputs.'),*cells]
    nbf.write(nb, nbdir/name)

setup="""from pathlib import Path\nimport sys, os\nROOT = Path.cwd().resolve().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.insert(0, str(ROOT / 'src'))\nsys.path.insert(0, str(ROOT / 'work' / 'python_packages'))\nos.environ['MPLBACKEND']='Agg'\nfrom procurement_intelligence.data import load_scms\nimport pandas as pd\npd.set_option('display.max_columns', 50)"""
make('01_data_quality_and_sql_validation.ipynb','01 — Data Quality, Field Audit & Analytical Contract',[
 nbf.v4.new_code_cell(setup),
 nbf.v4.new_code_cell("df = load_scms(ROOT/'data/private/scms_delivery_history.csv')\nprint(f'{df.shape[0]:,} rows × {df.shape[1]:,} fields')\npd.DataFrame({'field': df.columns, 'dtype': df.dtypes.astype(str).values}).head(12)"),
 nbf.v4.new_code_cell("audit = pd.DataFrame({'field': df.columns, 'missing_rate': df.isna().mean(), 'distinct_values': df.nunique()}).sort_values('missing_rate', ascending=False)\naudit.head(15)"),
 nbf.v4.new_code_cell("pd.read_csv(ROOT/'results/analytical_contract.csv')"),
 nbf.v4.new_markdown_cell('**Decision.** Quality, compliance and lead-time risk are not observable in this extract and are excluded. Schedule adherence remains conditional because the catalog advises against direct lead-time conclusions.')])
make('02_spend_and_supplier_portfolio.ipynb','02 — Spend & Supplier Portfolio',[
 nbf.v4.new_code_cell(setup),nbf.v4.new_code_cell("portfolio=pd.read_csv(ROOT/'results/spend_concentration.csv')\nportfolio.head(10)"),
 nbf.v4.new_code_cell("from IPython.display import Image, display\ndisplay(Image(filename=ROOT/'visuals/spend_concentration.png'))"),
 nbf.v4.new_markdown_cell('Observed value represents the source’s line-item value. It is used for portfolio exposure, not as a risk-score input.')])
make('03_risk_score_and_exposure.ipynb','03 — Risk Score & Exposure',[
 nbf.v4.new_code_cell(setup),nbf.v4.new_code_cell("scorecard=pd.read_csv(ROOT/'results/supplier_decision_table.csv')\nscorecard.sort_values('observable_risk_score',ascending=False)"),
 nbf.v4.new_code_cell("from IPython.display import Image, display\ndisplay(Image(filename=ROOT/'visuals/supplier_exposure_matrix.png'))"),
 nbf.v4.new_markdown_cell('The score combines only conditional/supported delivery, commercial and dependency signals. Total observed value is visible only on the matrix axis.')])
make('04_opportunity_and_supplier_actions.ipynb','04 — Opportunity & Supplier Actions',[
 nbf.v4.new_code_cell(setup),nbf.v4.new_code_cell("actions=pd.read_csv(ROOT/'results/supplier_decision_table.csv')\nactions.groupby('action').agg(suppliers=('supplier_alias','size'), observed_value_usd=('line_value_usd','sum')).sort_values('observed_value_usd',ascending=False)"),
 nbf.v4.new_code_cell("actions[['supplier_alias','action','observable_risk_score','late_rate','mean_positive_price_variance','max_product_dependency']].sort_values('observable_risk_score',ascending=False)"),
 nbf.v4.new_markdown_cell('Actions are review hypotheses. `RENEGOTIATE` requires comparable price evidence; `DEVELOP` requires schedule evidence; `DIVERSIFY` requires high score and material exposure. No savings are asserted.')])
make('05_decision_summary.ipynb','05 — Decision Summary',[
 nbf.v4.new_code_cell(setup),nbf.v4.new_code_cell("import json\nsummary=json.loads((ROOT/'results/analysis_summary.json').read_text())\nsummary"),
 nbf.v4.new_code_cell("scorecard=pd.read_csv(ROOT/'results/supplier_decision_table.csv')\nscorecard.groupby('action').agg(eligible_suppliers=('supplier_alias','size'), exposure_usd=('line_value_usd','sum')).sort_values('exposure_usd',ascending=False)"),
 nbf.v4.new_markdown_cell('**Management use.** Review the anonymized scorecard with supplier, procurement and logistics owners; validate supplier identities and context before any intervention. The README is the management-facing decision summary; it uses the same result files.')])
print('notebooks written')


