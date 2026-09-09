-- =========================================================
-- QUERY 1: Top 5 Funds by AUM
-- =========================================================

SELECT
    f.amfi_code,
    f.scheme_name,
    f.fund_house,
    p.aum_crore
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;

-- =========================================================
-- QUERY 2: Average NAV per Month
-- =========================================================

SELECT
    d.year,
    d.month,
    d.month_name,
    ROUND(AVG(n.nav), 4) AS average_nav
FROM fact_nav n
JOIN dim_date d
    ON n.date_id = d.date_id
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;
    -- =========================================================
-- QUERY 3: SIP Year-over-Year (YoY) Growth
-- =========================================================

SELECT
    d.year,
    ROUND(AVG(s.yoy_growth_pct), 2) AS avg_yoy_growth_pct,
    ROUND(SUM(s.sip_inflow_crore), 2) AS total_sip_inflow_crore
FROM fact_sip_inflows s
JOIN dim_date d
    ON s.date_id = d.date_id
GROUP BY d.year
ORDER BY d.year;

-- =========================================================
-- QUERY 4: Investor Transactions by State
-- =========================================================

SELECT
    state,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_inr), 2) AS total_transaction_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_transaction_amount_inr DESC;

-- =========================================================
-- QUERY 5: Funds with Expense Ratio Less Than 1%
-- =========================================================

SELECT
    amfi_code,
    scheme_name,
    fund_house,
    category,
    plan,
    expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;
-- =========================================================
-- QUERY 6: Top 5 Funds by 3-Year Return
-- =========================================================

SELECT
    f.amfi_code,
    f.scheme_name,
    f.fund_house,
    f.category,
    p.return_3yr_pct
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
ORDER BY p.return_3yr_pct DESC
LIMIT 5;
-- =========================================================
-- QUERY 7: Average Return by Fund Category
-- =========================================================

SELECT
    f.category,
    COUNT(*) AS total_funds,
    ROUND(AVG(p.return_1yr_pct), 2) AS avg_1yr_return_pct,
    ROUND(AVG(p.return_3yr_pct), 2) AS avg_3yr_return_pct,
    ROUND(AVG(p.return_5yr_pct), 2) AS avg_5yr_return_pct
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
GROUP BY f.category
ORDER BY avg_3yr_return_pct DESC;
-- =========================================================
-- QUERY 8: Highest Risk Funds
-- =========================================================

SELECT
    amfi_code,
    scheme_name,
    fund_house,
    category,
    risk_category,
    return_3yr_pct,
    std_dev_ann_pct,
    max_drawdown_pct
FROM dim_fund
JOIN fact_performance
    USING (amfi_code)
WHERE risk_category IN ('Very High', 'High')
ORDER BY
    CASE risk_category
        WHEN 'Very High' THEN 1
        WHEN 'High' THEN 2
    END,
    std_dev_ann_pct DESC;
    -- =========================================================
-- QUERY 9: Portfolio Holdings by Sector
-- =========================================================

SELECT
    sector,
    COUNT(*) AS total_holdings,
    ROUND(SUM(market_value_cr), 2) AS total_market_value_cr,
    ROUND(AVG(weight_pct), 2) AS avg_weight_pct
FROM fact_portfolio_holdings
GROUP BY sector
ORDER BY total_market_value_cr DESC;
-- =========================================================
-- QUERY 10: Benchmark Index Performance
-- =========================================================

SELECT
    b.index_name,
    MIN(d.date) AS start_date,
    MAX(d.date) AS end_date,
    ROUND(
        (MAX(b.close_value) - MIN(b.close_value))
        * 100.0 / MIN(b.close_value),
        2
    ) AS total_return_pct
FROM fact_benchmark_indices b
JOIN dim_date d
    ON b.date_id = d.date_id
GROUP BY b.index_name
ORDER BY total_return_pct DESC;