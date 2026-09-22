# Data dictionary

The original 33-column SCMS file remains local under `data/private/` and is not published. These analytical aliases are used after explicit type conversion.

| Analytical field | Source field | Use |
|---|---|---|
| `record_id` | `ID` | record-level uniqueness check |
| `vendor` | `Vendor` | supplier portfolio; an intermediary-labelled value is excluded from action recommendations |
| `line_value_usd` | `Line Item Value` | observed value / exposure axis |
| `scheduled_delivery_date` | `Scheduled Delivery Date` | schedule adherence proxy |
| `delivered_date` | `Delivered to Client Date` | schedule adherence proxy |
| `item_description` | `Item Description` | product dependency and comparable cohort key |
| `pack_price_usd` | `Pack Price` | conditional commercial comparison |
| `country`, `dosage_form`, `pack_size`, `shipment_year` | source columns | controls for comparable price cohorts |

No quality, rejection, compliance, contract, or verified supplier master-data field is available.
