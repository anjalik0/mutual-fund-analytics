# Bluestock Mutual Fund Analytics

# DAY 1 — Data Ingestion

## Overview

Day 1 focused on collecting, loading, inspecting, and performing the initial validation of the mutual fund datasets.

The objective was to understand the structure and quality of the available data before starting the data-cleaning and database creation process.

---

## Dataset Inspection

A total of **10 CSV datasets** were inspected using Python and Pandas.

For each dataset, the following aspects were examined:

* Number of rows and columns
* Column names
* Data types
* First few records
* Missing values
* Dataset structure
* Potential data-quality issues

All datasets were successfully loaded from the:

`data/raw/`

directory.

---

## Dataset Summary

The following 10 datasets were inspected:

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

These datasets contain information related to mutual fund schemes, NAV, AUM, SIP inflows, investor transactions, portfolio holdings, folio counts, and benchmark indices.

---

## Fund Master Analysis

The `01_fund_master.csv` dataset contains information about **40 mutual fund schemes**.

The following attributes were inspected:

* Fund houses
* Fund categories
* Sub-categories
* Risk categories
* AMFI scheme codes
* Fund managers
* Benchmark information
* Expense ratios
* Exit loads

### Fund Master Summary

* **Total fund schemes:** 40
* **Unique fund houses:** 10
* **Main categories:** Equity and Debt
* **Sub-categories:** 12
* **Risk categories:** Low, Moderate, Moderately High, High, Very High

---

## AMFI Code Validation

The AMFI scheme codes from the fund master dataset were compared with the AMFI codes available in the NAV history dataset.

### Validation Results

* Fund master AMFI codes: **40**
* NAV history AMFI codes: **40**
* Missing AMFI codes: **0**

Therefore, all **40 AMFI scheme codes** present in the fund master had corresponding codes in the NAV history dataset.

This initial validation confirmed that the two datasets could be related using the AMFI scheme code.

---

## Initial Missing-Value Analysis

Missing values were checked across all 10 datasets.

Most datasets did not contain missing values.

One notable issue was identified in:

`04_monthly_sip_inflows.csv`

The column:

`yoy_growth_pct`

contains **12 missing values**.

These missing values were recorded as a data-quality issue and were planned for further investigation during the Day 2 data-cleaning stage.

---

## Initial Data-Quality Observations

The following observations were identified during the initial inspection:

### 1. Missing SIP Growth Values

The `yoy_growth_pct` column in the monthly SIP inflow dataset contains **12 missing values**.

### 2. NAV API Validation

During live NAV API validation, some provided scheme codes returned fund metadata that did not match the expected local fund names.

This indicated a possible scheme-code mapping inconsistency between the API response and the local dataset.

The issue was noted for further investigation before using live API data in analysis.

### 3. Duplicate Records

Duplicate records were not considered part of the initial ingestion analysis.

A detailed duplicate-record check was planned as part of the Day 2 data-cleaning and validation process.

---

## Data Loading

The datasets were loaded into Pandas DataFrames for inspection and further processing.

The initial workflow was:

**Raw CSV Files → Pandas DataFrames → Dataset Inspection → Initial Validation → Data Cleaning**

---

## Day 1 Outcome

By the end of Day 1:

* All **10 CSV datasets** were successfully loaded.
* Dataset structures and data types were inspected.
* The fund master dataset containing **40 schemes** was analyzed.
* Fund houses, categories, sub-categories, and risk categories were examined.
* AMFI scheme-code consistency was validated.
* All **40 fund codes** had corresponding NAV history codes.
* Missing values were identified.
* Initial data-quality issues were documented.
* The datasets were prepared for detailed cleaning and transformation on Day 2.

---

## Status

**Day 1 — Data Ingestion: Completed ✅**

The initial data ingestion, dataset inspection, and validation process was completed successfully.

The identified data-quality issues were carried forward to **Day 2 — Data Cleaning and Database Setup**.



# DAY 2 — Data Cleaning and Database Setup

