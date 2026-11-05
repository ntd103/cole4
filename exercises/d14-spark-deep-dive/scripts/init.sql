CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    customer_segments VARCHAR(20),
    country VARCHAR(50),
    city VARCHAR(50),
    age_group VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_products (
    product_id BIGSERIAL PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    brand VARCHAR(50),
    supplier_id INTEGER,
    unit_cost DECIMAL(10,2),
    stock_quantity INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id INTEGER PRIMARY KEY,
    date DATE UNIQUE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    week INTEGER,
    day_of_week INTEGER,
    day_name VARCHAR(10),
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_regions (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR(50),
    country VARCHAR(50),
    continent VARCHAR(50),
    timezone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT REFERENCES dim_customers(customer_id),
    product_id BIGINT REFERENCES dim_products(product_id),
    date_id INTEGER REFERENCES dim_date(date_id),
    region_id INTEGER REFERENCES dim_regions(region_id),
    transaction_timestamp TIMESTAMP,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    payment_method VARCHAR(20),
    transaction_status VARCHAR(20),
    fraud_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);