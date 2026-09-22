SELECT vendor, SUM(line_value_usd) AS observed_line_value_usd, COUNT(*) AS shipment_lines,
       SUM(line_value_usd) / SUM(SUM(line_value_usd)) OVER () AS value_share
FROM shipment_lines
WHERE is_external_vendor = 1
GROUP BY vendor
ORDER BY observed_line_value_usd DESC;
