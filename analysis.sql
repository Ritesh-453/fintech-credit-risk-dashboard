-- 1. Default rate by credit grade
SELECT grade, 
       COUNT(*) AS total_loans,
       SUM(is_default) AS defaults,
       ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM loans 
GROUP BY grade 
ORDER BY grade;

-- 2. Default rate by DTI bucket
SELECT 
    CASE 
        WHEN dti < 10 THEN '0-10'
        WHEN dti < 20 THEN '10-20'
        WHEN dti < 30 THEN '20-30'
        ELSE '30+' 
    END AS dti_bucket,
    COUNT(*) AS total_loans,
    ROUND(AVG(is_default) * 100, 2) AS default_rate_pct
FROM loans
GROUP BY dti_bucket
ORDER BY default_rate_pct DESC;

-- 3. High-risk segment (Grade D-G + DTI > 30)
SELECT purpose, COUNT(*) AS total,
       ROUND(AVG(is_default) * 100, 2) AS default_rate_pct
FROM loans 
WHERE grade IN ('D','E','F','G') AND dti > 30
GROUP BY purpose 
ORDER BY default_rate_pct DESC;

-- 4. Default rate by income bucket
SELECT 
    CASE 
        WHEN annual_inc < 40000 THEN 'Low (<40k)'
        WHEN annual_inc < 80000 THEN 'Mid (40k-80k)'
        WHEN annual_inc < 120000 THEN 'High (80k-120k)'
        ELSE 'Very High (120k+)' 
    END AS income_bucket,
    COUNT(*) AS total_loans,
    ROUND(AVG(is_default) * 100, 2) AS default_rate_pct
FROM loans
GROUP BY income_bucket
ORDER BY default_rate_pct DESC;

-- 5. Interest rate vs default rate by grade
SELECT grade,
       ROUND(AVG(int_rate), 2) AS avg_interest_rate,
       ROUND(AVG(is_default) * 100, 2) AS default_rate_pct
FROM loans 
GROUP BY grade 
ORDER BY grade;

-- 6. Default rate by state (top 10 riskiest)
SELECT addr_state,
       COUNT(*) AS total_loans,
       ROUND(AVG(is_default) * 100, 2) AS default_rate_pct
FROM loans 
GROUP BY addr_state 
ORDER BY default_rate_pct DESC 
LIMIT 10;