SELECT vendor, COUNT(*) AS comparable_shipments,
       AVG(CASE WHEN delivery_delta_days > 0 THEN 1.0 ELSE 0.0 END) AS late_rate,
       AVG(delivery_delta_days) AS mean_schedule_delta_days
FROM shipment_lines
WHERE is_external_vendor = 1 AND delivery_delta_days BETWEEN -365 AND 365
GROUP BY vendor;