## Overview

Day 2 focused on transforming the raw mutual fund datasets into clean, structured, and validated data and storing them in a relational SQLite database.

The main objective was to prepare reliable data for SQL analytics and the upcoming fund performance and exploratory data analysis.

---

## Objectives

The major objectives of Day 2 were:

* Clean and validate the raw datasets.
* Handle missing and inconsistent values.
* Standardize column names and data formats.
* Convert date columns into proper date formats.
* Remove duplicate or invalid records where required.
* Create a structured SQLite database.
* Design dimension and fact tables.
* Load processed data into the database.
* Perform database validation.
* Create SQL queries for analytical requirements.

---

## Technologies Used

* **Python**
* **Pandas**
* **SQLite**
* **SQL**
* **Jupyter Notebook**
* **Git & GitHub**

---

## Raw Datasets

The project contains multiple datasets related to mutual funds, NAV, investors, AUM, SIPs, portfolio holdings, and benchmarks.

The raw datasets are stored in:

`data/raw/`

### Main Raw Datasets

1. Fund Master
2. NAV History
3. AUM by Fund House
4. Monthly SIP Inflows
5. Category-wise Inflows
6. Industry Folio Count
7. Scheme Performance
8. Investor Transactions
9. Portfolio Holdings
10. Benchmark Indices

---

## Data Cleaning

The raw datasets were processed using **Python and Pandas**.

### Cleaning Operations

The following data-cleaning operations were performed:

* Checked dataset dimensions and column names.
* Identified missing values.
* Checked duplicate records.
* Standardized data types.
* Converted date columns into consistent formats.
* Validated numerical columns.
* Checked mutual fund identifiers for consistency.
* Checked NAV records for valid values.
* Validated transaction data.
* Standardized categorical fields.
* Verified relationships between datasets.
* Removed or handled invalid records where required.

The cleaned and processed datasets were stored in:

`data/processed/`

---

## Data Validation

After cleaning, the datasets were validated to ensure that the data was consistent and suitable for database loading.

Important validation checks included:

* Fund identifiers were checked for consistency across datasets.
* NAV records were checked against the fund master.
* Dates were checked for valid ranges.
* Numerical fields were checked for invalid values.
* Dataset record counts were verified.
* Relationships between fact and dimension tables were checked.

---

## Database Setup

A relational **SQLite database** was created to organize the processed mutual fund data.

The database file is:

`bluestock_mf.db`

The database follows a structured **fact and dimension table** approach.

---

## Database Schema

### Dimension Tables

Dimension tables store descriptive information used for analysis.

* `dim_fund` — Fund and scheme information.
* `dim_date` — Date-related information.

### Fact Tables

Fact tables store measurable business and financial data.

* `fact_nav` — Historical NAV data.
* `fact_transactions` — Investor transaction records.
* `fact_performance` — Fund performance metrics.
* `fact_aum` — Assets Under Management data.
* `fact_sip_inflows` — Monthly SIP inflows.
* `fact_category_inflows` — Category-wise inflows.
* `fact_folio_count` — Mutual fund folio counts.
* `fact_portfolio_holdings` — Portfolio holdings and sector information.
* `fact_benchmark_indices` — Benchmark index data.

---

## Database Structure

The overall data flow was:

**Raw CSV Files → Data Cleaning → Data Validation → Processed Data → SQLite Database → SQL Analytics**

This structure makes the data easier to query, analyze, and use for further financial analysis.

---

## Database Records

After processing and loading the datasets, the database contained:

| Table                     |                     Records |
| ------------------------- | --------------------------: |
| `dim_fund`                |                    40 funds |
| `dim_date`                |                 1,306 dates |
| `fact_nav`                |          46,000 NAV records |
| `fact_transactions`       |  32,778 transaction records |
| `fact_performance`        |      40 performance records |
| `fact_aum`                |              90 AUM records |
| `fact_sip_inflows`        |       48 SIP inflow records |
| `fact_category_inflows`   | 144 category inflow records |
| `fact_folio_count`        |            21 folio records |
| `fact_portfolio_holdings` |         322 holding records |
| `fact_benchmark_indices`  |     8,050 benchmark records |

