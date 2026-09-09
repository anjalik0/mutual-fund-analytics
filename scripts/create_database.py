import sqlite3
import pandas as pd
from pathlib import Path

# =========================================================
# PROJECT PATHS
# =========================================================

DB_PATH = Path("bluestock_mf.db")
SCHEMA_PATH = Path("sql/schema.sql")
DATA_DIR = Path("data/processed")


# =========================================================
# 1. CREATE DATABASE + SCHEMA
# =========================================================

if DB_PATH.exists():
    DB_PATH.unlink()

conn = sqlite3.connect(DB_PATH)

with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
    schema = file.read()

conn.executescript(schema)
conn.commit()

print("Database schema created successfully!")


# =========================================================
# 2. LOAD FUND DIMENSION
# =========================================================

fund = pd.read_csv(DATA_DIR / "01_fund_master_cleaned.csv")

fund.to_sql(
    "dim_fund",
    conn,
    if_exists="append",
    index=False
)

print("Loaded dim_fund:", len(fund))


# =========================================================
# 3. CREATE DATE DIMENSION
# =========================================================

date_values = set()


def add_dates(filename, column):
    df = pd.read_csv(DATA_DIR / filename)

    dates = pd.to_datetime(
        df[column],
        errors="coerce"
    ).dropna()

    date_values.update(
        dates.dt.strftime("%Y-%m-%d").tolist()
    )


add_dates("02_nav_history_cleaned.csv", "date")
add_dates("03_aum_by_fund_house_cleaned.csv", "date")
add_dates("04_monthly_sip_inflows_cleaned.csv", "month")
add_dates("05_category_inflows_cleaned.csv", "month")
add_dates("06_industry_folio_count_cleaned.csv", "month")
add_dates("08_investor_transactions_cleaned.csv", "transaction_date")
add_dates("09_portfolio_holdings_cleaned.csv", "portfolio_date")
add_dates("10_benchmark_indices_cleaned.csv", "date")


# Sort dates
all_dates = sorted(date_values)

date_dimension = pd.DataFrame({
    "date": all_dates
})

# Generate date_id starting from 1
date_dimension.insert(
    0,
    "date_id",
    range(1, len(date_dimension) + 1)
)

# Date attributes
date_dimension["date"] = pd.to_datetime(
    date_dimension["date"]
)

date_dimension["year"] = date_dimension["date"].dt.year
date_dimension["month"] = date_dimension["date"].dt.month
date_dimension["month_name"] = date_dimension["date"].dt.month_name()
date_dimension["quarter"] = date_dimension["date"].dt.quarter

# Convert date back to SQLite-friendly format
date_dimension["date"] = date_dimension["date"].dt.strftime(
    "%Y-%m-%d"
)

date_dimension.to_sql(
    "dim_date",
    conn,
    if_exists="append",
    index=False
)

print("Loaded dim_date:", len(date_dimension))


# =========================================================
# DATE LOOKUP FUNCTION
# =========================================================

date_lookup = dict(
    zip(
        date_dimension["date"],
        date_dimension["date_id"]
    )
)


