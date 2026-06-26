
--  BASIC LEVEL


-- 1. Retrieve all distinct country names from the dataset.
SELECT DISTINCT Country_Name 
FROM Countries
WHERE Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
ORDER BY Country_Name;

-- 2. Count the total number of countries available.
SELECT COUNT(DISTINCT Country_Code) AS Total_Countries
FROM Countries
WHERE Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification');

-- 3. Find the total number of indicators present.
SELECT COUNT(DISTINCT Series_Code) AS Total_Indicators
FROM Indicators;

-- 4. Display the first 10 records of the dataset.
SELECT * FROM Debt_Data 
LIMIT 10;

-- 5. Calculate the total global debt.
SELECT SUM(d.Debt_Value) AS Global_Total_Debt
FROM Debt_Data d
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification');

-- 6. List all unique indicator names.
SELECT DISTINCT Series_Name 
FROM Indicators
ORDER BY Series_Name;

-- 7. Find the number of records for each country.
SELECT c.Country_Name, COUNT(d.Debt_Value) AS Number_Of_Records
FROM Debt_Data d
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
GROUP BY c.Country_Name
ORDER BY Number_Of_Records DESC;

-- 8. Display all records where debt is greater than 1 billion USD.
SELECT * FROM Debt_Data 
WHERE Debt_Value > 1000000000
LIMIT 100; -- Limit added for safety on large datasets

-- 9. Find the minimum, maximum, and average debt values.
SELECT 
    MIN(d.Debt_Value) AS Min_Debt, 
    MAX(d.Debt_Value) AS Max_Debt, 
    AVG(d.Debt_Value) AS Avg_Debt
FROM Debt_Data d
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification');

-- 10. Count total number of records in the dataset.
SELECT COUNT(*) AS Total_Records 
FROM Debt_Data;



--  INTERMEDIATE LEVEL



-- 1. Find the total debt for each country.
SELECT c.Country_Name, SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
GROUP BY c.Country_Name
ORDER BY Total_Debt DESC;

-- 2. Display the top 10 countries with the highest total debt.
SELECT c.Country_Name, SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
GROUP BY c.Country_Name
ORDER BY Total_Debt DESC
LIMIT 10;

-- 3. Find the average debt per country.
WITH CountryTotals AS (
    SELECT c.Country_Name, SUM(d.Debt_Value) AS Total_Debt
    FROM Debt_Data d
    JOIN Countries c ON d.Country_Code = c.Country_Code
    WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
    GROUP BY c.Country_Name
)
SELECT AVG(Total_Debt) AS Global_Average_Per_Country 
FROM CountryTotals;

-- 4. Calculate total debt for each indicator.
SELECT i.Series_Name, SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Indicators i ON d.Series_Code = i.Series_Code
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
GROUP BY i.Series_Name
ORDER BY Total_Debt DESC;

-- 5. Identify the indicator contributing the highest total debt.
SELECT i.Series_Name, SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Indicators i ON d.Series_Code = i.Series_Code
GROUP BY i.Series_Name
ORDER BY Total_Debt DESC
LIMIT 1;

-- 6. Find the country with the lowest total debt (excluding 0).
SELECT c.Country_Name, SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
  AND d.Debt_Value > 0
GROUP BY c.Country_Name
ORDER BY Total_Debt ASC
LIMIT 1;

-- 7. Calculate total debt for each country and indicator combination.
SELECT c.Country_Name, i.Series_Name, SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Countries c ON d.Country_Code = c.Country_Code
JOIN Indicators i ON d.Series_Code = i.Series_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
GROUP BY c.Country_Name, i.Series_Name
ORDER BY c.Country_Name, Total_Debt DESC;

-- 8. Count how many indicators each country has.
SELECT c.Country_Name, COUNT(DISTINCT d.Series_Code) AS Distinct_Indicators
FROM Debt_Data d
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
GROUP BY c.Country_Name
ORDER BY Distinct_Indicators DESC;

-- 9. Display countries whose total debt is above the global average.
WITH GlobalAvg AS (
    SELECT SUM(d.Debt_Value) / COUNT(DISTINCT d.Country_Code) AS AvgDebt 
    FROM Debt_Data d
    JOIN Countries c ON d.Country_Code = c.Country_Code
    WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
)
SELECT c.Country_Name, SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
GROUP BY c.Country_Name
HAVING Total_Debt > (SELECT AvgDebt FROM GlobalAvg)
ORDER BY Total_Debt DESC;

-- 10. Rank countries based on total debt (highest to lowest).
SELECT 
    c.Country_Name, 
    SUM(d.Debt_Value) AS Total_Debt,
    RANK() OVER (ORDER BY SUM(d.Debt_Value) DESC) AS Debt_Rank
FROM Debt_Data d
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
GROUP BY c.Country_Name;



--  ADVANCED LEVEL



-- 1. Find the top 5 indicators contributing most to global debt.
SELECT i.Series_Name, SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Indicators i ON d.Series_Code = i.Series_Code
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
GROUP BY i.Series_Name
ORDER BY Total_Debt DESC
LIMIT 5;

-- 2. Calculate percentage contribution of each country to total global debt.
WITH GlobalTotal AS (
    SELECT SUM(Debt_Value) AS GTotal 
    FROM Debt_Data d
    JOIN Countries c ON d.Country_Code = c.Country_Code
    WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
)
SELECT 
    c.Country_Name, 
    SUM(d.Debt_Value) AS Total_Debt,
    ROUND((SUM(d.Debt_Value) / (SELECT GTotal FROM GlobalTotal)) * 100, 2) AS Pct_Contribution