---

## SQL Analytics

SQL queries were created to extract meaningful business insights from the database.

### Analytical Questions

1. What are the top 5 funds by AUM?
2. What is the average NAV per month?
3. What is the SIP year-over-year growth?
4. How many transactions occurred in each state?
5. Which funds have an expense ratio below 1%?
6. What is the average return by fund category?
7. What is the most popular transaction type?
8. What is the monthly transaction volume?
9. How has AUM changed over time?
10. Which funds have the highest 1-year return?

These queries helped verify the database structure and demonstrated how SQL can be used for financial analytics.

---

## Database Validation

The SQLite database was validated after data loading.

The validation process included:

* Checking table creation.
* Checking row counts.
* Verifying primary identifiers.
* Checking relationships between tables.
* Comparing database records with processed CSV files.
* Running sample SQL queries.
* Verifying that analytical queries returned expected results.

---

## Key Outcomes

By the end of Day 2:

* Raw mutual fund datasets were cleaned and standardized.
* Processed datasets were created.
* A structured SQLite database was implemented.
* Fact and dimension tables were created.
* Data was successfully loaded into the database.
* Database record counts were validated.
* SQL analytical queries were created and tested.
* The database became ready for further financial performance analysis and EDA.

---

## Status

**Day 2 — Data Cleaning and Database Setup: Completed ✅**

Data cleaning, validation, SQLite database creation, schema implementation, data loading, and SQL analytical queries have been completed successfully.

# DAY 3 — Fund Performance Analytics

## Overview

Day 3 focused on analyzing the historical performance of **40 mutual fund schemes** using historical NAV data and benchmark index data.

The objective was to calculate risk-adjusted performance metrics, compare funds with their benchmarks, analyze downside risk, and create a comprehensive fund performance scorecard.

---

## Objectives

The major objectives of Day 3 were:

* Calculate daily fund returns.
* Measure short-term and long-term fund performance.
* Calculate risk-adjusted performance metrics.
* Measure systematic and downside risk.
* Compare fund performance against benchmarks.
* Analyze maximum drawdown.
* Calculate tracking error.
* Create a consolidated fund scorecard.

---

## Technologies Used

* **Python**
* **Pandas**
* **NumPy**
* **Matplotlib**
* **SciPy**
* **SQLite**
* **Jupyter Notebook**

---

## Data Used

The performance analysis was primarily performed using:

* Historical NAV data
* Fund master data
* Benchmark index data

The analysis covered **40 mutual fund schemes** over the available historical period.

---

## Performance Metrics

### 1. Daily Returns

Daily returns were calculated from consecutive NAV values to measure the daily percentage change in each mutual fund scheme.

This helped identify:

* Daily performance fluctuations
* Positive and negative return periods
* Volatility patterns
* Short-term performance behavior

The calculated daily returns were then used for further risk and performance calculations.

---

### 2. CAGR

Compound Annual Growth Rate was calculated to evaluate the annualized growth of funds over different investment periods.

The analysis considered:

* **1-Year CAGR**
* **3-Year CAGR**
* **5-Year CAGR**

CAGR helps compare fund growth over different time periods using a common annualized measure.

---

### 3. Sharpe Ratio

The Sharpe Ratio was calculated to evaluate the return generated by a fund relative to the amount of risk taken.

A higher Sharpe Ratio indicates higher excess return per unit of volatility within the analyzed period.

The analysis used a risk-free rate of **6.5%** for the calculations.

---

### 4. Sortino Ratio

The Sortino Ratio was used to evaluate risk-adjusted performance while focusing specifically on downside volatility.

Unlike the Sharpe Ratio, which considers overall volatility, the Sortino Ratio focuses on negative or harmful fluctuations.

This provides an additional perspective on downside risk.

