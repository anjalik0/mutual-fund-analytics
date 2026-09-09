import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

# Create processed folder if it doesn't exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# 1. NAV HISTORY
# =========================================================

print("\n" + "=" * 60)
print("1. CLEANING NAV HISTORY")
print("=" * 60)

nav = pd.read_csv(RAW_DIR / "02_nav_history.csv")

print("Original rows:", len(nav))

# Convert date
nav["date"] = pd.to_datetime(
    nav["date"],
    errors="coerce"
)

# Convert NAV to numeric
nav["nav"] = pd.to_numeric(
    nav["nav"],
    errors="coerce"
)

# Remove rows with invalid dates
nav = nav.dropna(subset=["date"])

# Sort by fund and date
nav = nav.sort_values(
    ["amfi_code", "date"]
)

# Remove duplicate fund/date combinations
nav = nav.drop_duplicates(
    subset=["amfi_code", "date"],
    keep="last"
)

# Forward fill missing NAV within each fund
nav["nav"] = (
    nav.groupby("amfi_code")["nav"]
    .ffill()
)

# Remove invalid NAV values
nav = nav[nav["nav"] > 0]

# Save cleaned file
nav.to_csv(
    PROCESSED_DIR / "02_nav_history_cleaned.csv",
    index=False
)

print("Cleaned rows:", len(nav))
print("Missing NAV:", nav["nav"].isna().sum())
print("Invalid NAV:", (nav["nav"] <= 0).sum())


# =========================================================
# 2. INVESTOR TRANSACTIONS
# =========================================================

print("\n" + "=" * 60)
print("2. CLEANING INVESTOR TRANSACTIONS")
print("=" * 60)

transactions = pd.read_csv(
    RAW_DIR / "08_investor_transactions.csv"
)

print("Original rows:", len(transactions))

# Convert transaction date
transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"],
    errors="coerce"
)

# Convert amount to numeric
transactions["amount_inr"] = pd.to_numeric(
    transactions["amount_inr"],
    errors="coerce"
)

# Standardize transaction types
transactions["transaction_type"] = (
    transactions["transaction_type"]
    .astype(str)
    .str.strip()
    .str.lower()
)

transaction_mapping = {
    "sip": "SIP",
    "lumpsum": "Lumpsum",
    "lump sum": "Lumpsum",
    "lump-sum": "Lumpsum",
    "redemption": "Redemption",
    "redeem": "Redemption"
}

transactions["transaction_type"] = (
    transactions["transaction_type"]
    .map(transaction_mapping)
)

# Check unknown transaction types
print(
    "Unknown transaction types:",
    transactions["transaction_type"].isna().sum()
)

# Remove invalid dates
transactions = transactions.dropna(
    subset=["transaction_date"]
)

# Keep only positive transaction amounts
transactions = transactions[
    transactions["amount_inr"] > 0
]

# Check KYC values
print(
    "KYC values:",
    transactions["kyc_status"].unique()
)

# Remove exact duplicate transactions
transactions = transactions.drop_duplicates()

# Save
transactions.to_csv(
    PROCESSED_DIR / "08_investor_transactions_cleaned.csv",
    index=False
)

print("Cleaned rows:", len(transactions))


# =========================================================
# 3. SCHEME PERFORMANCE
# =========================================================

print("\n" + "=" * 60)
print("3. CLEANING SCHEME PERFORMANCE")
print("=" * 60)

performance = pd.read_csv(
    RAW_DIR / "07_scheme_performance.csv"
)

print("Original rows:", len(performance))

# Numeric performance columns
numeric_columns = [
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
    "morningstar_rating"
]

for column in numeric_columns:
    performance[column] = pd.to_numeric(
        performance[column],
        errors="coerce"
    )

# Expense ratio validation
performance["expense_ratio_anomaly"] = ~(
    performance["expense_ratio_pct"].between(
        0.1,
        2.5
    )
)

print(
    "Expense ratio anomalies:",
    performance["expense_ratio_anomaly"].sum()
)

# Return validation
return_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct"
]

for column in return_columns:
    print(
        column,
        "missing/non-numeric:",
        performance[column].isna().sum()
    )

# Remove exact duplicates
performance = performance.drop_duplicates()

# Save
performance.to_csv(
    PROCESSED_DIR / "07_scheme_performance_cleaned.csv",
    index=False
)

print("Cleaned rows:", len(performance))


# =========================================================
# 4. FUND MASTER
# =========================================================

print("\n" + "=" * 60)
print("4. CLEANING FUND MASTER")
print("=" * 60)

fund = pd.read_csv(
    RAW_DIR / "01_fund_master.csv"
)

fund["launch_date"] = pd.to_datetime(
    fund["launch_date"],
    errors="coerce"
)

fund = fund.drop_duplicates(
    subset=["amfi_code"],
    keep="last"
)

fund.to_csv(
    PROCESSED_DIR / "01_fund_master_cleaned.csv",
    index=False
)

print("Rows:", len(fund))


# =========================================================
# 5. AUM BY FUND HOUSE
# =========================================================

print("\n" + "=" * 60)
print("5. CLEANING AUM DATA")
print("=" * 60)

aum = pd.read_csv(
    RAW_DIR / "03_aum_by_fund_house.csv"
)

