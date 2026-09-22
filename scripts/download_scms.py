from pathlib import Path
import hashlib
import json
import requests

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / 'data' / 'private'
PRIVATE.mkdir(parents=True, exist_ok=True)
source_url = 'https://raw.githubusercontent.com/Prashant-Abbi/Supply-Chain-Management/master/SCMS%20Dataset.csv'
target = PRIVATE / 'scms_delivery_history.csv'
response = requests.get(source_url, timeout=120)
response.raise_for_status()
target.write_bytes(response.content)
sha256 = hashlib.sha256(response.content).hexdigest()
provenance = {
    'dataset_title': 'Supply Chain Shipment Pricing Data',
    'original_publisher': 'USAID',
    'official_catalog_record': 'https://data.amerigeoss.org/dataset/supply-chain-shipment-pricing-data',
    'official_identifier': 'https://data.usaid.gov/api/views/a3rc-nmf6',
    'retrieval_route': 'Public mirror used because the historical USAID Socrata endpoint was unavailable during retrieval.',
    'mirror_url': source_url,
    'retrieved_utc': __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
    'file_name': target.name,
    'sha256': sha256,
    'bytes': len(response.content),
    'redistribution': 'not included in this repository; license metadata requires separate verification'
}
(PRIVATE / 'source_provenance.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
print(json.dumps({'bytes': provenance['bytes'], 'sha256': sha256, 'target': str(target)}, indent=2))
