-- Data Vault 2.0 Schema
-- Enhanced with Business Vault and Point-in-Time tables

-- Raw Vault (same as DV 1.0 but with some enhancements)
CREATE TABLE IF NOT EXISTS data_vault_2.hub_customer (
    customer_hk String,
    customer_id String,
    load_date DateTime,
    record_source String,
    applied_date DateTime,       -- DV 2.0 addition
    last_seen_date DateTime      -- DV 2.0 addition
) ENGINE = MergeTree()
ORDER BY customer_hk;

CREATE TABLE IF NOT EXISTS data_vault_2.hub_product (
    product_hk String,
    product_id String,
    load_date DateTime,
    record_source String,
    applied_date DateTime,
    last_seen_date DateTime
) ENGINE = MergeTree()
ORDER BY product_hk;

CREATE TABLE IF NOT EXISTS data_vault_2.hub_order (
    order_hk String,
    order_id String,
    load_date DateTime,
    record_source String,
    applied_date DateTime,
    last_seen_date DateTime
) ENGINE = MergeTree()
ORDER BY order_hk;

-- Multi-Active Satellite (DV 2.0 feature for arrays/multiple values)
CREATE TABLE IF NOT EXISTS data_vault_2.sat_customer_preferences (
    customer_hk String,
    load_date DateTime,
    load_end_date Nullable(DateTime),
    record_source String,
    hash_diff String,
    preference_type String,      -- Part of the grain
    preference_value String,     -- The actual preference
    preference_order Int32       -- For ordering preferences
) ENGINE = MergeTree()
ORDER BY (customer_hk, preference_type, load_date);

-- Point-in-Time Table (DV 2.0 Business Vault)
CREATE TABLE IF NOT EXISTS data_vault_2.pit_customer (
    customer_hk String,
    snapshot_date Date,
    sat_customer_load_date DateTime,
    sat_customer_preferences_load_date DateTime
) ENGINE = MergeTree()
ORDER BY (customer_hk, snapshot_date);

-- Bridge Table (DV 2.0 Business Vault)
CREATE TABLE IF NOT EXISTS data_vault_2.bridge_customer_order (
    customer_hk String,
    snapshot_date Date,
    order_hk Array(String),      -- Array of related orders
    link_hk Array(String)        -- Array of related links
) ENGINE = MergeTree()
ORDER BY (customer_hk, snapshot_date);

-- Business Vault - Reference Tables
CREATE TABLE IF NOT EXISTS data_vault_2.ref_product_category (
    category_code String,
    category_name String,
    category_description String,
    parent_category String,
    is_active Bool,
    load_date DateTime,
    record_source String
) ENGINE = MergeTree()
ORDER BY category_code;

-- Business Vault - Calculated Satellites
CREATE TABLE IF NOT EXISTS data_vault_2.sat_customer_metrics (
    customer_hk String,
    load_date DateTime,
    load_end_date Nullable(DateTime),
    record_source String,
    hash_diff String,
    total_orders Int32,
    total_spent Decimal(12,2),
    avg_order_value Decimal(10,2),
    last_order_date DateTime,
    customer_lifetime_value Decimal(12,2),
    customer_segment String
) ENGINE = MergeTree()
ORDER BY (customer_hk, load_date);

-- Business Vault - Hierarchical Link
CREATE TABLE IF NOT EXISTS data_vault_2.hier_link_product_category (
    hier_link_hk String,
    product_hk String,
    category_level_1 String,
    category_level_2 String,
    category_level_3 String,
    load_date DateTime,
    record_source String
) ENGINE = MergeTree()
ORDER BY hier_link_hk;

-- Same table structure (DV 2.0 just adds business vault layer)
CREATE TABLE IF NOT EXISTS data_vault_2.sat_customer (
    customer_hk String,
    load_date DateTime,
    load_end_date Nullable(DateTime),
    record_source String,
    hash_diff String,
    first_name String,
    last_name String,
    email String,
    phone String,
    address String,
    city String,
    state String,
    zip_code String,
    country String
) ENGINE = MergeTree()
ORDER BY (customer_hk, load_date);

CREATE TABLE IF NOT EXISTS data_vault_2.link_order_customer (
    link_hk String,
    order_hk String,
    customer_hk String,
    load_date DateTime,
    record_source String,
    applied_date DateTime,       -- DV 2.0 enhancement
    last_seen_date DateTime      -- DV 2.0 enhancement
) ENGINE = MergeTree()
ORDER BY link_hk;