aum["date"] = pd.to_datetime(
    aum["date"],
    errors="coerce"
)

numeric_columns = [
    "aum_lakh_crore",
    "aum_crore",
    "num_schemes"
]

for column in numeric_columns:
    aum[column] = pd.to_numeric(
        aum[column],
        errors="coerce"
    )

aum = aum.dropna(subset=["date"])
aum = aum.drop_duplicates()

aum.to_csv(
    PROCESSED_DIR / "03_aum_by_fund_house_cleaned.csv",
    index=False
)

print("Rows:", len(aum))


# =========================================================
# 6. MONTHLY SIP INFLOWS
# =========================================================

print("\n" + "=" * 60)
print("6. CLEANING SIP INFLOWS")
print("=" * 60)

sip = pd.read_csv(
    RAW_DIR / "04_monthly_sip_inflows.csv"
)

sip["month"] = pd.to_datetime(
    sip["month"],
    errors="coerce"
)

numeric_columns = [
    "sip_inflow_crore",
    "active_sip_accounts_crore",
    "new_sip_accounts_lakh",
    "sip_aum_lakh_crore",
    "yoy_growth_pct"
]

for column in numeric_columns:
    sip[column] = pd.to_numeric(
        sip[column],
        errors="coerce"
    )

# Do NOT fill missing YoY values.
# First-year YoY can naturally be unavailable.

sip = sip.dropna(subset=["month"])
sip = sip.drop_duplicates()

sip.to_csv(
    PROCESSED_DIR / "04_monthly_sip_inflows_cleaned.csv",
    index=False
)

print("Rows:", len(sip))


# =========================================================
# 7. CATEGORY INFLOWS
# =========================================================

print("\n" + "=" * 60)
print("7. CLEANING CATEGORY INFLOWS")
print("=" * 60)

category = pd.read_csv(
    RAW_DIR / "05_category_inflows.csv"
)

category["month"] = pd.to_datetime(
    category["month"],
    errors="coerce"
)

category["net_inflow_crore"] = pd.to_numeric(
    category["net_inflow_crore"],
    errors="coerce"
)

category = category.dropna(subset=["month"])
category = category.drop_duplicates()

category.to_csv(
    PROCESSED_DIR / "05_category_inflows_cleaned.csv",
    index=False
)

print("Rows:", len(category))


# =========================================================
# 8. INDUSTRY FOLIO COUNT
# =========================================================

print("\n" + "=" * 60)
print("8. CLEANING FOLIO DATA")
print("=" * 60)

folio = pd.read_csv(
    RAW_DIR / "06_industry_folio_count.csv"
)

folio["month"] = pd.to_datetime(
    folio["month"],
    errors="coerce"
)

numeric_columns = [
    "total_folios_crore",
    "equity_folios_crore",
    "debt_folios_crore",
    "hybrid_folios_crore",
    "others_folios_crore"
]

for column in numeric_columns:
    folio[column] = pd.to_numeric(
        folio[column],
        errors="coerce"
    )

folio = folio.dropna(subset=["month"])
folio = folio.drop_duplicates()

folio.to_csv(
    PROCESSED_DIR / "06_industry_folio_count_cleaned.csv",
    index=False
)

print("Rows:", len(folio))


# =========================================================
# 9. PORTFOLIO HOLDINGS
# =========================================================

print("\n" + "=" * 60)
print("9. CLEANING PORTFOLIO HOLDINGS")
print("=" * 60)

holdings = pd.read_csv(
    RAW_DIR / "09_portfolio_holdings.csv"
)

holdings["portfolio_date"] = pd.to_datetime(
    holdings["portfolio_date"],
    errors="coerce"
)

numeric_columns = [
    "weight_pct",
    "market_value_cr",
    "current_price_inr"
]

for column in numeric_columns:
    holdings[column] = pd.to_numeric(
        holdings[column],
        errors="coerce"
    )

holdings = holdings.dropna(
    subset=["portfolio_date"]
)

holdings = holdings.drop_duplicates()

holdings.to_csv(
    PROCESSED_DIR / "09_portfolio_holdings_cleaned.csv",
    index=False
)

print("Rows:", len(holdings))


# =========================================================
# 10. BENCHMARK INDICES
# =========================================================

print("\n" + "=" * 60)
print("10. CLEANING BENCHMARK INDICES")
print("=" * 60)

benchmark = pd.read_csv(
    RAW_DIR / "10_benchmark_indices.csv"
)

benchmark["date"] = pd.to_datetime(
    benchmark["date"],
    errors="coerce"
)

benchmark["close_value"] = pd.to_numeric(
    benchmark["close_value"],
    errors="coerce"
)

benchmark = benchmark.dropna(
    subset=["date"]
)

benchmark = benchmark[
    benchmark["close_value"] > 0
]

benchmark = benchmark.drop_duplicates()

benchmark.to_csv(
    PROCESSED_DIR / "10_benchmark_indices_cleaned.csv",
    index=False
)

print("Rows:", len(benchmark))


# =========================================================
# COMPLETED
# =========================================================

print("\n" + "=" * 60)
print("DAY 2 CLEANING COMPLETED")
print("=" * 60)

print(
    "Cleaned files saved in:",
    PROCESSED_DIR
)