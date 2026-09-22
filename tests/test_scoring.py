from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import pandas as pd
from procurement_intelligence.scoring import build_risk_score, action_from_evidence

def sample():
    return pd.DataFrame({'late_rate':[.1,.6,.3], 'mean_positive_price_variance':[.0,.5,.1], 'max_product_dependency':[.2,.8,.4], 'line_value_usd':[1e6,2e6,3e6], 'spend_share':[.03,.10,.04], 'shipments':[20,20,20], 'comparable_lines':[20,20,20]})

def test_score_is_bounded_and_excludes_value_component():
    x=build_risk_score(sample())
    assert x.observable_risk_score.between(0,100).all()
    changed=sample(); changed['line_value_usd'] *= 1000
    y=build_risk_score(changed)
    assert x.observable_risk_score.equals(y.observable_risk_score)

def test_renegotiate_requires_comparable_evidence():
    x=build_risk_score(sample()).iloc[1].copy(); x['observable_risk_score']=50; x['commercial_risk']=95; x['comparable_lines']=0
    assert action_from_evidence(x) != 'RENEGOTIATE'

def test_diversify_requires_material_exposure():
    x=build_risk_score(sample()).iloc[1].copy(); x['observable_risk_score']=90; x['spend_share']=.01
    assert action_from_evidence(x) != 'DIVERSIFY'
