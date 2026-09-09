# Day 1 Data Quality Summary

## Dataset Inspection

A total of **10 CSV datasets** were inspected using Pandas.

For each dataset, the following aspects were inspected:

* Number of rows and columns
* Data types
* First five records
* Missing values
* Dataset structure
* Potential data-quality issues

The datasets were successfully loaded from the `data/raw` directory.

## Dataset Summary

The 10 datasets inspected were:

1. `01_fund_master.csv`
2. `02_nav_history.csv`
3. `03_aum_by_fund_house.csv`
4. `04_monthly_sip_inflows.csv`
5. `05_category_inflows.csv`
6. `06_industry_folio_count.csv`
7. `07_scheme_performance.csv`
8. `08_investor_transactions.csv`
9. `09_portfolio_holdings.csv`
10. `10_benchmark_indices.csv`

## Fund Master

The fund master dataset contains **40 fund schemes**.

The following attributes were explored:

* Fund houses
* Categories
* Sub-categories
* Risk categories
* AMFI scheme codes

There are **10 unique fund houses**.

The available fund categories are:

* Equity
* Debt

There are **12 sub-categories**.

The available risk categories are:

* Low
* Moderate
* Moderately High
* High
* Very High

## AMFI Code Validation

AMFI scheme codes from `01_fund_master.csv` were compared against the AMFI codes available in `02_nav_history.csv`.

* Total fund master codes: **40**
* Total NAV history codes: **40**
* Missing AMFI codes: **0**

Therefore, all AMFI scheme codes present in the fund master dataset have corresponding records in the NAV history dataset.

## Missing Values

Most datasets did not contain missing values.

One identified issue was found in:

`04_monthly_sip_inflows.csv`

The column `yoy_growth_pct` contains **12 missing values**.

These missing values will be investigated during the data-cleaning and transformation stage.

No missing values were found in the other inspected datasets.

## Anomalies

The following data-quality observations were identified:

* `04_monthly_sip_inflows.csv` contains 12 missing values in `yoy_growth_pct`.
* During live NAV API validation, several provided scheme codes returned fund metadata that did not match the expected fund names. This indicates a possible current API scheme-code mapping issue and should be investigated before using those live NAV files for analysis.
* Duplicate-record counts have not yet been separately validated and will be checked during further data-quality analysis.

## Conclusion

The Day 1 data ingestion and initial validation process was completed successfully.

All **10 CSV datasets** were successfully loaded and inspected. The fund master contains **40 schemes**, and all **40 AMFI scheme codes** have corresponding codes in the NAV history dataset.

The main identified data-quality issue is the presence of **12 missing `yoy_growth_pct` values** in the monthly SIP inflows dataset. The live NAV API also showed scheme-code mapping inconsistencies that require further investigation.

These issues will be handled during the data-cleaning, validation, and transformation stages.

Day2

# Bluestock Mutual Fund Analytics

## Project Overview

This project analyzes mutual fund data using Python, Pandas, SQLite, and SQL.

The project covers data cleaning, database creation, SQL analytics, and fund performance analysis.

## Project Objectives

* Clean and validate mutual fund datasets
* Store cleaned data in a SQLite database
* Design a star-schema database
* Perform analytical queries using SQL
* Analyze fund performance, NAV, AUM, SIP inflows, and investor transactions

## Project Structure

```text
mutual-fund-analytics/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── sql/
│   ├── schema.sql
│   └── analytical_queries.sql
├── scripts/
│   ├── clean_data.py
│   └── create_database.py
├── dashboard/
├── bluestock_mf.db
├── README.md
└── requirements.txt
```

## Technologies Used

* Python
* Pandas
* SQLite
* SQL
* Jupyter Notebook
* Git & GitHub

## Database

The SQLite database is:

`bluestock_mf.db`

Main tables include:

* `dim_fund`
* `dim_date`
* `fact_nav`
* `fact_transactions`
* `fact_performance`
* `fact_aum`
* `fact_sip_inflows`
* `fact_category_inflows`
* `fact_folio_count`
* `fact_portfolio_holdings`
* `fact_benchmark_indices`

## Data Processing

The raw datasets were cleaned and validated using Python and Pandas.

The cleaned datasets are stored in:

`data/processed/`

## SQL Analytics

Analytical SQL queries were created to answer questions such as:

1. Top 5 funds by AUM
2. Average NAV per month
3. SIP year-over-year growth
4. Transactions by state
5. Funds with expense ratio below 1%
6. Average return by fund category
7. Most popular transaction type
8. Monthly transaction volume
9. AUM growth over time
10. Funds with highest 1-year return

## Database Validation

The database contains:

* 40 funds
* 1,306 dates
* 46,000 NAV records
* 32,778 transaction records
* 40 performance records
* 90 AUM records
* 48 SIP inflow records
* 144 category inflow records
* 21 folio records
* 322 portfolio holding records
* 8,050 benchmark index records

## Status

Data cleaning, SQLite database creation, schema implementation, and SQL analytical queries have been completed.

DAY3
# Fund Performance Analytics

## Project Overview
This project analyzes the performance of 40 mutual fund schemes using historical NAV data.

## Tasks Completed
- Daily Returns
- CAGR (1Y, 3Y, 5Y)
- Sharpe Ratio
- Sortino Ratio
- Alpha & Beta
- Maximum Drawdown
- Fund Scorecard
- Benchmark Comparison
- Tracking Error

## Deliverables
- Performance_Analytics.ipynb
- fund_scorecard.csv
- alpha_beta.csv
- benchmark_comparison.png
- tracking_error.csv

## Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- SciPy
- SQLite

## How to Run
1. Clone the repository.
2. Install required Python libraries.
3. Open `notebooks/Performance_Analytics.ipynb`.
4. Run all cells.