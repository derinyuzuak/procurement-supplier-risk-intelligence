WITH supplier_item AS (
  SELECT item_description, vendor, SUM(line_value_usd) AS value_usd
  FROM shipment_lines WHERE is_external_vendor = 1 GROUP BY item_description, vendor
)
SELECT item_description, vendor, value_usd,
       value_usd / SUM(value_usd) OVER (PARTITION BY item_description) AS supplier_share_within_item
FROM supplier_item;