---

### 5. Alpha and Beta

Alpha and Beta were calculated to measure the relationship between fund performance and its benchmark.

**Alpha** measures the fund's excess performance relative to the benchmark after accounting for the model assumptions.

**Beta** measures the sensitivity of the fund's returns to movements in the benchmark.

These metrics were stored in:

`alpha_beta.csv`

---

### 6. Maximum Drawdown

Maximum Drawdown was calculated to measure the largest decline in a fund's value from a previous peak to a subsequent low.

This metric helps understand the historical downside experienced by investors during major market declines.

Drawdown analysis was performed for the mutual fund schemes and used to compare historical downside risk.

---

## Fund Scorecard

A consolidated **fund scorecard** was created to bring together important performance and risk metrics for each mutual fund.

The scorecard included metrics such as:

* CAGR
* Sharpe Ratio
* Sortino Ratio
* Maximum Drawdown
* Alpha
* Beta
* Tracking Error

The final scorecard was exported as:

`fund_scorecard.csv`

This provides a structured view of the performance characteristics of the analyzed funds.

---

## Benchmark Comparison

Mutual fund performance was compared against relevant benchmark indices.

The comparison helped analyze:

* Fund returns relative to benchmarks
* Outperformance and underperformance periods
* Relationship between fund and benchmark returns

The benchmark comparison visualization was exported as:

`benchmark_comparison.png`

---

## Tracking Error

Tracking Error was calculated to measure how closely a fund's returns followed its benchmark.

A lower tracking error generally indicates that the fund's return pattern stayed closer to the benchmark during the analyzed period.

The calculated tracking-error results were exported as:

`tracking_error.csv`

---

## Key Performance Results

The analysis generated the following important results:

* **40 mutual fund schemes** were analyzed.
* Daily return observations were calculated from the historical NAV dataset.
* Average daily return across the analyzed observations was approximately **0.0631%**.
* The standard deviation of daily returns was approximately **1.029%**.
* The highest observed daily return was approximately **6.47%**.
* The lowest observed daily return was approximately **−5.81%**.
* A **6.5% annual risk-free rate** was used for risk-adjusted calculations.

### Top CAGR Observations

Some of the highest calculated CAGR values included:

| Fund / AMFI Code          |   CAGR |
| ------------------------- | -----: |
| ICICI Pru Midcap — 120505 | 32.83% |
| SBI Small Cap — 119598    | 32.42% |
| DSP Small Cap — 149324    | 32.29% |

These figures represent historical calculations from the project's dataset and should not be interpreted as future-return predictions.

---

## Deliverables

The following outputs were generated:

* `Performance_Analytics.ipynb`
* `fund_scorecard.csv`
* `alpha_beta.csv`
* `benchmark_comparison.png`
* `tracking_error.csv`
* Drawdown analysis outputs
* Performance visualization outputs

---

## Analysis Workflow

The overall Day 3 workflow was:

**Historical NAV Data → Daily Returns → Performance Metrics → Risk Analysis → Benchmark Comparison → Fund Scorecard**

---

## Day 3 Outcome

By the end of Day 3:

* Historical NAV data for 40 funds was analyzed.
* Daily returns were calculated.
* 1Y, 3Y, and 5Y CAGR metrics were calculated.
* Sharpe and Sortino ratios were calculated.
* Alpha and Beta were calculated.
* Maximum drawdown was analyzed.
* Benchmark comparison was performed.
* Tracking error was calculated.
* A consolidated fund performance scorecard was generated.
* Analysis outputs were exported for further use.

---

## Status

**Day 3 — Fund Performance Analytics: Completed ✅**

The fund performance and risk analysis was completed successfully, providing a structured view of historical returns, risk, benchmark relationships, and downside performance across the analyzed mutual fund schemes.


# DAY 4 — Exploratory Data Analysis (EDA)

## Overview

Day 4 focused on performing **Exploratory Data Analysis (EDA)** on mutual fund market and investor datasets.

