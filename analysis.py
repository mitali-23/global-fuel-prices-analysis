from pathlib import Path
import pandas as pd
import json

ROOT = Path(__file__).resolve().parent
df = pd.read_csv(ROOT / "data" / "fuel_prices_cleaned.csv", parse_dates=["date"])
numeric = ["petrol_usd_liter", "diesel_usd_liter", "lpg_usd_liter", "brent_crude_usd", "tax_percentage"]
summary = {
    "rows": int(len(df)),
    "countries": int(df["country"].nunique()),
    "regions": int(df["region"].nunique()),
    "date_min": str(df["date"].min().date()),
    "date_max": str(df["date"].max().date()),
    "missing_cells": int(df.isna().sum().sum()),
    "duplicate_rows": int(df.duplicated().sum()),
    "numeric_describe": df[numeric].describe().round(4).to_dict(),
    "yearly_means": df.groupby(df["date"].dt.year)[numeric].mean().round(4).to_dict(orient="index"),
    "regional_means": df.groupby("region")[numeric].mean().round(4).to_dict(orient="index"),
    "correlations": df[numeric].corr().round(4).to_dict()
}
(ROOT / "outputs" / "analysis_summary_rerun.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps({k: summary[k] for k in ["rows", "countries", "regions", "date_min", "date_max", "missing_cells", "duplicate_rows"]}, indent=2))
