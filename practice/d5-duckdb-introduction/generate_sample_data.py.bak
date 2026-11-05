#!/usr/bin/env python3
"""
Generate large sample datasets for DuckDB demonstration
"""

import pandas as pd
import numpy as np
from faker import Faker
import os
from datetime import datetime, timedelta
import random
from tqdm import tqdm

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker()
Faker.seed(42)

def create_directory(path):
    """Create directory if it doesn't exist"""
    os.makedirs(path, exist_ok=True)

def generate_customers(num_records=1_000_000):
    """Generate customer dataset"""
    print(f"Generating {num_records:,} customer records...")
    
    customers = []
    
    for _ in tqdm(range(num_records), desc="Creating customers"):
        customer = {
            'customer_id': fake.unique.random_int(min=1, max=10_000_000),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'address': fake.street_address(),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'zip_code': fake.zipcode(),
            'country': fake.country_code(),
            'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=80),
            'registration_date': fake.date_between(start_date='-5y', end_date='today'),
            'customer_segment': random.choice(['Premium', 'Standard', 'Basic']),
            'annual_income': np.random.normal(55000, 25000),
            'credit_score': np.random.randint(300, 850)
        }
        customers.append(customer)
    
    df = pd.DataFrame(customers)
    
    # Clean and format data
    df['annual_income'] = np.clip(df['annual_income'], 20000, 200000).astype(int)
    df['phone'] = df['phone'].str.replace(r'\D', '', regex=True).str[:10]
    
    return df

def generate_transactions(num_records=10_000_000, customer_ids=None):
    """Generate transaction dataset"""
    print(f"Generating {num_records:,} transaction records...")
    
    if customer_ids is None:
        customer_ids = list(range(1, 1_000_001))
    
    transactions = []
    
    # Product categories and their price ranges
    categories = {
        'Electronics': (50, 2000),
        'Clothing': (10, 300),
        'Books': (5, 50),
        'Home & Garden': (15, 500),
        'Sports': (20, 800),
        'Food & Beverage': (5, 100),
        'Health & Beauty': (8, 150),
        'Automotive': (25, 1000)
    }
    
    for _ in tqdm(range(num_records), desc="Creating transactions"):
        category = random.choice(list(categories.keys()))
        min_price, max_price = categories[category]
        
        transaction = {
            'transaction_id': fake.unique.random_int(min=1, max=50_000_000),
            'customer_id': random.choice(customer_ids),
            'transaction_date': fake.date_time_between(start_date='-2y', end_date='now'),
            'product_category': category,
            'product_name': fake.catch_phrase(),
            'quantity': np.random.poisson(2) + 1,
            'unit_price': round(np.random.uniform(min_price, max_price), 2),
            'discount_percent': np.random.choice([0, 5, 10, 15, 20, 25], p=[0.4, 0.2, 0.2, 0.1, 0.07, 0.03]),
            'payment_method': random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash', 'Bank Transfer']),
            'store_location': fake.city(),
            'sales_rep_id': np.random.randint(1, 1000)
        }
        
        # Calculate derived fields
        subtotal = transaction['quantity'] * transaction['unit_price']
        discount_amount = subtotal * (transaction['discount_percent'] / 100)
        transaction['total_amount'] = round(subtotal - discount_amount, 2)
        transaction['profit_margin'] = round(np.random.uniform(0.1, 0.4), 3)
        
        transactions.append(transaction)
    
    return pd.DataFrame(transactions)

def generate_products(num_records=100_000):
    """Generate product catalog"""
    print(f"Generating {num_records:,} product records...")
    
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 
                  'Sports', 'Food & Beverage', 'Health & Beauty', 'Automotive']
    
    products = []
    
    for _ in tqdm(range(num_records), desc="Creating products"):
        category = random.choice(categories)
        product = {
            'product_id': fake.unique.random_int(min=1, max=1_000_000),
            'product_name': fake.catch_phrase(),
            'category': category,
            'brand': fake.company(),
            'description': fake.text(max_nb_chars=200),
            'cost_price': round(np.random.uniform(5, 500), 2),
            'selling_price': 0,  # Will be calculated
            'stock_quantity': np.random.randint(0, 1000),
            'reorder_level': np.random.randint(10, 100),
            'supplier_id': np.random.randint(1, 500),
            'weight_kg': round(np.random.uniform(0.1, 20), 2),
            'dimensions': f"{np.random.randint(5, 50)}x{np.random.randint(5, 50)}x{np.random.randint(5, 50)} cm",
            'launch_date': fake.date_between(start_date='-3y', end_date='today'),
            'rating': round(np.random.uniform(1, 5), 1),
            'review_count': np.random.randint(0, 10000)
        }
        
        # Calculate selling price with markup
        markup = np.random.uniform(1.2, 3.0)
        product['selling_price'] = round(product['cost_price'] * markup, 2)
        
        products.append(product)
    
    return pd.DataFrame(products)

