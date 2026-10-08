-- Snowflake Schema
-- Normalized dimensional modeling where dimensions are further normalized

-- Time hierarchy (normalized)
CREATE TABLE IF NOT EXISTS snowflake_schema.dim_year (
    year_key Int16,
    year_number Int16,
    fiscal_year Int16,
    is_leap_year Bool
) ENGINE = MergeTree()
ORDER BY year_key;

CREATE TABLE IF NOT EXISTS snowflake_schema.dim_quarter (
    quarter_key Int16,
    year_key Int16,
    quarter_number Int8,
    quarter_name String,
    fiscal_quarter Int8
) ENGINE = MergeTree()
ORDER BY quarter_key;

CREATE TABLE IF NOT EXISTS snowflake_schema.dim_month (
    month_key Int16,
    quarter_key Int16,
    month_number Int8,
    month_name String,
    month_abbr String,
    days_in_month Int8,
    fiscal_month Int8
) ENGINE = MergeTree()
ORDER BY month_key;

CREATE TABLE IF NOT EXISTS snowflake_schema.dim_date (
    date_key Int32,
    month_key Int16,
    date Date,
    day_number Int8,
    day_name String,
    day_abbr String,
    day_of_week Int8,
    day_of_year Int16,
    week_of_year Int8,
    is_weekend Bool,
    is_holiday Bool,
    holiday_name String
) ENGINE = MergeTree()
ORDER BY date_key;

-- Geography hierarchy (normalized)
CREATE TABLE IF NOT EXISTS snowflake_schema.dim_continent (
    continent_key Int8,
    continent_code String,
    continent_name String
) ENGINE = MergeTree()
ORDER BY continent_key;

CREATE TABLE IF NOT EXISTS snowflake_schema.dim_country (
    country_key Int16,
    continent_key Int8,
    country_code String,
    country_name String,
    currency_code String,
    phone_prefix String
) ENGINE = MergeTree()
ORDER BY country_key;

CREATE TABLE IF NOT EXISTS snowflake_schema.dim_state (
    state_key Int16,
    country_key Int16,
    state_code String,
    state_name String,
    capital_city String,
    population Int32
) ENGINE = MergeTree()
ORDER BY state_key;

CREATE TABLE IF NOT EXISTS snowflake_schema.dim_city (
    city_key Int32,
    state_key Int16,
    city_name String,
    zip_code String,
    population Int32,
    area_code String,
    time_zone String
) ENGINE = MergeTree()
ORDER BY city_key;

-- Product hierarchy (normalized)
CREATE TABLE IF NOT EXISTS snowflake_schema.dim_brand (
    brand_key Int16,
    brand_code String,
    brand_name String,
    brand_owner String,
    established_year Int16
) ENGINE = MergeTree()
ORDER BY brand_key;

CREATE TABLE IF NOT EXISTS snowflake_schema.dim_category_l1 (
    category_l1_key Int16,
    category_l1_code String,
    category_l1_name String,
    category_manager String
) ENGINE = MergeTree()
ORDER BY category_l1_key;

CREATE TABLE IF NOT EXISTS snowflake_schema.dim_category_l2 (
    category_l2_key Int16,
    category_l1_key Int16,
    category_l2_code String,
    category_l2_name String
) ENGINE = MergeTree()
ORDER BY category_l2_key;

CREATE TABLE IF NOT EXISTS snowflake_schema.dim_category_l3 (
    category_l3_key Int16,
    category_l2_key Int16,
    category_l3_code String,
    category_l3_name String
) ENGINE = MergeTree()
ORDER BY category_l3_key;

CREATE TABLE IF NOT EXISTS snowflake_schema.dim_product (
    product_key Int32,
    category_l3_key Int16,
    brand_key Int16,
    product_id String,
    product_name String,
    sku String,
    model String,
    color String,
    size String,
    weight Decimal(8,2),
    cost Decimal(10,2),
    list_price Decimal(10,2),
    launch_date Date,
    status String,
    rating Decimal(3,2),
    is_active Bool
) ENGINE = MergeTree()
ORDER BY product_key;

