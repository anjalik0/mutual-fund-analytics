-- =========================================================
-- MUTUAL FUND ANALYTICS - STAR SCHEMA
-- =========================================================

-- Remove existing tables if they exist
DROP TABLE IF EXISTS fact_benchmark_indices;
DROP TABLE IF EXISTS fact_portfolio_holdings;
DROP TABLE IF EXISTS fact_folio_count;
DROP TABLE IF EXISTS fact_category_inflows;
DROP TABLE IF EXISTS fact_sip_inflows;
DROP TABLE IF EXISTS fact_nav;
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS fact_aum;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_fund;


-- =========================================================
-- 1. DIMENSION: FUND
-- =========================================================

CREATE TABLE dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    fund_house TEXT NOT NULL,
    scheme_name TEXT NOT NULL,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    launch_date DATE,
    benchmark TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    min_sip_amount INTEGER,
    min_lumpsum_amount INTEGER,
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);


-- =========================================================
-- 2. DIMENSION: DATE
-- =========================================================

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    year INTEGER,
    month INTEGER,
    month_name TEXT,
    quarter INTEGER
);


-- =========================================================
-- 3. FACT: NAV
-- =========================================================

CREATE TABLE fact_nav (
    amfi_code INTEGER NOT NULL,
    date_id INTEGER NOT NULL,
    nav REAL NOT NULL,

    PRIMARY KEY (amfi_code, date_id),

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);


-- =========================================================
-- 4. FACT: INVESTOR TRANSACTIONS
-- =========================================================

CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT NOT NULL,
    transaction_date_id INTEGER NOT NULL,
    amfi_code INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,
    amount_inr REAL NOT NULL,
    state TEXT,
    city TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL,
    payment_mode TEXT,
    kyc_status TEXT,

    FOREIGN KEY (transaction_date_id)
        REFERENCES dim_date(date_id),

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code)
);


-- =========================================================
-- 5. FACT: SCHEME PERFORMANCE
-- =========================================================

CREATE TABLE fact_performance (
    amfi_code INTEGER PRIMARY KEY,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    benchmark_3yr_pct REAL,
    alpha REAL,
    beta REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    std_dev_ann_pct REAL,
    max_drawdown_pct REAL,
    aum_crore REAL,
    expense_ratio_pct REAL,
    morningstar_rating INTEGER,
    risk_grade TEXT,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code)
);


-- =========================================================
-- 6. FACT: AUM
-- =========================================================

CREATE TABLE fact_aum (
    date_id INTEGER NOT NULL,
    fund_house TEXT NOT NULL,
    aum_lakh_crore REAL,
    aum_crore REAL,
    num_schemes INTEGER,

    PRIMARY KEY (date_id, fund_house),

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);


-- =========================================================
-- 7. FACT: MONTHLY SIP INFLOWS
-- CSV: 04_monthly_sip_inflows.csv
-- =========================================================

CREATE TABLE fact_sip_inflows (
    date_id INTEGER PRIMARY KEY,
    sip_inflow_crore REAL,
    active_sip_accounts_crore REAL,
    new_sip_accounts_lakh REAL,
    sip_aum_lakh_crore REAL,
    yoy_growth_pct REAL,

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);


-- =========================================================
-- 8. FACT: CATEGORY INFLOWS
-- CSV: 05_category_inflows.csv
-- =========================================================

CREATE TABLE fact_category_inflows (
    date_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    net_inflow_crore REAL,

    PRIMARY KEY (date_id, category),

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);


-- =========================================================
-- 9. FACT: INDUSTRY FOLIO COUNT
-- CSV: 06_industry_folio_count.csv
-- =========================================================

CREATE TABLE fact_folio_count (
    date_id INTEGER PRIMARY KEY,
    total_folios_crore REAL,
    equity_folios_crore REAL,
    debt_folios_crore REAL,
    hybrid_folios_crore REAL,
    others_folios_crore REAL,

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);


-- =========================================================
-- 10. FACT: PORTFOLIO HOLDINGS
-- CSV: 09_portfolio_holdings.csv
-- =========================================================

CREATE TABLE fact_portfolio_holdings (
    amfi_code INTEGER NOT NULL,
    stock_symbol TEXT NOT NULL,
    stock_name TEXT,
    sector TEXT,
    weight_pct REAL,
    market_value_cr REAL,
    current_price_inr REAL,
    portfolio_date_id INTEGER NOT NULL,

    PRIMARY KEY (
        amfi_code,
        stock_symbol,
        portfolio_date_id
    ),

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (portfolio_date_id)
        REFERENCES dim_date(date_id)
);


-- =========================================================
-- 11. FACT: BENCHMARK INDICES
-- CSV: 10_benchmark_indices.csv
-- =========================================================

CREATE TABLE fact_benchmark_indices (
    date_id INTEGER NOT NULL,
    index_name TEXT NOT NULL,
    close_value REAL NOT NULL,

    PRIMARY KEY (date_id, index_name),

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);