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
