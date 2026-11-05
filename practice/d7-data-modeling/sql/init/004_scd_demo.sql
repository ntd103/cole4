-- Slowly Changing Dimensions (SCD) Schema

-- SCD Type 1: Overwrite (No History)
CREATE TABLE IF NOT EXISTS scd_demo.dim_customer_type1 (
    customer_key Int32,          -- Surrogate key
    customer_id String,          -- Business key
    first_name String,
    last_name String,
    email String,
    phone String,
    address String,              -- This will be updated in place
    city String,                 -- This will be updated in place
    state String,
    zip_code String,
    country String,
    last_updated DateTime
) ENGINE = MergeTree()
ORDER BY customer_key;

-- SCD Type 2: Add New Record (Full History)
CREATE TABLE IF NOT EXISTS scd_demo.dim_customer_type2 (
    customer_key Int32,          -- Surrogate key (auto-increment)
    customer_id String,          -- Business key
    first_name String,
    last_name String,
    email String,
    phone String,
    address String,
    city String,
    state String,
    zip_code String,
    country String,
    effective_date DateTime,     -- When this version became effective
    expiry_date Nullable(DateTime), -- When this version expired
    is_current Bool,             -- Flag for current record
    version_number Int32         -- Version counter
) ENGINE = MergeTree()
ORDER BY (customer_id, customer_key);

-- SCD Type 3: Add New Attribute (Limited History)
CREATE TABLE IF NOT EXISTS scd_demo.dim_customer_type3 (
    customer_key Int32,
    customer_id String,
    first_name String,
    last_name String,
    email String,
    phone String,
    current_address String,      -- Current value
    previous_address String,     -- Previous value
    address_change_date DateTime, -- When address changed
    current_city String,
    previous_city String,
    city_change_date DateTime,
    state String,
    zip_code String,
    country String,
    last_updated DateTime
) ENGINE = MergeTree()
ORDER BY customer_key;

-- Supporting fact table to demonstrate SCD usage
CREATE TABLE IF NOT EXISTS scd_demo.fact_orders (
    order_key Int32,
    order_id String,
    customer_key Int32,          -- References SCD table
    product_key Int32,
    order_date Date,
    quantity Int32,
    unit_price Decimal(10,2),
    total_amount Decimal(12,2)
) ENGINE = MergeTree()
ORDER BY (order_date, order_key);

-- Product dimension (also using SCD Type 2)
CREATE TABLE IF NOT EXISTS scd_demo.dim_product_type2 (
    product_key Int32,
    product_id String,
    product_name String,
    category String,
    brand String,
    price Decimal(10,2),
    cost Decimal(10,2),
    effective_date DateTime,
    expiry_date Nullable(DateTime),
    is_current Bool,
    version_number Int32
) ENGINE = MergeTree()
ORDER BY (product_id, product_key);

-- SCD Type 4: Mini-Dimension (for rapidly changing attributes)
CREATE TABLE IF NOT EXISTS scd_demo.dim_customer_profile (
    profile_key Int32,
    customer_segment String,
    credit_rating String,
    annual_income_range String,
    loyalty_status String,
    effective_date DateTime,
    expiry_date Nullable(DateTime),
    is_current Bool
) ENGINE = MergeTree()
ORDER BY profile_key;

-- Bridge table linking customer to profile
CREATE TABLE IF NOT EXISTS scd_demo.bridge_customer_profile (
    customer_key Int32,
    profile_key Int32,
    effective_date DateTime,
    expiry_date Nullable(DateTime),
    is_current Bool
) ENGINE = MergeTree()
ORDER BY (customer_key, effective_date);

-- SCD Type 6: Hybrid (combines Type 1, 2, and 3)
CREATE TABLE IF NOT EXISTS scd_demo.dim_customer_type6 (
    customer_key Int32,          -- Surrogate key
    customer_id String,          -- Business key (Type 2)
    first_name String,           -- Type 1 (always current)
    last_name String,            -- Type 1 (always current) 
    email String,                -- Type 1 (always current)
    phone String,                -- Type 1 (always current)
    
    -- Type 2 attributes (historical)
    historical_address String,
    historical_city String,
    historical_state String,
    
    -- Type 3 attributes (current + previous)
    current_address String,
    previous_address String,
    address_change_date DateTime,
    
    -- Type 2 control fields
    effective_date DateTime,
    expiry_date Nullable(DateTime),
    is_current Bool,
    version_number Int32,
    
    -- Additional fields
    zip_code String,
    country String,
    last_updated DateTime
) ENGINE = MergeTree()
ORDER BY (customer_id, customer_key);