-- Customer hierarchy (normalized)
CREATE TABLE IF NOT EXISTS snowflake_schema.dim_customer_segment (
    segment_key Int8,
    segment_code String,
    segment_name String,
    segment_description String
) ENGINE = MergeTree()
ORDER BY segment_key;

CREATE TABLE IF NOT EXISTS snowflake_schema.dim_loyalty_status (
    loyalty_key Int8,
    loyalty_code String,
    loyalty_name String,
    min_points Int32,
    discount_rate Decimal(5,2)
) ENGINE = MergeTree()
ORDER BY loyalty_key;

CREATE TABLE IF NOT EXISTS snowflake_schema.dim_customer (
    customer_key Int32,
    city_key Int32,              -- FK to geography
    segment_key Int8,            -- FK to customer segment
    loyalty_key Int8,            -- FK to loyalty status
    customer_id String,
    first_name String,
    last_name String,
    full_name String,
    email String,
    phone String,
    birth_date Date,
    gender String,
    address String,
    registration_date Date,
    credit_rating String,
    is_active Bool
) ENGINE = MergeTree()
ORDER BY customer_key;

-- Supplier normalized
CREATE TABLE IF NOT EXISTS snowflake_schema.dim_supplier_rating (
    rating_key Int8,
    rating_code String,
    rating_name String,
    min_score Decimal(3,2),
    max_score Decimal(3,2)
) ENGINE = MergeTree()
ORDER BY rating_key;

CREATE TABLE IF NOT EXISTS snowflake_schema.dim_supplier (
    supplier_key Int32,
    city_key Int32,              -- FK to geography
    rating_key Int8,             -- FK to supplier rating
    supplier_id String,
    supplier_name String,
    contact_person String,
    email String,
    phone String,
    address String,
    contract_start_date Date,
    contract_end_date Date,
    is_active Bool
) ENGINE = MergeTree()
ORDER BY supplier_key;

-- Sales Channel normalized
CREATE TABLE IF NOT EXISTS snowflake_schema.dim_channel_type (
    channel_type_key Int8,
    channel_type_code String,
    channel_type_name String,
    commission_base_rate Decimal(5,2)
) ENGINE = MergeTree()
ORDER BY channel_type_key;

CREATE TABLE IF NOT EXISTS snowflake_schema.dim_sales_channel (
    channel_key Int32,
    channel_type_key Int8,       -- FK to channel type
    channel_id String,
    channel_name String,
    manager_name String,
    commission_rate Decimal(5,2),
    is_active Bool
) ENGINE = MergeTree()
ORDER BY channel_key;

-- Promotion normalized
CREATE TABLE IF NOT EXISTS snowflake_schema.dim_promotion_type (
    promotion_type_key Int8,
    promotion_type_code String,
    promotion_type_name String,
    default_discount_percent Decimal(5,2)
) ENGINE = MergeTree()
ORDER BY promotion_type_key;

CREATE TABLE IF NOT EXISTS snowflake_schema.dim_promotion (
    promotion_key Int32,
    promotion_type_key Int8,     -- FK to promotion type
    promotion_id String,
    promotion_name String,
    discount_type String,
    discount_value Decimal(10,2),
    start_date Date,
    end_date Date,
    is_active Bool
) ENGINE = MergeTree()
ORDER BY promotion_key;

-- Central Fact Table (same structure as star schema but references normalized dimensions)
CREATE TABLE IF NOT EXISTS snowflake_schema.fact_sales (
    sales_key Int64,
    date_key Int32,              -- FK to dim_date
    customer_key Int32,          -- FK to dim_customer
    product_key Int32,           -- FK to dim_product
    supplier_key Int32,          -- FK to dim_supplier
    shipping_city_key Int32,     -- FK to dim_city (shipping)
    billing_city_key Int32,      -- FK to dim_city (billing)
    channel_key Int32,           -- FK to dim_sales_channel
    promotion_key Int32,         -- FK to dim_promotion
    
    -- Degenerate dimensions
    order_id String,
    order_line_id String,
    invoice_number String,
    
    -- Measures
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
    
    -- Non-additive measures
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
ORDER BY (date_key, customer_key, product_key)
SETTINGS index_granularity = 8192;
