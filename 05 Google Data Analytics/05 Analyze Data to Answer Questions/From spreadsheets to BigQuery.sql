-- ! Explore the data in BigQuery
-- @block
SELECT
*
FROM `my-first-project-417404.sales.sales_info`
LIMIT 50

-- * Check min max
-- @block
SELECT
MIN(Date) AS min_date
, MAX(Date) AS max_date
FROM `my-first-project-417404.sales.sales_info`

-- * Answering the query
-- @block
SELECT
  EXTRACT(YEAR FROM Date) AS YEAR --time grouping
, EXTRACT(MONTH FROM Date) AS MONTH --time grouping
, ProductId --need to know which products are sold
, StoreID --need to know which stores are selling
, SUM(quantity) AS UnitsSold --how many (impacts inventory)
, AVG(UnitPrice) AS UnitPriceProxy --can be interesting
, COUNT(DISTINCT salesID) AS NumTransactions --unique transactions can be interesting
FROM `my-first-project-417404.sales.sales_info`
GROUP BY   YEAR,   MONTH,   ProductId, StoreID
ORDER BY   YEAR,   MONTH,   ProductId, StoreID

-- * Advance Query
-- @block
with sales_history as (
  SELECT
    EXTRACT(YEAR FROM Date) AS YEAR --time grouping
  , EXTRACT(MONTH FROM Date) AS MONTH --time grouping
  , ProductId --need to know which products are sold
  , StoreID --need to know which stores are selling
  , SUM(quantity) AS UnitsSold --how many (impacts inventory)
  , AVG(UnitPrice) AS UnitPriceProxy --can be interesting
  , COUNT(DISTINCT salesID) AS NumTransactions --unique transactions can be interesting
  FROM `my-first-project-417404.sales.sales_info`
  GROUP BY   YEAR,   MONTH, ProductId, StoreID
)
SELECT
 inventory.*
 , (SELECT AVG(UnitsSold) FROM sales_history
      WHERE inventory.ProductID=sales_history.ProductID
      AND inventory.StoreID=sales_history.StoreID) AS avg_quantity_sold_in_a_month
FROM `my-first-project-417404.sales.inventory`