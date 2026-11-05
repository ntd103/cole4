
-- Create tables for Spark-PostgreSQL integration demo

CREATE TABLE IF NOT EXISTS sales_summary (
    region VARCHAR(50),
    category VARCHAR(50),
    total_sales DECIMAL(15,2),
    avg_order_value DECIMAL(10,2),
    transaction_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customer_segments (
    segment_name VARCHAR(50),
    min_age INTEGER,
    max_age INTEGER,
    loyalty_tier VARCHAR(20),
    avg_lifetime_value DECIMAL(10,2),
    customer_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample data
INSERT INTO sales_summary (region, category, total_sales, avg_order_value, transaction_count) VALUES
('North', 'Electronics', 150000.00, 350.00, 428),
('South', 'Clothing', 89000.00, 125.00, 712),
('East', 'Books', 45000.00, 28.50, 1578),
('West', 'Home & Garden', 67000.00, 89.00, 753),
('Central', 'Sports', 78000.00, 156.00, 500);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO spark;
