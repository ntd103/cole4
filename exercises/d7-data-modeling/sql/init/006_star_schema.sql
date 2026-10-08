-- Star Schema
-- Traditional dimensional modeling with fact and dimension tables

-- Time Dimension
CREATE TABLE IF NOT EXISTS star_schema.dim_time (
    time_key Int32,              -- YYYYMMDD format
    date Date,
    year Int16,
    quarter Int8,
    month Int8,
    month_name String,
    day Int8,
    day_of_week Int8,
    day_name String,
    week_of_year Int8,
    is_weekend Bool,
    is_holiday Bool,
    holiday_name String,
    season String,
    fiscal_year Int16,
    fiscal_quarter Int8,
    fiscal_month Int8
) ENGINE = MergeTree()
ORDER BY time_key;

-- Customer Dimension
CREATE TABLE IF NOT EXISTS star_schema.dim_customer (
    customer_key Int32,
    customer_id String,
    first_name String,
    last_name String,
    full_name String,
    email String,
    phone String,
    birth_date Date,
    gender String,
    address String,
    city String,
    state String,
    zip_code String,
    country String,
    registration_date Date,
    customer_segment String,
    loyalty_status String,
    credit_rating String,
    is_active Bool,
    effective_date DateTime,
    expiry_date Nullable(DateTime)
) ENGINE = MergeTree()
ORDER BY customer_key;

-- Product Dimension
CREATE TABLE IF NOT EXISTS star_schema.dim_product (
    product_key Int32,
    product_id String,
    product_name String,
    sku String,
    category String,
    subcategory String,
    brand String,
    model String,
    color String,
    size String,
    weight Decimal(8,2),
    cost Decimal(10,2),
    list_price Decimal(10,2),
    launch_date Date,
    status String,
    rating Decimal(3,2),
    is_active Bool,
    effective_date DateTime,
    expiry_date Nullable(DateTime)
) ENGINE = MergeTree()
ORDER BY product_key;

-- Geography Dimension
CREATE TABLE IF NOT EXISTS star_schema.dim_geography (
    geography_key Int32,
    address String,
    city String,
    state String,
    zip_code String,
    country String,
    region String,
    continent String,
    time_zone String,
    population Int32,
    area_code String
) ENGINE = MergeTree()
ORDER BY geography_key;

-- Supplier Dimension
CREATE TABLE IF NOT EXISTS star_schema.dim_supplier (
    supplier_key Int32,
    supplier_id String,
    supplier_name String,
    contact_person String,
    email String,
    phone String,
    address String,
    city String,
    country String,
    region String,
    rating Decimal(3,2),
    contract_start_date Date,
    contract_end_date Date,
    is_active Bool
) ENGINE = MergeTree()
ORDER BY supplier_key;

-- Sales Channel Dimension
CREATE TABLE IF NOT EXISTS star_schema.dim_sales_channel (
    channel_key Int32,
    channel_id String,
    channel_name String,
    channel_type String,
    channel_category String,
    manager_name String,
    commission_rate Decimal(5,2),
    is_active Bool
) ENGINE = MergeTree()
ORDER BY channel_key;

-- Promotion Dimension
CREATE TABLE IF NOT EXISTS star_schema.dim_promotion (
    promotion_key Int32,
    promotion_id String,
    promotion_name String,
    promotion_type String,
    discount_type String,
    discount_value Decimal(10,2),
    start_date Date,
    end_date Date,
    is_active Bool
) ENGINE = MergeTree()
ORDER BY promotion_key;

-- Central Fact Table
CREATE TABLE IF NOT EXISTS star_schema.fact_sales (
    sales_key Int64,             -- Surrogate key for the fact
    time_key Int32,              -- FK to dim_time
    customer_key Int32,          -- FK to dim_customer
    product_key Int32,           -- FK to dim_product
    supplier_key Int32,          -- FK to dim_supplier
    geography_key Int32,         -- FK to dim_geography (shipping)
    billing_geography_key Int32, -- FK to dim_geography (billing)
    channel_key Int32,           -- FK to dim_sales_channel
    promotion_key Int32,         -- FK to dim_promotion
    
    -- Degenerate dimensions (stored in fact table)
    order_id String,
    order_line_id String,
    invoice_number String,
    
    -- Measures (additive)
    quantity Int32,
    unit_price Decimal(10,2),
    discount_amount Decimal(10,2),
    line_total Decimal(12,2),
    cost_amount Decimal(10,2),
    profit_amount Decimal(12,2),
    tax_amount Decimal(10,2),
    shipping_cost Decimal(8,2),
    
    -- Semi-additive measures
    inventory_quantity Int32,
    unit_cost Decimal(10,2),
    
    -- Non-additive measures (stored as facts for drill-down)
    profit_margin Decimal(5,2),
    discount_percent Decimal(5,2),
    
    -- Flags
    is_returned Bool,
    is_exchange Bool,
    
    -- Timestamps
    order_timestamp DateTime,
    shipped_timestamp Nullable(DateTime),
    delivered_timestamp Nullable(DateTime)
    
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(toDate(order_timestamp))
ORDER BY (time_key, customer_key, product_key)
SETTINGS index_granularity = 8192;

-- Aggregate fact tables for performance
CREATE TABLE IF NOT EXISTS star_schema.fact_sales_monthly (
    time_key Int32,              -- Month key
    customer_key Int32,
    product_key Int32,
    channel_key Int32,
    
    -- Aggregated measures
    total_quantity Int64,
    total_sales Decimal(18,2),
    total_cost Decimal(18,2),
    total_profit Decimal(18,2),
    order_count Int32,
    unique_customers Int32,
    avg_order_value Decimal(12,2),
    
    -- Min/Max for non-additive measures
    min_profit_margin Decimal(5,2),
    max_profit_margin Decimal(5,2),
    avg_profit_margin Decimal(5,2)
    
) ENGINE = SummingMergeTree()
ORDER BY (time_key, customer_key, product_key, channel_key);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer ON star_schema.fact_sales (customer_key) TYPE minmax GRANULARITY 3;
CREATE INDEX IF NOT EXISTS idx_fact_sales_product ON star_schema.fact_sales (product_key) TYPE minmax GRANULARITY 3;
CREATE INDEX IF NOT EXISTS idx_fact_sales_time ON star_schema.fact_sales (time_key) TYPE minmax GRANULARITY 3;