The objective was to identify important **trends, patterns, relationships, distributions, and portfolio characteristics** through statistical analysis and data visualizations.

Multiple datasets covering NAV, AUM, SIP inflows, investor demographics, folio counts, portfolio holdings, and fund categories were analyzed.

---

## Objectives

The major objectives of Day 4 were:

* Analyze historical NAV trends.
* Identify major market movements.
* Study AUM growth across fund houses.
* Analyze monthly SIP inflows.
* Compare category-wise mutual fund inflows.
* Understand investor demographics.
* Analyze geographical investment distribution.
* Study mutual fund folio growth.
* Examine correlations between selected funds.
* Analyze aggregate sector allocation across equity funds.
* Generate meaningful visualizations and insights.

---

## Technologies Used

* **Python**
* **Pandas**
* **NumPy**
* **Matplotlib**
* **Seaborn**
* **Plotly**
* **SQLite**
* **Jupyter Notebook**

---

## Datasets Used

The EDA was performed using multiple datasets from the project, including:

* NAV History
* AUM by Fund House
* Monthly SIP Inflows
* Category-wise Inflows
* Industry Folio Count
* Investor Transactions
* Portfolio Holdings
* Fund Master
* Scheme Performance
* Benchmark Indices

---

## EDA Analysis Performed

### 1. NAV Trend Analysis

Daily NAV trends for **40 mutual fund schemes** were analyzed over the 2022–2026 period.

The analysis was used to:

* Observe long-term NAV movements.
* Compare trends across different schemes.
* Identify periods of strong market movement.
* Highlight the **2023 bull-run period**.
* Highlight the **2024 market-correction period**.

The NAV trend visualizations were created using Plotly.

---

### 2. AUM Growth Analysis

Assets Under Management (AUM) were analyzed across different fund houses from **2022–2025**.

The analysis helped identify:

* Fund houses with higher AUM.
* Changes in AUM over time.
* Relative growth across fund houses.
* Major fund-house-level differences.

The analysis also highlighted SBI's AUM, which reached approximately **₹12.5 lakh crore in 2025** in the project dataset.

---

### 3. Monthly SIP Inflow Analysis

Monthly SIP inflows were analyzed from **January 2022 to December 2025**.

The analysis helped identify:

* Overall SIP inflow trends.
* Monthly fluctuations.
* Growth in investor participation through SIPs.
* High and low inflow periods.

The highest highlighted observation was **December 2025**, with approximately **₹31,002 crore** in SIP inflows.

---

### 4. Category-wise Inflow Analysis

Monthly mutual fund inflows were analyzed across different fund categories.

A heatmap was created to visualize:

* Monthly inflow patterns.
* Category-level differences.
* Periods of higher and lower inflows.
* Changes in category participation over time.

The heatmap was created using Seaborn.

---

### 5. Investor Demographic Analysis

Investor transaction data was analyzed to understand demographic patterns.

The analysis included:

* Investor age distribution.
* Gender distribution.
* SIP amount distribution across age groups.

The visualizations included:

* Investor age distribution pie chart.
* SIP amount by age-group boxplot.
* Gender distribution chart.

---

### 6. Geographical Distribution Analysis

Investor SIP activity was analyzed geographically using state-level and city-tier information.

The analysis included:

* SIP amount by state.
* Top investor cities.
* T30 vs B30 city distribution.

A horizontal bar chart was used for state-level SIP distribution, while a pie chart was used to visualize the T30/B30 distribution.

---

### 7. Folio Count Growth Analysis

The growth of mutual fund folios was analyzed over the available period.

The total folio count increased from approximately:

**13.26 crore in January 2022 → 26.12 crore in December 2025**

This visualization helped demonstrate the growth in the number of mutual fund folios during the analyzed period.

---

### 8. NAV Return Correlation Analysis

The return correlation between **10 selected mutual fund schemes** was analyzed.

A correlation matrix was created to understand:

