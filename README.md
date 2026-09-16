# Bluestock Mutual Fund Analytics

# DAY 1 — Project Setup + Data Ingestion (ETL)

## Overview

Day 1 focused on setting up the Mutual Fund Analytics project, configuring the development environment, ingesting the provided datasets, integrating live NAV data through MFAPI, and performing initial data exploration and validation.

## Tasks Completed

* Created the project structure with `data/raw`, `data/processed`, `notebooks`, `sql`, `dashboard`, and `reports`.
* Initialized Git and connected the project to GitHub.
* Installed the required Python dependencies and created `requirements.txt`.
* Loaded and inspected all **10 provided CSV datasets** using Pandas.
* Checked dataset shape, data types, sample records, and initial data-quality observations.
* Integrated the **MFAPI** to fetch live NAV data for HDFC Top 100 Direct (`125497`) and saved the response as raw CSV data.
* Fetched NAV data for five key schemes:

  * SBI Bluechip — `119551`
  * ICICI Bluechip — `120503`
  * Nippon Large Cap — `118632`
  * Axis Bluechip — `119092`
  * Kotak Bluechip — `120841`
* Explored the fund master dataset, including fund houses, categories, sub-categories, risk grades, and AMFI scheme codes.
* Validated AMFI codes between the fund master and NAV history datasets.

## Key Findings

* **40 mutual fund schemes** were identified in the fund master dataset.
* **40 AMFI codes** were present in both the fund master and NAV history datasets.
* **0 AMFI codes were missing** from NAV history.
* Initial dataset anomalies and data-quality observations were documented for further processing.

## Files & Deliverables

```text
data/
└── raw/
    ├── 01_fund_master.csv
    ├── 02_nav_history.csv
    ├── 03_aum_by_fund_house.csv
    ├── 04_monthly_sip_inflows.csv
    ├── 05_category_inflows.csv
    ├── 06_industry_folio_count.csv
    ├── 07_scheme_performance.csv
    ├── 08_investor_transactions.csv
    ├── 09_portfolio_holdings.csv
    ├── 10_benchmark_indices.csv
    └── live_nav_125497.csv

notebooks/
└──Data_Ingestion.ipynb

data_ingestion.py
live_nav_fetch.py
requirements.txt
```

## Git Commit

```text
Day 1: Data ingestion complete
```

## Status

**Day 1 — Completed ✅**




# DAY 2 — Data Cleaning + SQL Database Design

## Overview

Day 2 focused on cleaning and validating the mutual fund datasets, designing a SQLite star schema, loading the cleaned data into the database, creating analytical SQL queries, and documenting the database fields.

## Tasks Completed

* Cleaned `nav_history.csv` by:

  * Converting dates to datetime format
  * Sorting records by `amfi_code` and date
  * Handling missing NAV values
  * Removing duplicate records
  * Validating NAV values greater than zero

* Cleaned `investor_transactions.csv` by:

  * Standardizing transaction types into **SIP, Lumpsum, and Redemption**
  * Validating transaction amounts
  * Standardizing date formats
  * Checking KYC status values

* Cleaned `scheme_performance.csv` by:

  * Validating return columns as numeric
  * Identifying potential anomalies
  * Validating expense-ratio values against the expected **0.1%–2.5%** range

* Designed a **SQLite star schema** with dimension and fact tables:

  * `dim_fund`
  * `dim_date`
  * `fact_nav`
  * `fact_transactions`
  * `fact_performance`
  * `fact_aum`

* Defined primary keys and foreign-key relationships between the database tables.

* Loaded the cleaned datasets into `bluestock_mf.db` using **SQLAlchemy** and Pandas `to_sql()`.

* Verified database row counts against the processed source datasets.

* Created **10 analytical SQL queries**, including:

  * Top 5 funds by AUM
  * Average NAV per month
  * SIP year-over-year growth
  * Transactions by state
  * Funds with expense ratio below 1%
  * Additional fund, transaction, and performance analysis queries

* Created a data dictionary documenting:

  * Column names
  * Data types
  * Business definitions
  * Source references

## Database Structure

```text
Raw CSV Data
      ↓
Data Cleaning & Validation
      ↓
Processed CSV Data
      ↓
SQLite Database
      ↓
SQL Analytical Queries
```

### Main Database Tables

| Type      | Tables                                                          |
| --------- | --------------------------------------------------------------- |
| Dimension | `dim_fund`, `dim_date`                                          |
| Fact      | `fact_nav`, `fact_transactions`, `fact_performance`, `fact_aum` |

## Files & Deliverables

```text
data/
└── processed/
    ├── 10 cleaned CSV files

sql/
├── schema.sql
└── queries.sql

notebooks/
└── Day2_Data_Cleaning_SQL.ipynb

data_dictionary.md
bluestock_mf.db
```

## Git Commit

```text
Day 2: Cleaned data + SQLite DB loaded
```

## Status

**Day 2 — Completed ✅**

Data cleaning, validation, SQLite database creation, schema implementation, data loading, and SQL analytical queries have been completed successfully.

# DAY 3 — Fund Performance Analytics

