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
# 1. LOAD ALL CLEANED CSV FILES
# =========================================================

print("\nReading cleaned CSV files...")

fund = pd.read_csv(
    PROCESSED_DIR / "01_fund_master_cleaned.csv"
)

nav = pd.read_csv(
    PROCESSED_DIR / "02_nav_history_cleaned.csv"
)

aum = pd.read_csv(
    PROCESSED_DIR / "03_aum_by_fund_house_cleaned.csv"
)

sip = pd.read_csv(
    PROCESSED_DIR / "04_monthly_sip_inflows_cleaned.csv"
)

category = pd.read_csv(
    PROCESSED_DIR / "05_category_inflows_cleaned.csv"
)

folio = pd.read_csv(
    PROCESSED_DIR / "06_industry_folio_count_cleaned.csv"
)

performance = pd.read_csv(
    PROCESSED_DIR / "07_scheme_performance_cleaned.csv"
)

transactions = pd.read_csv(
    PROCESSED_DIR / "08_investor_transactions_cleaned.csv"
)

holdings = pd.read_csv(
    PROCESSED_DIR / "09_portfolio_holdings_cleaned.csv"
)

benchmark = pd.read_csv(
    PROCESSED_DIR / "10_benchmark_indices_cleaned.csv"
)

print("All 10 cleaned CSV files loaded successfully!")


# =========================================================
# 2. LOAD DIM_FUND
# =========================================================

print("\nLoading dim_fund...")

fund_columns = [
    "amfi_code",
    "fund_house",
    "scheme_name",
    "category",
    "sub_category",
    "plan",
    "launch_date",
    "benchmark",
    "expense_ratio_pct",
    "exit_load_pct",
    "min_sip_amount",
    "min_lumpsum_amount",
    "fund_manager",
    "risk_category",
    "sebi_category_code"
]

dim_fund = fund[fund_columns].copy()

dim_fund.to_sql(
    "dim_fund",
    conn,
    if_exists="append",
    index=False
)

print("dim_fund rows:", len(dim_fund))


# =========================================================
# 3. CREATE DIM_DATE
# =========================================================

print("\nCreating dim_date...")

date_sets = []

# NAV dates
date_sets.append(
    pd.to_datetime(nav["date"], errors="coerce")
)

# Transaction dates
date_sets.append(
    pd.to_datetime(
        transactions["transaction_date"],
        errors="coerce"
    )
)

# AUM dates
date_sets.append(
    pd.to_datetime(aum["date"], errors="coerce")
)

# SIP monthly dates
date_sets.append(
    pd.to_datetime(sip["month"], errors="coerce")
)

# Category inflow monthly dates
date_sets.append(
    pd.to_datetime(category["month"], errors="coerce")
)

# Folio monthly dates
date_sets.append(
    pd.to_datetime(folio["month"], errors="coerce")
)

# Portfolio dates
date_sets.append(
    pd.to_datetime(
        holdings["portfolio_date"],
        errors="coerce"
    )
)

# Benchmark dates
date_sets.append(
    pd.to_datetime(
        benchmark["date"],
        errors="coerce"
    )
)


# Combine all dates
all_dates = pd.concat(
    date_sets,
    ignore_index=True
)

all_dates = (
    all_dates
    .dropna()
    .drop_duplicates()
    .sort_values()
    .reset_index(drop=True)
)


# Create date dimension
dim_date = pd.DataFrame({
    "date_id": all_dates.dt.strftime("%Y%m%d").astype(int),
    "date": all_dates.dt.strftime("%Y-%m-%d"),
    "year": all_dates.dt.year,
    "month": all_dates.dt.month,
    "month_name": all_dates.dt.month_name(),
    "quarter": all_dates.dt.quarter
})


dim_date.to_sql(
    "dim_date",
    conn,
    if_exists="append",
    index=False
)

print("dim_date rows:", len(dim_date))


# =========================================================
# 4. LOAD FACT_NAV
# =========================================================

print("\nLoading fact_nav...")

nav["date"] = pd.to_datetime(
    nav["date"],
    errors="coerce"
)

