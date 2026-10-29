from pathlib import Path
import sqlite3, json
import pandas as pd
from flask import Flask, render_template, request, jsonify, abort
import plotly.express as px
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "fuel_prices.db"
app = Flask(__name__)

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_data():
    query = "SELECT * FROM fuel_prices WHERE 1=1"
    params = []
    for field in ["region", "income_level", "subsidy_level", "country"]:
        value = request.args.get(field, "").strip()
        if value:
            query += f" AND {field} = ?"
            params.append(value)
    start = request.args.get("start_date", "").strip()
    end = request.args.get("end_date", "").strip()
    if start:
        query += " AND date >= ?"; params.append(start)
    if end:
        query += " AND date <= ?"; params.append(end)
    query += " ORDER BY date"
    with get_conn() as conn:
        df = pd.read_sql_query(query, conn, params=params, parse_dates=["date"])
    return df

def choices():
    with get_conn() as conn:
        result = {}
        for field in ["region", "income_level", "subsidy_level", "country"]:
            result[field] = [r[0] for r in conn.execute(f"SELECT DISTINCT {field} FROM fuel_prices ORDER BY {field}")]
    return result

def fig_json(fig):
    return json.loads(fig.to_json())

@app.route("/")
def index():
    df = get_data()
    if df.empty:
        return render_template("dashboard.html", filters=choices(), selected=request.args, stats={}, charts={}, no_data=True)
    stats = {
        "rows": f"{len(df):,}",
        "countries": f"{df['country'].nunique():,}",
        "petrol": f"${df['petrol_usd_liter'].mean():.2f}",
        "tax": f"{df['tax_percentage'].mean():.1f}%"
    }
    yearly = df.groupby(df["date"].dt.year, as_index=False).agg(
        Petrol=("petrol_usd_liter","mean"), Diesel=("diesel_usd_liter","mean"), LPG=("lpg_usd_liter","mean"))
    yearly = yearly.rename(columns={"date":"year"}) if "date" in yearly.columns else yearly
    yearly["year"] = yearly.iloc[:,0].astype(str)
    fig1 = px.line(yearly, x="year", y=["Petrol","Diesel","LPG"], markers=True,
                   title="Fuel price trend over time", labels={"value":"USD per litre","year":"Year","variable":"Fuel"})
    region = df.groupby("region", as_index=False).agg(Petrol=("petrol_usd_liter","mean"), Tax=("tax_percentage","mean"))
    fig2 = px.bar(region.sort_values("Petrol"), x="Petrol", y="region", orientation="h",
                  title="Average petrol price by region", labels={"Petrol":"USD per litre","region":"Region"})
    income = df.groupby("income_level", as_index=False).agg(Petrol=("petrol_usd_liter","mean"), Tax=("tax_percentage","mean"))
    fig3 = px.bar(income, x="income_level", y="Petrol", color="income_level",
                  title="Average petrol price by income group", labels={"Petrol":"USD per litre","income_level":"Income group"})
    scatter = px.scatter(df.sample(min(len(df), 5000), random_state=7), x="tax_percentage", y="petrol_usd_liter",
                         color="subsidy_level", hover_data=["country","region","date"],
                         title="Petrol price vs tax percentage (sampled to 5,000 points)",
                         labels={"tax_percentage":"Tax (%)","petrol_usd_liter":"Petrol (USD/litre)"})
    corr = df[["petrol_usd_liter","diesel_usd_liter","lpg_usd_liter","brent_crude_usd","tax_percentage"]].corr()
    fig5 = px.imshow(corr, text_auto=".2f", aspect="auto", title="Numeric variable correlation",
                     labels=dict(color="Correlation"))
    top = df.groupby(["country","region"], as_index=False).agg(
        Petrol=("petrol_usd_liter","mean"), Diesel=("diesel_usd_liter","mean"), Tax=("tax_percentage","mean"))
    top = top.sort_values("Petrol", ascending=False).head(12)
    fig6 = px.bar(top, x="Petrol", y="country", color="region", orientation="h",
                  title="12 highest average petrol-price countries", labels={"Petrol":"USD per litre","country":"Country"})
    fig6.update_layout(yaxis={"categoryorder":"total ascending"})
    charts = {k: fig_json(v) for k,v in {"trend":fig1,"region":fig2,"income":fig3,"tax":scatter,"corr":fig5,"top":fig6}.items()}
    return render_template("dashboard.html", filters=choices(), selected=request.args, stats=stats, charts=charts, no_data=False)

@app.route("/story")
def story():
    df = get_data()
    if df.empty:
        return render_template("story.html", scenes=[], selected=request.args)
    region = df.groupby("region")["petrol_usd_liter"].mean().sort_values()
    year = df.groupby(df["date"].dt.year)["petrol_usd_liter"].mean()
    subsidy = df.groupby("subsidy_level")["petrol_usd_liter"].mean().sort_values()
    income = df.groupby("income_level")["petrol_usd_liter"].mean().sort_values()
    scenes = [
      {"title":"Scene 1 — Global overview","text":f"The filtered view contains {len(df):,} records across {df['country'].nunique()} countries. Mean petrol price is ${df['petrol_usd_liter'].mean():.2f}/litre, diesel is ${df['diesel_usd_liter'].mean():.2f}/litre and LPG is ${df['lpg_usd_liter'].mean():.2f}/litre."},
      {"title":"Scene 2 — Regional price gaps","text":f"{region.index[-1]} has the highest regional average petrol price (${region.iloc[-1]:.2f}/litre), while {region.index[0]} has the lowest (${region.iloc[0]:.2f}/litre) in the selected records."},
      {"title":"Scene 3 — Time trend","text":f"Across available years, the average petrol price ranges from ${year.min():.2f}/litre (year {int(year.idxmin())}) to ${year.max():.2f}/litre (year {int(year.idxmax())})."},
      {"title":"Scene 4 — Income groups","text":f"Average petrol price by income group ranges from ${income.iloc[0]:.2f}/litre ({income.index[0]}) to ${income.iloc[-1]:.2f}/litre ({income.index[-1]}). This is descriptive and may reflect multiple factors."},
      {"title":"Scene 5 — Subsidies and policy context","text":f"Subsidy categories show different observed price averages; the lowest in this filtered view is {subsidy.index[0]} (${subsidy.iloc[0]:.2f}/litre) and the highest is {subsidy.index[-1]} (${subsidy.iloc[-1]:.2f}/litre). Category labels alone do not prove a causal subsidy effect."}
    ]
    return render_template("story.html", scenes=scenes, selected=request.args)

@app.route("/api/summary")
def api_summary():
    df = get_data()
    if df.empty:
        return jsonify({"rows":0,"countries":0})
    return jsonify({"rows":int(len(df)), "countries":int(df.country.nunique()),
                    "date_min":str(df.date.min().date()), "date_max":str(df.date.max().date()),
                    "mean_petrol":round(float(df.petrol_usd_liter.mean()),4),
                    "mean_diesel":round(float(df.diesel_usd_liter.mean()),4),
                    "mean_lpg":round(float(df.lpg_usd_liter.mean()),4),
                    "mean_tax":round(float(df.tax_percentage.mean()),4)})

@app.route("/health")
def health():
    with get_conn() as conn:
        rows = conn.execute("SELECT COUNT(*) FROM fuel_prices").fetchone()[0]
    return jsonify({"status":"ok","database_rows":rows})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
