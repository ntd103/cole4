-- Big Fact Table Schema
-- Denormalized approach with all data in one large table

CREATE TABLE IF NOT EXISTS big_fact.big_fact_sales (
    -- Primary identifiers
    transaction_id String,
    order_id String,
    order_line_id String,
    
    -- Time dimensions (denormalized)
    order_date Date,
    order_datetime DateTime,
    order_year Int16,
    order_quarter Int8,
    order_month Int8,
    order_day Int8,
    order_day_of_week Int8,
    order_week Int8,
    is_weekend Bool,
    is_holiday Bool,
    season String,
    
    -- Customer dimensions (denormalized)
    customer_id String,
    customer_first_name String,
    customer_last_name String,
    customer_full_name String,
    customer_email String,
    customer_phone String,
    customer_birth_date Date,
    customer_age Int8,
    customer_gender String,
    customer_address String,
    customer_city String,
    customer_state String,
    customer_zip_code String,
    customer_country String,
    customer_registration_date Date,
    customer_segment String,
    customer_loyalty_status String,
    customer_credit_rating String,
    customer_annual_income Decimal(12,2),
    
    -- Product dimensions (denormalized)
    product_id String,
    product_name String,
    product_sku String,
    product_category_l1 String,
    product_category_l2 String,
    product_category_l3 String,
    product_brand String,
    product_model String,
    product_color String,
    product_size String,
    product_weight Decimal(8,2),
    product_cost Decimal(10,2),
    product_list_price Decimal(10,2),
    product_launch_date Date,
    product_status String,
    product_rating Decimal(3,2),
    
    -- Supplier dimensions (denormalized)
    supplier_id String,
    supplier_name String,
    supplier_country String,
    supplier_region String,
    supplier_rating Decimal(3,2),
    supplier_contact_person String,
    supplier_email String,
    supplier_phone String,
    
    -- Geography dimensions (denormalized)
    shipping_address String,
    shipping_city String,
    shipping_state String,
    shipping_zip_code String,
    shipping_country String,
    shipping_region String,
    billing_address String,
    billing_city String,
    billing_state String,
    billing_zip_code String,
    billing_country String,
    
    -- Sales metrics
    quantity Int32,
    unit_price Decimal(10,2),
    list_price Decimal(10,2),
    discount_amount Decimal(10,2),
    discount_percent Decimal(5,2),
    line_total Decimal(12,2),
    cost_amount Decimal(10,2),
    profit_amount Decimal(12,2),
    profit_margin Decimal(5,2),
    
    -- Order level metrics (repeated for each line)
    order_total_amount Decimal(12,2),
    order_total_items Int32,
    order_total_weight Decimal(10,2),
    shipping_cost Decimal(8,2),
    tax_amount Decimal(10,2),
    
    -- Operational dimensions
    order_status String,
    payment_method String,
    payment_status String,
    shipping_method String,
    shipping_carrier String,
    tracking_number String,
    warehouse_id String,
    warehouse_name String,
    warehouse_region String,
    sales_rep_id String,
    sales_rep_name String,
    sales_channel String,
    promotion_code String,
    promotion_name String,
    promotion_type String,
    
    -- Flags and indicators
    is_first_purchase Bool,
    is_repeat_customer Bool,
    is_bulk_order Bool,
    is_expedited_shipping Bool,
    is_gift_order Bool,
    has_discount Bool,
    has_promotion Bool,
    is_returned Bool,
    return_date Nullable(Date),
    return_reason String,
    
    -- Timestamps
    created_timestamp DateTime,
    updated_timestamp DateTime,
    shipped_timestamp Nullable(DateTime),
    delivered_timestamp Nullable(DateTime)
    
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(order_date)
ORDER BY (order_date, customer_id, product_id)
SETTINGS index_granularity = 8192;

-- Materialized views for common aggregations
CREATE MATERIALIZED VIEW IF NOT EXISTS big_fact.mv_daily_sales_summary
ENGINE = SummingMergeTree()
ORDER BY (order_date, customer_segment, product_category_l1)
AS SELECT
    order_date,
    customer_segment,
    product_category_l1,
    count() as transaction_count,
    sum(quantity) as total_quantity,
    sum(line_total) as total_sales,
    sum(cost_amount) as total_cost,
    sum(profit_amount) as total_profit,
    uniq(customer_id) as unique_customers,
    uniq(product_id) as unique_products
FROM big_fact.big_fact_sales
GROUP BY order_date, customer_segment, product_category_l1;

CREATE MATERIALIZED VIEW IF NOT EXISTS big_fact.mv_customer_summary
ENGINE = ReplacingMergeTree()
ORDER BY customer_id
AS SELECT
    customer_id,
    customer_segment,
    customer_country,
    count() as total_orders,
    sum(line_total) as total_spent,
    avg(line_total) as avg_order_value,
    max(order_date) as last_order_date,
    min(order_date) as first_order_date
FROM big_fact.big_fact_sales
GROUP BY customer_id, customer_segment, customer_country;
