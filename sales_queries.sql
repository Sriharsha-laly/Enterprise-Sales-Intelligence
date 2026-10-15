
-- 1. Overall business performance
SELECT
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(AVG(Revenue), 2) AS Average_Revenue
FROM sales_data;


-- 2. Regional performance
SELECT
    Region,
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    COUNT(*) AS Transaction_Count
FROM sales_data
GROUP BY Region
ORDER BY Total_Revenue DESC;


-- 3. Most profitable products
SELECT
    Product,
    ROUND(SUM(Revenue), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit
FROM sales_data
GROUP BY Product
ORDER BY Profit DESC;


-- 4. Monthly sales trends
SELECT
    strftime('%Y-%m', Order_Date) AS Sales_Month,
    ROUND(SUM(Revenue), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit
FROM sales_data
GROUP BY strftime('%Y-%m', Order_Date)
ORDER BY Sales_Month;


-- 5. Customer segment analysis
SELECT
    Customer_Segment,
    COUNT(*) AS Transactions,
    ROUND(SUM(Revenue), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit
FROM sales_data
GROUP BY Customer_Segment
ORDER BY Revenue DESC;


-- 6. Sales channel comparison
SELECT
    Sales_Channel,
    COUNT(*) AS Transactions,
    ROUND(SUM(Revenue), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit
FROM sales_data
GROUP BY Sales_Channel
ORDER BY Revenue DESC;


-- 7. Discount analysis
SELECT
    CASE
        WHEN Discount = 0 THEN 'No discount'
        WHEN Discount <= 0.10 THEN 'Low discount'
        WHEN Discount <= 0.20 THEN 'Medium discount'
        ELSE 'High discount'
    END AS Discount_Band,
    COUNT(*) AS Transactions,
    ROUND(SUM(Revenue), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit
FROM sales_data
GROUP BY Discount_Band
ORDER BY Revenue DESC;


-- 8. Order status summary
SELECT
    Order_Status,
    COUNT(*) AS Transactions,
    ROUND(SUM(Revenue), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit
FROM sales_data
GROUP BY Order_Status
ORDER BY Transactions DESC;