FROM Debt_Data d
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
GROUP BY c.Country_Name
ORDER BY Pct_Contribution DESC;

-- 3. Identify the top 3 countries for each indicator based on debt.
WITH RankedData AS (
    SELECT 
        i.Series_Name, 
        c.Country_Name, 
        SUM(d.Debt_Value) AS Total_Debt,
        ROW_NUMBER() OVER(PARTITION BY i.Series_Code ORDER BY SUM(d.Debt_Value) DESC) AS RN
    FROM Debt_Data d
    JOIN Countries c ON d.Country_Code = c.Country_Code
    JOIN Indicators i ON d.Series_Code = i.Series_Code
    WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
    GROUP BY i.Series_Code, i.Series_Name, c.Country_Name
)
SELECT Series_Name, Country_Name, Total_Debt
FROM RankedData
WHERE RN <= 3;

-- 4. Find the difference between maximum and minimum debt for each country.
SELECT 
    c.Country_Name, 
    MAX(d.Debt_Value) AS Max_Debt_Record, 
    MIN(d.Debt_Value) AS Min_Debt_Record,
    (MAX(d.Debt_Value) - MIN(d.Debt_Value)) AS Debt_Spread
FROM Debt_Data d
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
GROUP BY c.Country_Name
ORDER BY Debt_Spread DESC;

-- 5. Create a view for the top 10 countries with highest debt.
CREATE OR REPLACE VIEW Top_10_Debtors AS
SELECT c.Country_Name, SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
GROUP BY c.Country_Name
ORDER BY Total_Debt DESC
LIMIT 10;

-- 6. Categorize countries into High Debt, Medium Debt, Low Debt.
-- (Thresholds: > $500 Billion = High, $100B - $500B = Medium, < $100B = Low)
SELECT 
    c.Country_Name, 
    SUM(d.Debt_Value) AS Total_Debt,
    CASE 
        WHEN SUM(d.Debt_Value) > 500000000000 THEN 'High Debt'
        WHEN SUM(d.Debt_Value) BETWEEN 100000000000 AND 500000000000 THEN 'Medium Debt'
        ELSE 'Low Debt'
    END AS Debt_Category
FROM Debt_Data d
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
GROUP BY c.Country_Name
ORDER BY Total_Debt DESC;

-- 7. Use window functions to calculate cumulative debt per country (Over the years).
SELECT 
    c.Country_Name, 
    d.Year, 
    SUM(d.Debt_Value) AS Yearly_Debt,
    SUM(SUM(d.Debt_Value)) OVER (PARTITION BY c.Country_Code ORDER BY d.Year) AS Cumulative_Debt
FROM Debt_Data d
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
GROUP BY c.Country_Code, c.Country_Name, d.Year
ORDER BY c.Country_Name, d.Year;

-- 8. Find indicators where average debt is higher than overall average debt.
WITH OverallAvg AS (
    SELECT AVG(Debt_Value) AS OAvg 
    FROM Debt_Data d
    JOIN Countries c ON d.Country_Code = c.Country_Code
    WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
)
SELECT i.Series_Name, AVG(d.Debt_Value) AS Indicator_Avg_Debt
FROM Debt_Data d
JOIN Indicators i ON d.Series_Code = i.Series_Code
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
GROUP BY i.Series_Name
HAVING AVG(d.Debt_Value) > (SELECT OAvg FROM OverallAvg)
ORDER BY Indicator_Avg_Debt DESC;

-- 9. Identify countries contributing more than 5% of global debt.
WITH GlobalTotal AS (
    SELECT SUM(Debt_Value) AS GTotal 
    FROM Debt_Data d
    JOIN Countries c ON d.Country_Code = c.Country_Code
    WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
)
SELECT 
    c.Country_Name, 
    SUM(d.Debt_Value) AS Total_Debt, 
    ROUND((SUM(d.Debt_Value) / (SELECT GTotal FROM GlobalTotal)) * 100, 2) AS Pct_Contribution
FROM Debt_Data d
JOIN Countries c ON d.Country_Code = c.Country_Code
WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
GROUP BY c.Country_Name
HAVING Pct_Contribution > 5
ORDER BY Pct_Contribution DESC;

-- 10. Find the most dominant indicator (highest contribution) for each country.
WITH RankedIndicators AS (
    SELECT 
        c.Country_Name, 
        i.Series_Name, 
        SUM(d.Debt_Value) AS Total_Debt,
        ROW_NUMBER() OVER(PARTITION BY c.Country_Code ORDER BY SUM(d.Debt_Value) DESC) AS RN
    FROM Debt_Data d
    JOIN Countries c ON d.Country_Code = c.Country_Code
    JOIN Indicators i ON d.Series_Code = i.Series_Code
    WHERE c.Country_Name NOT IN ('World', 'Low & middle income', 'Middle income', 'Upper middle income', 'Lower middle income', 'South Asia', 'East Asia & Pacific', 'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia', 'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification')
    GROUP BY c.Country_Code, c.Country_Name, i.Series_Name
)
SELECT Country_Name, Series_Name AS Dominant_Indicator, Total_Debt
FROM RankedIndicators
WHERE RN = 1;