nav["date_id"] = (
    nav["date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

fact_nav = nav[
    [
        "amfi_code",
        "date_id",
        "nav"
    ]
].copy()


fact_nav.to_sql(
    "fact_nav",
    conn,
    if_exists="append",
    index=False
)

print("fact_nav rows:", len(fact_nav))


# =========================================================
# 5. LOAD FACT_TRANSACTIONS
# =========================================================

print("\nLoading fact_transactions...")

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"],
    errors="coerce"
)

transactions["transaction_date_id"] = (
    transactions["transaction_date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

fact_transactions = transactions[
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
].copy()


fact_transactions.to_sql(
    "fact_transactions",
    conn,
    if_exists="append",
    index=False
)

print(
    "fact_transactions rows:",
    len(fact_transactions)
)


# =========================================================
# 6. LOAD FACT_PERFORMANCE
# =========================================================

print("\nLoading fact_performance...")

# Remove validation helper column if present
if "expense_ratio_anomaly" in performance.columns:
    performance = performance.drop(
        columns=["expense_ratio_anomaly"]
    )


fact_performance = performance[
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
].copy()


fact_performance.to_sql(
    "fact_performance",
    conn,
    if_exists="append",
    index=False
)

print(
    "fact_performance rows:",
    len(fact_performance)
)


# =========================================================
# 7. LOAD FACT_AUM
# =========================================================

print("\nLoading fact_aum...")

aum["date"] = pd.to_datetime(
    aum["date"],
    errors="coerce"
)

aum["date_id"] = (
    aum["date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

fact_aum = aum[
    [
        "date_id",
        "fund_house",
        "aum_lakh_crore",
        "aum_crore",
        "num_schemes"
    ]
].copy()


fact_aum.to_sql(
    "fact_aum",
    conn,
    if_exists="append",
    index=False
)

print("fact_aum rows:", len(fact_aum))


# =========================================================
# 8. LOAD FACT_SIP_INFLOWS
# =========================================================

print("\nLoading fact_sip_inflows...")

sip["month"] = pd.to_datetime(
    sip["month"],
    errors="coerce"
)

sip["date_id"] = (
    sip["month"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

fact_sip = sip[
    [
        "date_id",
        "sip_inflow_crore",
        "active_sip_accounts_crore",
        "new_sip_accounts_lakh",
        "sip_aum_lakh_crore",
        "yoy_growth_pct"
    ]
].copy()


fact_sip.to_sql(
    "fact_sip_inflows",
    conn,
    if_exists="append",
    index=False
)

print("fact_sip_inflows rows:", len(fact_sip))


# =========================================================
# 9. LOAD FACT_CATEGORY_INFLOWS
# =========================================================

print("\nLoading fact_category_inflows...")

category["month"] = pd.to_datetime(
    category["month"],
    errors="coerce"
)

category["date_id"] = (
    category["month"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

fact_category = category[
    [
        "date_id",
        "category",
        "net_inflow_crore"
    ]
].copy()


fact_category.to_sql(
    "fact_category_inflows",
    conn,
    if_exists="append",
    index=False
)

print(
    "fact_category_inflows rows:",
    len(fact_category)
)


# =========================================================
# 10. LOAD FACT_FOLIO_COUNT
# =========================================================

print("\nLoading fact_folio_count...")

folio["month"] = pd.to_datetime(
    folio["month"],
    errors="coerce"
)

folio["date_id"] = (
    folio["month"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

fact_folio = folio[
    [
        "date_id",
        "total_folios_crore",
        "equity_folios_crore",
        "debt_folios_crore",
        "hybrid_folios_crore",
        "others_folios_crore"
    ]
].copy()


fact_folio.to_sql(
    "fact_folio_count",
    conn,
    if_exists="append",
    index=False
)

print(
    "fact_folio_count rows:",
    len(fact_folio)
)


# =========================================================
# 11. LOAD FACT_PORTFOLIO_HOLDINGS
# =========================================================

print("\nLoading fact_portfolio_holdings...")

holdings["portfolio_date"] = pd.to_datetime(
    holdings["portfolio_date"],
    errors="coerce"
)

holdings["portfolio_date_id"] = (
    holdings["portfolio_date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

fact_holdings = holdings[
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
].copy()


fact_holdings.to_sql(
    "fact_portfolio_holdings",
    conn,
    if_exists="append",
    index=False
)

print(
    "fact_portfolio_holdings rows:",
    len(fact_holdings)
)


# =========================================================
# 12. LOAD FACT_BENCHMARK_INDICES
# =========================================================

print("\nLoading fact_benchmark_indices...")

benchmark["date"] = pd.to_datetime(
    benchmark["date"],
    errors="coerce"
)

benchmark["date_id"] = (
    benchmark["date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

fact_benchmark = benchmark[
    [
        "date_id",
        "index_name",
        "close_value"
    ]
].copy()


fact_benchmark.to_sql(
    "fact_benchmark_indices",
    conn,
    if_exists="append",
    index=False
)

print(
    "fact_benchmark_indices rows:",
    len(fact_benchmark)
)


# =========================================================
# 13. VERIFY ROW COUNTS
# =========================================================

print("\n" + "=" * 65)
print("DATABASE ROW COUNT VERIFICATION")
print("=" * 65)

tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum",
    "fact_sip_inflows",
    "fact_category_inflows",
    "fact_folio_count",
    "fact_portfolio_holdings",
    "fact_benchmark_indices"
]

for table in tables:

    result = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()

    print(f"{table}: {result[0]} rows")


# =========================================================
# 14. CLOSE DATABASE
# =========================================================

conn.close()

print("\n" + "=" * 65)
print("ALL 10 DATASETS LOADED SUCCESSFULLY!")
print("=" * 65)