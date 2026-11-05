-- Initialize the Spark demo database
CREATE TABLE IF NOT EXISTS processed_sales (
    transaction_id BIGINT PRIMARY KEY,
    customer_id BIGINT,
    product_id BIGINT,
    category VARCHAR(50),
    amount DECIMAL(10,2),
    transaction_date DATE,
    region VARCHAR(20),
    customer_name VARCHAR(100),
    product_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS performance_metrics (
    metric_id SERIAL PRIMARY KEY,
    job_id VARCHAR(100),
    stage_id INTEGER,
    task_count INTEGER,
    execution_time_ms BIGINT,
    shuffle_read_bytes BIGINT,
    shuffle_write_bytes BIGINT,
    memory_used_mb BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indices for better performance
CREATE INDEX IF NOT EXISTS idx_processed_sales_customer ON processed_sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_processed_sales_category ON processed_sales(category);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_job ON performance_metrics(job_id);
