-- Run after the prepared SCMS data is loaded as shipment_lines.
SELECT COUNT(*) AS rows, COUNT(DISTINCT record_id) AS unique_record_ids,
       SUM(CASE WHEN line_value_usd <= 0 THEN 1 ELSE 0 END) AS non_positive_values,
       SUM(CASE WHEN delivered_date < '2000-01-01' THEN 1 ELSE 0 END) AS implausible_dates
FROM shipment_lines;
