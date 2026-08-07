"""
process_data.py

Reads all CSV files in the data/ folder, keeps only rows for
"Pink Morsels", computes Sales = Quantity * Price, and writes a
single output CSV with columns: Sales, Date, Region.
"""

import glob
import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
OUTPUT_PATH = os.path.join(DATA_DIR, "formatted_sales_data.csv")


def load_and_combine(data_dir: str) -> pd.DataFrame:
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in '{data_dir}'")

    frames = []
    for path in csv_files:
        df = pd.read_csv(path)
        # normalise column names to lowercase for reliable matching
        df.columns = [c.strip().lower() for c in df.columns]
        frames.append(df)

    return pd.concat(frames, ignore_index=True)


def clean_price(series: pd.Series) -> pd.Series:
    # handles values like "$1.50" as well as plain numbers
    return (
        series.astype(str)
        .str.replace(r"[^0-9.\-]", "", regex=True)
        .astype(float)
    )


def main():
    print(f"Looking for CSVs in: {DATA_DIR}")
    combined = load_and_combine(DATA_DIR)
    print(f"Loaded {len(combined)} total rows from {combined['product'].nunique()} product types")

    required = {"product", "price", "quantity", "date", "region"}
    missing = required - set(combined.columns)
    if missing:
        raise ValueError(
            f"Expected columns {required}, missing {missing}. "
            f"Found columns: {list(combined.columns)}"
        )

    # 1. keep only Pink Morsels
    pink_only = combined[combined["product"].str.strip().str.lower() == "pink morsel"].copy()

    # 2. compute sales = quantity * price
    pink_only["price"] = clean_price(pink_only["price"])
    pink_only["sales"] = pink_only["quantity"] * pink_only["price"]

    # 3. keep only Sales, Date, Region
    result = pink_only[["sales", "date", "region"]].rename(
        columns={"sales": "Sales", "date": "Date", "region": "Region"}
    )

    result.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(result)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()