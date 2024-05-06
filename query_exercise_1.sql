WITH SubscriptionPeriods AS (
  SELECT
    id_customer_synth,
    -- The start date of the subscription period.
    MIN(order_datetime_synth) AS start_date,
    -- The end date of the subscription period.
    MAX(order_datetime_synth) AS end_date,
    -- The number of orders during the subscription period.
    COUNT(*) AS order_count
  FROM (
    SELECT
      id_customer_synth,
      order_datetime_synth,
      -- Check if there was a change in subscription status from the previous row.
      SUM(subscription_change) OVER (PARTITION BY id_customer_synth ORDER BY order_datetime_synth) AS subscription_group
    FROM (
      SELECT
        id_customer_synth,
        order_datetime_synth,
        is_deliveroo_plus_subscriber,
        -- Check if there was a change in subscription status from the previous row.
        -- If there is a change, this field is marked as 1, otherwise 0.
        IF(LAG(is_deliveroo_plus_subscriber, 1) OVER (PARTITION BY id_customer_synth ORDER BY order_datetime_synth) IS DISTINCT FROM is_deliveroo_plus_subscriber, 1, 0) AS subscription_change
      FROM `dsba-head-of-data-101-2.assignment_data.synthetic_deliveroo_plus_dataset`
    )
    WHERE is_deliveroo_plus_subscriber = 1
  )
  GROUP BY id_customer_synth, subscription_group
  -- Only include groups with at least 3 orders to qualify as a subscription period.
  HAVING order_count >= 3
),

-- EnrichedOrders: This CTE augments the original orders dataset with subscription information.
EnrichedOrders AS (
  SELECT
    o.*,
    p.start_date AS subscription_start_date,
    p.end_date AS subscription_end_date,
    -- Check if the order was made during a subscription period.
    CASE
      WHEN o.order_datetime_synth BETWEEN p.start_date AND p.end_date THEN 1
      ELSE 0
    END AS is_order_made_during_subscription
  FROM `dsba-head-of-data-101-2.assignment_data.synthetic_deliveroo_plus_dataset` o
  -- Join with SubscriptionPeriods to add start_date and end_date to orders.
  LEFT JOIN SubscriptionPeriods p
  ON o.id_customer_synth = p.id_customer_synth
  AND o.order_datetime_synth BETWEEN p.start_date AND p.end_date
)

-- The final SELECT statement retrieves all columns from EnrichedOrders which includes original order information plus subscription period data.
SELECT * FROM EnrichedOrders;


