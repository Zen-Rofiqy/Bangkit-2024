-- Create dataset (database) and the table first in BigQuery
-- ! Examine the tables
-- @block
SELECT
	*
FROM
	`my-first-project-417404.warehouse_orders.warehouse`

-- ! Create a new query
-- @block
SELECT
	*
FROM
	`my-first-project-417404.warehouse_orders.orders`
LIMIT 100

-- ! Create aliases and JOIN the tables
-- @block
SELECT
     *
FROM 
     `my-first-project-417404.warehouse_orders.orders` AS orders

-- @block
SELECT
	*
FROM
	`my-first-project-417404.warehouse_orders.orders` AS orders
JOIN
    `my-first-project-417404.warehouse_orders.warehouse` warehouse ON orders.warehouse_id = warehouse.warehouse_id

-- @block
SELECT
	orders.*,
	warehouse.warehouse_alias,
	warehouse.state
FROM
	`my-first-project-417404.warehouse_orders.orders` AS orders
JOIN
    `my-first-project-417404.warehouse_orders.warehouse` warehouse ON orders.warehouse_id = warehouse.warehouse_id

-- ! Query the ordered data's number of states with COUNT
-- @block
SELECT
	COUNT(warehouse.state) as num_states
FROM
	`my-first-project-417404.warehouse_orders.orders` AS orders
JOIN
    `my-first-project-417404.warehouse_orders.warehouse` warehouse ON orders.warehouse_id = warehouse.warehouse_id

-- ! Query the ordered data's number of states with COUNT DISTINCT
-- @block
SELECT
	COUNT(DISTINCT warehouse.state) as num_states
FROM
	`my-first-project-417404.warehouse_orders.orders` AS orders
JOIN
    `my-first-project-417404.warehouse_orders.warehouse` warehouse ON orders.warehouse_id = warehouse.warehouse_id

-- ! Organize the results table with GROUP BY
-- @block
SELECT
	state,
	COUNT(DISTINCT order_id) as num_orders
FROM
	`my-first-project-417404.warehouse_orders.orders` AS orders
JOIN
    `my-first-project-417404.warehouse_orders.warehouse` warehouse ON orders.warehouse_id = warehouse.warehouse_id
GROUP BY
	warehouse.state