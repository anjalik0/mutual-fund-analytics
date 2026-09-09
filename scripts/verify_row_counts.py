import sqlite3
import pandas as pd
from pathlib import Path


# =========================================================
# PATHS
# =========================================================

DB_PATH = Path("bluestock_mf.db")
PROCESSED_DIR = Path("data/processed")

conn = sqlite3.connect(DB_PATH)


# =========================================================
# CLEANED CSV → DATABASE TABLE MAPPING
# =========================================================

checks = [
    (
        "01_fund_master_cleaned.csv",
        "dim_fund"
    ),
    (
        "02_nav_history_cleaned.csv",
        "fact_nav"
    ),
    (
        "03_aum_by_fund_house_cleaned.csv",
        "fact_aum"
    ),
    (
        "04_monthly_sip_inflows_cleaned.csv",
        "fact_sip_inflows"
    ),
    (
        "05_category_inflows_cleaned.csv",
        "fact_category_inflows"
    ),
    (
        "06_industry_folio_count_cleaned.csv",
        "fact_folio_count"
    ),
    (
        "07_scheme_performance_cleaned.csv",
        "fact_performance"
    ),
    (
        "08_investor_transactions_cleaned.csv",
        "fact_transactions"
    ),
    (
        "09_portfolio_holdings_cleaned.csv",
        "fact_portfolio_holdings"
    ),
    (
        "10_benchmark_indices_cleaned.csv",
        "fact_benchmark_indices"
    )
]


# =========================================================
# VERIFY ROW COUNTS
# =========================================================

print("\n" + "=" * 75)
print("CLEANED CSV vs DATABASE ROW COUNT VERIFICATION")
print("=" * 75)

all_match = True

for csv_file, table_name in checks:

    # Read cleaned CSV
    csv_path = PROCESSED_DIR / csv_file

    cleaned_rows = len(
        pd.read_csv(csv_path)
    )

    # Get database row count
    result = conn.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    ).fetchone()

    database_rows = result[0]

    # Compare
    if cleaned_rows == database_rows:
        status = "MATCH"
    else:
        status = "MISMATCH"
        all_match = False

    print(
        f"{csv_file:<45} "
        f"CSV: {cleaned_rows:<6} "
        f"DB: {database_rows:<6} "
        f"{status}"
    )


# =========================================================
# FINAL RESULT
# =========================================================

print("\n" + "=" * 75)

if all_match:
    print("SUCCESS: All cleaned CSV row counts match database tables.")
else:
    print("WARNING: Some row counts do not match.")

print("=" * 75)

conn.close()