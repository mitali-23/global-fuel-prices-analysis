# Requirements coverage checklist

| Requirement visible in project-description video | Included artifact / implementation |
|---|---|
| Data collection & extraction | `data/fuel_prices_cleaned.csv`, `analysis.py` |
| Store data in DB | `data/fuel_prices.db` |
| Perform SQL operations | `sql/analysis_queries.sql`, indexed table, 3 views |
| Connect database to Tableau | Tableau import instructions + row-level and aggregate CSV extracts |
| Data preparation | `analysis.py`, derived fields, quality JSON |
| Unique visualizations | 6 interactive Plotly charts + 4 static EDA charts |
| Responsive dashboard | Flask dashboard with filters, KPI cards, responsive CSS |
| Story / number of scenes | 5 dynamic scenes at `/story` |
| Performance testing | 5,000-point scatter cap, SQL indexes, unit tests; benchmark guidance in PDF |
| Web integration | Flask app, dashboard, story, JSON API and health endpoint |
| Project demonstration & documentation | Detailed PDF, README and suggested demo flow below |

## Suggested demonstration recording (4–6 minutes)
1. Introduce the problem and dataset scope.
2. Show data quality metrics and the cleaned CSV.
3. Open SQLite and run one query from `sql/analysis_queries.sql`.
4. Launch Flask and demonstrate region/country/date/income/subsidy filters.
5. Explain 2–3 charts and caveat that association is not causation.
6. Open the 5-scene story and explain the policy/logistics/research audience use cases.
7. Show Tableau-ready CSVs and close with limitations and next steps.