def generate_time_series_data():
    """Generate time series data for analytics"""
    print("Generating time series data...")
    
    # Daily metrics for 2 years
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 1, 1)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    ts_data = []
    base_visitors = 10000
    
    for date in tqdm(date_range, desc="Creating time series"):
        # Simulate seasonal patterns
        day_of_year = date.timetuple().tm_yday
        seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * day_of_year / 365)
        
        # Weekend effect
        weekend_factor = 1.2 if date.weekday() >= 5 else 1.0
        
        # Trend
        days_since_start = (date - start_date).days
        trend_factor = 1 + (days_since_start / 365) * 0.1  # 10% yearly growth
        
        # Noise
        noise_factor = np.random.normal(1, 0.1)
        
        visitors = int(base_visitors * seasonal_factor * weekend_factor * trend_factor * noise_factor)
        
        record = {
            'date': date.date(),
            'website_visitors': visitors,
            'page_views': visitors * np.random.randint(2, 8),
            'bounce_rate': round(np.random.uniform(0.2, 0.6), 3),
            'conversion_rate': round(np.random.uniform(0.01, 0.05), 4),
            'avg_session_duration': np.random.randint(120, 600),  # seconds
            'new_signups': np.random.poisson(visitors * 0.001),
            'revenue': round(np.random.uniform(1000, 10000), 2),
            'marketing_spend': round(np.random.uniform(500, 3000), 2)
        }
        
        ts_data.append(record)
    
    return pd.DataFrame(ts_data)

def save_datasets():
    """Generate and save all datasets"""
    data_dir = "/app/data"
    create_directory(data_dir)
    
    print("=== Starting DuckDB Demo Data Generation ===")
    
    # Generate customers (1M records)
    customers_df = generate_customers(1_000_000)
    customer_ids = customers_df['customer_id'].tolist()
    
    print("Saving customers dataset...")
    customers_df.to_parquet(f"{data_dir}/customers.parquet", index=False)
    customers_df.to_csv(f"{data_dir}/customers.csv", index=False)
    print(f"Customers saved: {len(customers_df):,} records")
    
    # Generate transactions (10M records)
    transactions_df = generate_transactions(10_000_000, customer_ids[:100_000])  # Subset for joins
    
    print("Saving transactions dataset...")
    transactions_df.to_parquet(f"{data_dir}/transactions.parquet", index=False)
    print(f"Transactions saved: {len(transactions_df):,} records")
    
    # Save a smaller CSV sample for comparison
    sample_transactions = transactions_df.sample(n=100_000)
    sample_transactions.to_csv(f"{data_dir}/transactions_sample.csv", index=False)
    
    # Generate products
    products_df = generate_products(100_000)
    
    print("Saving products dataset...")
    products_df.to_parquet(f"{data_dir}/products.parquet", index=False)
    products_df.to_csv(f"{data_dir}/products.csv", index=False)
    print(f"Products saved: {len(products_df):,} records")
    
    # Generate time series data
    timeseries_df = generate_time_series_data()
    
    print("Saving time series dataset...")
    timeseries_df.to_parquet(f"{data_dir}/daily_metrics.parquet", index=False)
    timeseries_df.to_csv(f"{data_dir}/daily_metrics.csv", index=False)
    print(f"Time series saved: {len(timeseries_df):,} records")
    
    # Generate summary statistics
    summary = {
        'generation_date': datetime.now().isoformat(),
        'datasets': {
            'customers': {
                'records': len(customers_df),
                'file_size_parquet': os.path.getsize(f"{data_dir}/customers.parquet"),
                'file_size_csv': os.path.getsize(f"{data_dir}/customers.csv")
            },
            'transactions': {
                'records': len(transactions_df),
                'file_size_parquet': os.path.getsize(f"{data_dir}/transactions.parquet"),
                'date_range': [
                    transactions_df['transaction_date'].min().isoformat(),
                    transactions_df['transaction_date'].max().isoformat()
                ]
            },
            'products': {
                'records': len(products_df),
                'file_size_parquet': os.path.getsize(f"{data_dir}/products.parquet"),
                'categories': products_df['category'].unique().tolist()
            },
            'daily_metrics': {
                'records': len(timeseries_df),
                'file_size_parquet': os.path.getsize(f"{data_dir}/daily_metrics.parquet"),
                'date_range': [
                    timeseries_df['date'].min().isoformat(),
                    timeseries_df['date'].max().isoformat()
                ]
            }
        }
    }
    
    import json
    with open(f"{data_dir}/dataset_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n=== Data Generation Complete ===")
    print(f"Total customers: {len(customers_df):,}")
    print(f"Total transactions: {len(transactions_df):,}")
    print(f"Total products: {len(products_df):,}")
    print(f"Total time series records: {len(timeseries_df):,}")
    print(f"Data saved to: {data_dir}")

if __name__ == "__main__":
    save_datasets()