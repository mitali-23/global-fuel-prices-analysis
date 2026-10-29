# Global Fuel Prices & Taxation Analytics

A complete, local-first analytics project built from the supplied `global_fuel_prices_Dataset.csv`. It includes data cleaning, exploratory analysis, a SQLite database, SQL queries/views, Tableau-ready extracts, static charts, a responsive Flask dashboard, a five-scene data story, validation tests, and documentation.

## Dataset
- Source file: `global_fuel_prices_Dataset.csv`
- Cleaned row count: 27,468
- Countries: 84
- Regions: 7
- Date range: 2020-01-06 through 2026-04-06
- Source fields: date, country, region, income_level, subsidy_level, petrol_usd_liter, diesel_usd_liter, lpg_usd_liter, brent_crude_usd, tax_percentage
- Derived fields: year, month, quarter, fuel_price_spread_petrol_diesel, fuel_price_spread_petrol_lpg, avg_fuel_price_usd_liter

## Quick start
1. Install Python 3.10+.
2. In this folder, create/activate a virtual environment (recommended).
3. Run `pip install -r requirements.txt`.
4. Run `python app.py`.
5. Open `http://127.0.0.1:5000` in your browser. The story is at `/story`; health endpoint is `/health`.

The SQLite database is already included at `data/fuel_prices.db`; no database setup step is needed. `python analysis.py` reruns core summary calculations.

## Main components
- `app.py`: Flask routes, parameterized SQL filtering, chart creation, summary API.
- `templates/dashboard.html`: responsive filterable dashboard.
- `templates/story.html`: five-scene narrative page.
- `data/fuel_prices.db`: row-level data plus indexed columns and analytical views.
- `data/fuel_prices_cleaned.csv`: cleaned row-level data for external BI tools.
- `data/*_summary.csv`: pre-aggregated extracts for Tableau/Excel.
- `sql/analysis_queries.sql`: example queries and views.
- `outputs/charts/`: static EDA visuals.
- `outputs/analysis_summary.json`, `outputs/data_quality.json`: machine-readable results.
- `tests/test_project.py`: basic data/database integrity tests.
- `docs/Project_Documentation.pdf`: detailed project documentation.

## Tableau connection
Use Tableau Desktop/Public → Connect → To a File → Text File to load `data/fuel_prices_cleaned.csv`, or connect to the SQLite database using a compatible SQLite connector/driver. The `yearly_summary.csv`, `regional_summary.csv`, `country_summary.csv`, `income_summary.csv`, and `subsidy_summary.csv` files are convenient starter extracts. Suggested worksheets: yearly fuel trends, regional price comparison, tax vs petrol scatter, subsidy/income comparisons, country ranking and correlation heatmap. Add filters for date, region, country, income level and subsidy level. A native Tableau workbook is not included; create/save the `.twb`/`.twbx` in Tableau Desktop if your course requires a Tableau-authored file.

## Data interpretation cautions
- The uploaded file has no accompanying data dictionary or source methodology.
- `brent_crude_usd` is retained as supplied; its exact unit/meaning should be confirmed before external interpretation.
- A repeated/regular time series and clean data do not by themselves guarantee that values are official or real-world measurements.
- Descriptive averages/correlations do not establish causal effects of tax or subsidies.
- Prices as low as $0.01/litre and tax values at 0%/65% are retained because they are present in the source; inspect them as potential edge cases rather than silently deleting them.

## Testing
Run `python -m unittest discover -s tests -v`.
