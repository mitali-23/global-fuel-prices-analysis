-- Global Fuel Prices & Taxation: reusable SQLite queries
-- 1. Dataset size and date coverage
SELECT COUNT(*) AS rows, COUNT(DISTINCT country) AS countries,
       MIN(date) AS first_date, MAX(date) AS last_date
FROM fuel_prices;

-- 2. Regional comparison
SELECT * FROM v_regional_fuel_summary ORDER BY avg_petrol_usd_liter DESC;

-- 3. Yearly trends
SELECT * FROM v_yearly_fuel_trends ORDER BY year;

-- 4. Highest average petrol price by country
SELECT country, region, ROUND(AVG(petrol_usd_liter),3) AS avg_petrol
FROM fuel_prices GROUP BY country, region
ORDER BY avg_petrol DESC LIMIT 10;

-- 5. Compare subsidy categories
SELECT subsidy_level, COUNT(*) AS observations,
       ROUND(AVG(petrol_usd_liter),3) AS petrol_avg,
       ROUND(AVG(diesel_usd_liter),3) AS diesel_avg,
       ROUND(AVG(tax_percentage),2) AS tax_avg
FROM fuel_prices GROUP BY subsidy_level
ORDER BY petrol_avg;

-- 6. Correlation-ready row-level extract
SELECT date, country, region, income_level, subsidy_level,
       petrol_usd_liter, diesel_usd_liter, lpg_usd_liter,
       brent_crude_usd, tax_percentage,
       avg_fuel_price_usd_liter, fuel_price_spread_petrol_diesel
FROM fuel_prices;