* Similar return movements.
* Relationships between selected funds.
* Diversification characteristics.
* Funds showing stronger or weaker return relationships.

The correlation matrix was visualized using a heatmap.

---

### 9. Sector Allocation Analysis

Portfolio holdings were analyzed to understand the aggregate sector allocation across equity funds.

The analysis identified the contribution of sectors such as:

* Banking
* IT
* Pharma
* Automobile
* FMCG
* Utilities
* Infrastructure
* Telecom
* Energy
* Consumer Goods
* Cement
* NBFC
* Paints
* Diversified

A donut chart was created to visualize the aggregate sector allocation.

---

## Key EDA Findings

Based on the analyzed project datasets:

1. NAV trends showed significant movement across mutual fund schemes during the 2022–2026 period.

2. Several schemes showed strong market movement during the 2023 period.

3. Market corrections were visible during the 2024 period.

4. SBI showed a significant AUM position among the analyzed fund houses, reaching approximately **₹12.5 lakh crore in 2025** in the dataset.

5. Monthly SIP inflows showed an overall upward movement across the analyzed period.

6. **December 2025 recorded approximately ₹31,002 crore** in SIP inflows.

7. Total mutual fund folios increased from approximately **13.26 crore in January 2022** to **26.12 crore in December 2025**.

8. Investor participation differed across age groups and genders.

9. SIP investment amounts varied across different states and T30/B30 city categories.

10. The aggregate equity portfolio showed meaningful exposure across sectors including **Banking, IT, Pharma, Automobile, FMCG, and Utilities**.

---

## EDA Visualizations

The EDA phase generated multiple visualizations covering market trends, investor behavior, and portfolio characteristics.

The generated charts include:

* NAV trends for 40 funds
* Highlighted NAV trends
* AUM growth by fund house
* AUM trends
* SBI AUM dominance
* Monthly SIP inflows
* Highlighted SIP inflow trend
* Category inflow heatmap
* Investor age distribution
* SIP amount by age group
* Gender distribution
* SIP distribution by state
* Top investor cities
* T30/B30 city distribution
* Folio count growth
* NAV return correlation matrix
* Sector allocation donut chart

All generated EDA outputs are stored in:

`outputs/eda/`

---

## EDA Deliverables

### Notebook

`notebooks/EDA_Analysis.ipynb`

### Output Directory

`outputs/eda/`

### Major Output Files

* `nav_trends_40_funds.png`
* `nav_trends_highlighted.png`
* `aum_growth_by_fund_house.png`
* `aum_trends_fund_houses.png`
* `sbi_aum_dominance.png`
* `monthly_sip_inflows.png`
* `sip_inflow_trend_highlighted.png`
* `category_inflow_heatmap.png`
* `investor_age_distribution.png`
* `sip_amount_by_age.png`
* `gender_distribution.png`
* `investor_distribution_by_state.png`
* `top_10_investor_cities.png`
* `investor_city_tier_distribution.png`
* `folio_count_growth.png`
* `nav_return_correlation.png`
* `sector_allocation_donut.png`

---

## Analysis Workflow

The overall Day 4 workflow was:

**Raw & Processed Data → Data Exploration → Statistical Analysis → Visualization → Pattern Identification → EDA Findings**

---

## Day 4 Outcome

By the end of Day 4:

* Historical NAV trends were analyzed for 40 schemes.
* AUM trends across fund houses were analyzed.
* Monthly SIP inflows were studied.
* Category-wise inflows were visualized.
* Investor demographics were analyzed.
* Geographic investment patterns were examined.
* Folio growth was analyzed.
* Fund return correlations were calculated.
* Aggregate equity-sector allocation was analyzed.
* Multiple EDA visualizations were generated and exported as PNG files.
* Key findings were documented.

---

## Status

**Day 4 — Exploratory Data Analysis: Completed ✅**

The EDA phase was completed successfully, providing insights into **mutual fund market trends, investor behavior, fund-house AUM, SIP activity, folio growth, return relationships, and sector allocation**.
