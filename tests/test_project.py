import unittest, sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

class ProjectIntegrityTests(unittest.TestCase):
    def test_clean_csv_exists_and_schema(self):
        p = ROOT / "data" / "fuel_prices_cleaned.csv"
        self.assertTrue(p.exists())
        df = pd.read_csv(p)
        self.assertEqual(len(df), 27468)
        self.assertIn("avg_fuel_price_usd_liter", df.columns)
        self.assertEqual(int(df.isna().sum().sum()), 0)

    def test_db_row_count_and_views(self):
        conn = sqlite3.connect(ROOT / "data" / "fuel_prices.db")
        count = conn.execute("SELECT COUNT(*) FROM fuel_prices").fetchone()[0]
        self.assertEqual(count, 27468)
        views = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='view'")}
        self.assertTrue({"v_regional_fuel_summary","v_yearly_fuel_trends","v_country_fuel_summary"}.issubset(views))
        conn.close()

    def test_no_duplicate_country_date_pairs(self):
        df = pd.read_csv(ROOT / "data" / "fuel_prices_cleaned.csv")
        self.assertEqual(int(df.duplicated(["country","date"]).sum()), 0)

if __name__ == "__main__":
    unittest.main()
