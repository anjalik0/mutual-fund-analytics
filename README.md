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
