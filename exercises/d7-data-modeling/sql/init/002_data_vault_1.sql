-- Data Vault 1.0 Schema
-- Raw Vault Layer

-- Hubs (Business Keys)
CREATE TABLE IF NOT EXISTS data_vault_1.hub_customer (
    customer_hk String,           -- Hash key (business key hash)
    customer_id String,           -- Business key
    load_date DateTime,           -- Load timestamp
    record_source String          -- Source system
) ENGINE = MergeTree()
ORDER BY customer_hk;

CREATE TABLE IF NOT EXISTS data_vault_1.hub_product (
    product_hk String,
    product_id String,
    load_date DateTime,
    record_source String
) ENGINE = MergeTree()
ORDER BY product_hk;

CREATE TABLE IF NOT EXISTS data_vault_1.hub_order (
    order_hk String,
    order_id String,
    load_date DateTime,
    record_source String
) ENGINE = MergeTree()
ORDER BY order_hk;

CREATE TABLE IF NOT EXISTS data_vault_1.hub_supplier (
    supplier_hk String,
    supplier_id String,
    load_date DateTime,
    record_source String
) ENGINE = MergeTree()
ORDER BY supplier_hk;

-- Links (Relationships)
CREATE TABLE IF NOT EXISTS data_vault_1.link_order_customer (
    link_hk String,              -- Hash of all foreign keys
    order_hk String,
    customer_hk String,
    load_date DateTime,
    record_source String
) ENGINE = MergeTree()
ORDER BY link_hk;

CREATE TABLE IF NOT EXISTS data_vault_1.link_order_product (
    link_hk String,
    order_hk String,
    product_hk String,
    load_date DateTime,
    record_source String
) ENGINE = MergeTree()
ORDER BY link_hk;

CREATE TABLE IF NOT EXISTS data_vault_1.link_product_supplier (
    link_hk String,
    product_hk String,
    supplier_hk String,
    load_date DateTime,
    record_source String
) ENGINE = MergeTree()
ORDER BY link_hk;

-- Satellites (Descriptive Data)
CREATE TABLE IF NOT EXISTS data_vault_1.sat_customer (
    customer_hk String,
    load_date DateTime,
    load_end_date Nullable(DateTime),
    record_source String,
    hash_diff String,            -- Hash of all attributes for change detection
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

CREATE TABLE IF NOT EXISTS data_vault_1.sat_product (
    product_hk String,
    load_date DateTime,
    load_end_date Nullable(DateTime),
    record_source String,
    hash_diff String,
    product_name String,
    category String,
    brand String,
    price Decimal(10,2),
    description String
) ENGINE = MergeTree()
ORDER BY (product_hk, load_date);

CREATE TABLE IF NOT EXISTS data_vault_1.sat_order (
    order_hk String,
    load_date DateTime,
    load_end_date Nullable(DateTime),
    record_source String,
    hash_diff String,
    order_date DateTime,
    order_status String,
    total_amount Decimal(12,2),
    shipping_address String,
    payment_method String
) ENGINE = MergeTree()
ORDER BY (order_hk, load_date);

CREATE TABLE IF NOT EXISTS data_vault_1.sat_order_line (
    link_hk String,              -- References link_order_product
    load_date DateTime,
    load_end_date Nullable(DateTime),
    record_source String,
    hash_diff String,
    quantity Int32,
    unit_price Decimal(10,2),
    discount_percent Decimal(5,2),
    line_total Decimal(12,2)
) ENGINE = MergeTree()
ORDER BY (link_hk, load_date);

CREATE TABLE IF NOT EXISTS data_vault_1.sat_supplier (
    supplier_hk String,
    load_date DateTime,
    load_end_date Nullable(DateTime),
    record_source String,
    hash_diff String,
    supplier_name String,
    contact_person String,
    email String,
    phone String,
    address String,
    city String,
    country String,
    rating Decimal(3,2)
) ENGINE = MergeTree()
ORDER BY (supplier_hk, load_date);
