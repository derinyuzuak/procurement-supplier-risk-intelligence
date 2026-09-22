WITH comparable AS (
  SELECT *, MEDIAN(pack_price_usd) OVER (PARTITION BY item_description, dosage_form, pack_size, country, shipment_year) AS cohort_median
  FROM shipment_lines WHERE pack_price_usd > 0
)
SELECT vendor, AVG(CASE WHEN pack_price_usd > cohort_median THEN pack_price_usd / cohort_median - 1 ELSE 0 END) AS mean_positive_variance
FROM comparable GROUP BY vendor;
-- MEDIAN support varies by SQL engine; notebooks use pandas for this conditional calculation.
