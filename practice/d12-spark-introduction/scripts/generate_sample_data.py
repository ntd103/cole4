import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import csv
import os

def create_directories():
    """Create necessary directories"""
    dirs = ['data/csv', 'data/json', 'data/parquet', 'notebooks', 'sql']
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)

def generate_sales_data(num_records=10000):
    """Generate sales transaction data"""
    np.random.seed(42)
    
    # Generate date range
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = pd.date_range(start_date, end_date, freq='D')
    
    # Product categories and names
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Toys']
    products = {
        'Electronics': ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Smart Watch'],
        'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Shoes', 'Hat'],
        'Books': ['Fiction', 'Non-Fiction', 'Textbook', 'Comic', 'Magazine'],
        'Home & Garden': ['Chair', 'Table', 'Plant', 'Lamp', 'Decoration'],
        'Sports': ['Ball', 'Equipment', 'Clothing', 'Shoes', 'Accessories'],
        'Toys': ['Action Figure', 'Board Game', 'Puzzle', 'Doll', 'Building Blocks']
    }
    
    # Generate sales data
    sales_data = []
    for _ in range(num_records):
        category = np.random.choice(categories)
        product = np.random.choice(products[category])
        
        record = {
            'transaction_id': f'TXN{_+1:06d}',
            'date': pd.Timestamp(np.random.choice(date_range)).strftime('%Y-%m-%d'),
            'category': category,
            'product_name': product,
            'quantity': np.random.randint(1, 10),
            'unit_price': round(np.random.uniform(10, 500), 2),
            'customer_id': f'CUST{np.random.randint(1, 1000):04d}',
            'sales_rep': f'REP{np.random.randint(1, 50):03d}',
            'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'])
        }
        record['total_amount'] = round(record['quantity'] * record['unit_price'], 2)
        sales_data.append(record)
    
    # Save as CSV
    df = pd.DataFrame(sales_data)
    df.to_csv('data/csv/sales_data.csv', index=False)
    print(f"Generated {num_records} sales records in data/csv/sales_data.csv")
    
    return df

def generate_customer_data(num_customers=1000):
    """Generate customer demographics data"""
    np.random.seed(42)
    
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Lisa', 'Robert', 'Jennifer', 'William', 'Patricia']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    
    customers = []
    for i in range(1, num_customers + 1):
        customer = {
            'customer_id': f'CUST{i:04d}',
            'first_name': np.random.choice(first_names),
            'last_name': np.random.choice(last_names),
            'age': np.random.randint(18, 80),
            'city': np.random.choice(cities),
            'signup_date': (datetime(2020, 1, 1) + timedelta(days=np.random.randint(0, 1460))).strftime('%Y-%m-%d'),
            'loyalty_tier': np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'], p=[0.5, 0.3, 0.15, 0.05])
        }
        customers.append(customer)
    
    df = pd.DataFrame(customers)
    df.to_csv('data/csv/customers.csv', index=False)
    print(f"Generated {num_customers} customer records in data/csv/customers.csv")
    
    return df

def generate_product_data():
    """Generate product catalog data"""
    categories = {
        'Electronics': [
            {'name': 'Laptop', 'cost': 800, 'margin': 0.25},
            {'name': 'Phone', 'cost': 400, 'margin': 0.30},
            {'name': 'Tablet', 'cost': 300, 'margin': 0.35},
            {'name': 'Headphones', 'cost': 50, 'margin': 0.40},
            {'name': 'Smart Watch', 'cost': 200, 'margin': 0.35}
        ],
        'Clothing': [
            {'name': 'T-Shirt', 'cost': 15, 'margin': 0.60},
            {'name': 'Jeans', 'cost': 30, 'margin': 0.50},
            {'name': 'Jacket', 'cost': 60, 'margin': 0.45},
            {'name': 'Shoes', 'cost': 40, 'margin': 0.55},
            {'name': 'Hat', 'cost': 10, 'margin': 0.65}
        ],
        'Books': [
            {'name': 'Fiction', 'cost': 8, 'margin': 0.40},
            {'name': 'Non-Fiction', 'cost': 12, 'margin': 0.35},
            {'name': 'Textbook', 'cost': 80, 'margin': 0.25},
            {'name': 'Comic', 'cost': 5, 'margin': 0.50},
            {'name': 'Magazine', 'cost': 3, 'margin': 0.60}
        ]
    }
    
    products = []
    product_id = 1
    for category, items in categories.items():
        for item in items:
            products.append({
                'product_id': f'PROD{product_id:04d}',
                'category': category,
                'product_name': item['name'],
                'cost_price': item['cost'],
                'profit_margin': item['margin'],
                'suggested_price': round(item['cost'] * (1 + item['margin']), 2)
            })
            product_id += 1
    
    df = pd.DataFrame(products)
    df.to_csv('data/csv/products.csv', index=False)
    print(f"Generated {len(products)} product records in data/csv/products.csv")
    
    return df

def generate_streaming_data():
    """Generate JSON data for streaming simulation"""
    np.random.seed(42)
    
    events = ['page_view', 'click', 'purchase', 'signup', 'logout']
    devices = ['desktop', 'mobile', 'tablet']
    browsers = ['chrome', 'firefox', 'safari', 'edge']
    
    streaming_data = []
    for i in range(5000):
        event = {
            'timestamp': (datetime.now() - timedelta(seconds=np.random.randint(0, 86400))).isoformat(),
            'user_id': f'USER{np.random.randint(1, 1000):04d}',
            'event_type': np.random.choice(events),
            'device': np.random.choice(devices),
            'browser': np.random.choice(browsers),
            'session_duration': np.random.randint(30, 3600),
            'page_url': f'/page_{np.random.randint(1, 100)}',
            'referrer': np.random.choice(['google', 'facebook', 'direct', 'twitter', ''])
        }
        streaming_data.append(event)
    
    with open('data/json/web_events.json', 'w') as f:
        for event in streaming_data:
            f.write(json.dumps(event) + '\n')
    
    print(f"Generated {len(streaming_data)} streaming events in data/json/web_events.json")

def create_sql_init_script():
    """Create SQL script for PostgreSQL initialization"""
    sql_script = """
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
"""
    
    with open('sql/init.sql', 'w') as f:
        f.write(sql_script)
    
    print("Created SQL initialization script in sql/init.sql")

def main():
    """Generate all sample data"""
    print("Creating directories...")
    create_directories()
    
    print("Generating sample data...")
    generate_sales_data(10000)
    generate_customer_data(1000)
    generate_product_data()
    generate_streaming_data()
    create_sql_init_script()
    
    print("\n✅ Sample data generation complete!")
    print("\nGenerated files:")
    print("- data/csv/sales_data.csv (10,000 sales transactions)")
    print("- data/csv/customers.csv (1,000 customers)")
    print("- data/csv/products.csv (product catalog)")
    print("- data/json/web_events.json (5,000 web events)")
    print("- sql/init.sql (PostgreSQL initialization)")

if __name__ == "__main__":
    main()