def convert_date_to_id(df, source_column, target_column):
    dates = pd.to_datetime(
        df[source_column],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    df[target_column] = dates.map(date_lookup)

    if df[target_column].isna().any():
        raise ValueError(
            f"Some dates could not be mapped for {source_column}"
        )

    df[target_column] = df[target_column].astype(int)

    return df


# =========================================================
# 4. LOAD NAV
# =========================================================

nav = pd.read_csv(
    DATA_DIR / "02_nav_history_cleaned.csv"
)

nav = convert_date_to_id(
    nav,
    "date",
    "date_id"
)

nav = nav[
    ["amfi_code", "date_id", "nav"]
]

nav.to_sql(
    "fact_nav",
    conn,
    if_exists="append",
    index=False
)

print("Loaded fact_nav:", len(nav))


# =========================================================
# 5. LOAD AUM
# =========================================================

aum = pd.read_csv(
    DATA_DIR / "03_aum_by_fund_house_cleaned.csv"
)

aum = convert_date_to_id(
    aum,
    "date",
    "date_id"
)

aum = aum[
    [
        "date_id",
        "fund_house",
        "aum_lakh_crore",
        "aum_crore",
        "num_schemes"
    ]
]

aum.to_sql(
    "fact_aum",
    conn,
    if_exists="append",
    index=False
)

print("Loaded fact_aum:", len(aum))


# =========================================================
# 6. LOAD SIP INFLOWS
# =========================================================

sip = pd.read_csv(
    DATA_DIR / "04_monthly_sip_inflows_cleaned.csv"
)

sip = convert_date_to_id(
    sip,
    "month",
    "date_id"
)

sip = sip[
    [
        "date_id",
        "sip_inflow_crore",
        "active_sip_accounts_crore",
        "new_sip_accounts_lakh",
        "sip_aum_lakh_crore",
        "yoy_growth_pct"
    ]
]

sip.to_sql(
    "fact_sip_inflows",
    conn,
    if_exists="append",
    index=False
)

print("Loaded fact_sip_inflows:", len(sip))


# =========================================================
# 7. LOAD CATEGORY INFLOWS
# =========================================================

category = pd.read_csv(
    DATA_DIR / "05_category_inflows_cleaned.csv"
)

category = convert_date_to_id(
    category,
    "month",
    "date_id"
)

category = category[
    [
        "date_id",
        "category",
        "net_inflow_crore"
    ]
]

category.to_sql(
    "fact_category_inflows",
    conn,
    if_exists="append",
    index=False
)

print("Loaded fact_category_inflows:", len(category))


# =========================================================
# 8. LOAD FOLIO COUNT
# =========================================================

folio = pd.read_csv(
    DATA_DIR / "06_industry_folio_count_cleaned.csv"
)

folio = convert_date_to_id(
    folio,
    "month",
    "date_id"
)

folio = folio[
    [
        "date_id",
        "total_folios_crore",
        "equity_folios_crore",
        "debt_folios_crore",
        "hybrid_folios_crore",
        "others_folios_crore"
    ]
]

folio.to_sql(
    "fact_folio_count",
    conn,
    if_exists="append",
    index=False
)

print("Loaded fact_folio_count:", len(folio))


# =========================================================
# 9. LOAD SCHEME PERFORMANCE
# =========================================================

performance = pd.read_csv(
    DATA_DIR / "07_scheme_performance_cleaned.csv"
)

performance = performance[
    [
        "amfi_code",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "aum_crore",
        "expense_ratio_pct",
        "morningstar_rating",
        "risk_grade"
    ]
]

performance.to_sql(
    "fact_performance",
    conn,
    if_exists="append",
    index=False
)

print("Loaded fact_performance:", len(performance))


# =========================================================
# 10. LOAD INVESTOR TRANSACTIONS
# =========================================================

transactions = pd.read_csv(
    DATA_DIR / "08_investor_transactions_cleaned.csv"
)

transactions = convert_date_to_id(
    transactions,
    "transaction_date",
    "transaction_date_id"
)

transactions = transactions[
    [
        "investor_id",
        "transaction_date_id",
        "amfi_code",
        "transaction_type",
        "amount_inr",
        "state",
        "city",
        "city_tier",
        "age_group",
        "gender",
        "annual_income_lakh",
        "payment_mode",
        "kyc_status"
    ]
]

transactions.to_sql(
    "fact_transactions",
    conn,
    if_exists="append",
    index=False
)

print("Loaded fact_transactions:", len(transactions))


# =========================================================
# 11. LOAD PORTFOLIO HOLDINGS
# =========================================================

portfolio = pd.read_csv(
    DATA_DIR / "09_portfolio_holdings_cleaned.csv"
)

portfolio = convert_date_to_id(
    portfolio,
    "portfolio_date",
    "portfolio_date_id"
)

portfolio = portfolio[
    [
        "amfi_code",
        "stock_symbol",
        "stock_name",
        "sector",
        "weight_pct",
        "market_value_cr",
        "current_price_inr",
        "portfolio_date_id"
    ]
]

portfolio.to_sql(
    "fact_portfolio_holdings",
    conn,
    if_exists="append",
    index=False
)

print("Loaded fact_portfolio_holdings:", len(portfolio))


# =========================================================
# 12. LOAD BENCHMARK INDICES
# =========================================================

benchmark = pd.read_csv(
    DATA_DIR / "10_benchmark_indices_cleaned.csv"
)

benchmark = convert_date_to_id(
    benchmark,
    "date",
    "date_id"
)

benchmark = benchmark[
    [
        "date_id",
        "index_name",
        "close_value"
    ]
]

benchmark.to_sql(
    "fact_benchmark_indices",
    conn,
    if_exists="append",
    index=False
)

print("Loaded fact_benchmark_indices:", len(benchmark))


# =========================================================
# 13. VERIFY ROW COUNTS
# =========================================================

print("\n========================================")
print("DATABASE ROW COUNTS")
print("========================================")

tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_aum",
    "fact_sip_inflows",
    "fact_category_inflows",
    "fact_folio_count",
    "fact_performance",
    "fact_transactions",
    "fact_portfolio_holdings",
    "fact_benchmark_indices"
]

cursor = conn.cursor()

for table in tables:
    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cursor.fetchone()[0]

    print(f"{table}: {count}")


# =========================================================
# 14. CLOSE DATABASE
# =========================================================

conn.commit()
conn.close()

print("\n========================================")
print("DATABASE CREATED AND DATA LOADED!")
print("========================================")