## Overview

Day 3 focused on evaluating the performance and risk of the 40 mutual fund schemes using historical NAV data, risk-adjusted performance metrics, benchmark comparison, and a composite fund scorecard.

## Tasks Completed

* Computed **daily returns** for all 40 schemes using consecutive NAV values and validated the return distribution.
* Calculated **1-year, 3-year, and 5-year CAGR** for each fund and created a comparison table.
* Calculated the **Sharpe Ratio** using a 6.5% annual risk-free rate and annualized daily returns using 252 trading days.
* Calculated the **Sortino Ratio** using downside volatility to measure risk-adjusted returns.
* Performed **Alpha and Beta analysis** using OLS regression of fund returns against the **Nifty 100** benchmark.
* Calculated **Maximum Drawdown** for each fund and identified the corresponding worst drawdown period.
* Created a **0–100 Fund Scorecard** using weighted rankings based on:

  * 3-year return — 30%
  * Sharpe Ratio — 25%
  * Alpha — 20%
  * Expense Ratio — 15% (inverse ranking)
  * Maximum Drawdown — 10% (inverse ranking)
* Compared the **top 5 funds** against Nifty 50 and Nifty 100 over a 3-year period.
* Calculated **Tracking Error** to measure the deviation of fund returns from the benchmark.

## Key Results

* Daily return analysis was completed for **45,960 fund observations**.
* Average daily return: **0.0631%**
* Daily return standard deviation: **1.0290%**
* Annual risk-free rate used: **6.5%**
* Top CAGR results included:

  * ICICI Prudential Midcap — **32.83%**
  * SBI Small Cap — **32.42%**
  * DSP Small Cap — **32.29%**
* Performance and risk metrics were consolidated into the final fund scorecard.

## Files & Deliverables

```text
notebooks/
└── Performance_Analytics.ipynb

outputs/
└── performance/
    ├── fund_scorecard.csv
    ├── alpha_beta.csv
    ├── tracking_error.csv
    ├── benchmark_comparison.png
    └── drawdown.png
```

## Git Commit

```text
Day 3: Fund performance analytics complete
```

## Status

**Day 3 — Completed ✅**


The fund performance and risk analysis was completed successfully, providing a structured view of historical returns, risk, benchmark relationships, and downside performance across the analyzed mutual fund schemes.


# DAY 4 — Exploratory Data Analysis (EDA)

## Overview

Day 4 focused on performing comprehensive Exploratory Data Analysis (EDA) on mutual fund performance, AUM, SIP inflows, investor demographics, geographic distribution, folio growth, fund correlations, and sector allocation. Interactive and statistical visualizations were created to identify important trends and patterns in the data.

## Tasks Completed

* Analyzed daily **NAV trends for all 40 schemes** from 2022–2026 and highlighted the 2023 bull run and 2024 market corrections.
* Created **AUM growth analysis by fund house** for 2022–2025, including SBI's ₹12.5L Cr AUM in 2025.
* Analyzed the **monthly SIP inflow trend** from January 2022 to December 2025 and highlighted the ₹31,002 Cr all-time high in December 2025.
* Created a **category-wise inflow heatmap** to identify monthly trends across mutual fund categories.
* Analyzed **investor demographics** using age-group distribution, SIP amount by age group, and gender distribution.
* Analyzed **geographic distribution** through state-wise SIP amounts and T30 vs B30 investor distribution.
* Visualized **folio count growth** from 13.26 Cr in January 2022 to 26.12 Cr in December 2025 and identified key milestones.
* Computed the **NAV return correlation matrix** for 10 selected funds to identify relationships between fund returns.
* Created a **sector allocation donut chart** using aggregate portfolio holdings across equity funds.
* Documented **10 key EDA findings** in Jupyter Markdown cells with supporting chart references.

## Key Results

* NAV trends were analyzed across **40 mutual fund schemes** covering 2022–2026.
* SBI AUM increased from **₹6.30L Cr in 2022 to ₹12.50L Cr in 2025**.
* Monthly SIP inflows reached an all-time high of **₹31,002 Cr in December 2025**.
* Industry folios increased from **13.26 Cr to 26.12 Cr** between January 2022 and December 2025.
* Sector allocation analysis showed **Banking, IT, and Pharma** as major sectors in the aggregated equity-fund holdings.

## Files & Deliverables

```text
notebooks/
└── EDA_Analysis.ipynb

outputs/
└── eda/
    ├── nav_trends_40_funds.png
    ├── nav_trends_highlighted.png
    ├── aum_growth_by_fund_house.png
    ├── monthly_sip_inflows.png
    ├── category_inflow_heatmap.png
    ├── investor_age_distribution.png
    ├── sip_amount_by_age.png
    ├── gender_distribution.png
    ├── investor_distribution_by_state.png
    ├── investor_city_tier_distribution.png
    ├── folio_count_growth.png
    ├── nav_return_correlation.png
    └── sector_allocation_donut.png
```

## Git Commit

```text
Complete EDA analysis and charts
```

## Status

**Day 4 — Completed ✅**
