import numpy as np
import pandas as pd
import os
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)


# 1.Generate Date Dimension
print("Generate Date Dimension")
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
dates = pd.date_range(start_date, end_date)

dim_date = pd.DataFrame({
    'date_id': [(d.year*10000 + d.month*100 + d.day) for d in dates],
    'date': dates,
    'year': dates.year,
    'quarter': dates.quarter,
    'month': dates.month,
    'week': dates.isocalendar().week,
    'day_of_week': dates.dayofweek,
    'day': dates.day,
    'is_weekend': dates.dayofweek >= 5,
    'is_holiday': [random.random() < 0.05 for _ in dates]  # Randomly assign some holidays
})
dim_date.to_csv('data/raw/dim_date.csv', index=False)


# 2. Generate Customer Dimension
print("Generating customer dimension...")
n_customers = 50000

first_names = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'James', 'Emma', 
               'Robert', 'Olivia', 'William', 'Sophia', 'Richard', 'Isabella', 'Thomas']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 
              'Davis', 'Rodriguez', 'Martinez', 'Wilson', 'Anderson', 'Taylor', 'Thomas']
countries = ['USA', 'UK', 'Germany', 'France', 'Canada', 'Australia', 'Japan', 'Singapore']
cities = ['New York', 'London', 'Berlin', 'Paris', 'Toronto', 'Sydney', 'Tokyo', 'Singapore']
segments = ['premium', 'regular', 'new']
age_groups = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']

dim_customers = pd.DataFrame({
    'customer_id': range(1, n_customers + 1),
    'first_name': [random.choice(first_names) for _ in range(n_customers)],
    'last_name': [random.choice(last_names) for _ in range(n_customers)],
    'email': [f"user{i}@example.com" for i in range(1, n_customers + 1)],
    'registration_date': [start_date + timedelta(days=random.randint(0, 365)) 
                          for _ in range(n_customers)],
    'customer_segment': np.random.choice(segments, n_customers, p=[0.15, 0.65, 0.20]),
    'country': [random.choice(countries) for _ in range(n_customers)],
    'city': [random.choice(cities) for _ in range(n_customers)],
    'age_group': [random.choice(age_groups) for _ in range(n_customers)]
})

dim_customers.to_csv('data/raw/dim_customers.csv', index=False)
print(f"Generated {len(dim_customers)} customer records")

# 3. Generate Product Dimension
print("Generating product dimension...")
n_products = 5000

categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Toys']
sub_categories = {
    'Electronics': ['Phones', 'Laptops', 'Tablets', 'Accessories'],
    'Clothing': ['Men', 'Women', 'Kids', 'Accessories'],
    'Home & Garden': ['Furniture', 'Kitchen', 'Decor', 'Tools'],
    'Sports': ['Fitness', 'Outdoor', 'Team Sports', 'Equipment'],
    'Books': ['Fiction', 'Non-Fiction', 'Educational', 'Comics'],
    'Toys': ['Action Figures', 'Board Games', 'Educational', 'Outdoor']
}
brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE', 'BrandF', 'Generic']

products_list = []
for i in range(1, n_products + 1):
    category = random.choice(categories)
    sub_category = random.choice(sub_categories[category])
    products_list.append({
        'product_id': i,
        'product_name': f"{category} {sub_category} Product {i}",
        'category': category,
        'sub_category': sub_category,
        'brand': random.choice(brands),
        'supplier_id': random.randint(1, 100),
        'unit_cost': round(random.uniform(5, 500), 2),
        'stock_quantity': random.randint(0, 1000)
    })

dim_products = pd.DataFrame(products_list)
dim_products.to_csv('data/raw/dim_products.csv', index=False)
print(f"Generated {len(dim_products)} product records")

# 4. Generate Transaction Fact Table
print("Generating transaction fact table...")
n_transactions = 1000000

# Region IDs (matching PostgreSQL inserts)
region_ids = [1, 2, 3, 4, 5, 6]
payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash']
statuses = ['completed', 'refunded', 'failed']

transactions_list = []

for i in range(1, n_transactions + 1):
    if i % 100000 == 0:
        print(f"  Generated {i} transactions...")
    
    transaction_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    date_id = transaction_date.year * 10000 + transaction_date.month * 100 + transaction_date.day
    
    customer_id = random.randint(1, n_customers)
    product_id = random.randint(1, n_products)
    product = dim_products[dim_products['product_id'] == product_id].iloc[0]
    
    quantity = random.randint(1, 5)
    unit_price = round(product['unit_cost'] * random.uniform(1.5, 3.0), 2)
    total_amount = round(quantity * unit_price, 2)
    discount_amount = round(total_amount * random.uniform(0, 0.3), 2) if random.random() < 0.3 else 0
    tax_amount = round((total_amount - discount_amount) * 0.1, 2)
    
    status = np.random.choice(statuses, p=[0.92, 0.05, 0.03])
    fraud_score = random.uniform(0, 1) if status == 'failed' else random.uniform(0, 0.3)
    
    transactions_list.append({
        'transaction_id': i,
        'customer_id': customer_id,
        'product_id': product_id,
        'date_id': date_id,
        'region_id': random.choice(region_ids),
        'transaction_timestamp': transaction_date + timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        ),
        'quantity': quantity,
        'unit_price': unit_price,
        'total_amount': total_amount,
        'discount_amount': discount_amount,
        'tax_amount': tax_amount,
        'payment_method': random.choice(payment_methods),
        'transaction_status': status,
        'fraud_score': round(fraud_score, 4)
    })

fact_transactions = pd.DataFrame(transactions_list)

# Save in chunks for easier processing
chunk_size = 100000
for i in range(0, len(fact_transactions), chunk_size):
    chunk = fact_transactions[i:i+chunk_size]
    chunk_num = i // chunk_size + 1
    chunk.to_csv(f'data/raw/fact_transactions_part{chunk_num}.csv', index=False)
    print(f"Saved chunk {chunk_num}")

print(f"Generated {len(fact_transactions)} transaction records")

# 5. Generate streaming data (smaller batches for real-time simulation)
print("Generating streaming data samples...")
streaming_transactions = transactions_list[-100000:]  # Last 100000 transactions
streaming_df = pd.DataFrame(streaming_transactions)
streaming_df.to_json('data/raw/streaming_transactions.json', orient='records', lines=True)
print(f"Generated {len(streaming_df)} streaming transaction records")

print("\n=== Data Generation Complete ===")
print(f"Customers: {len(dim_customers):,}")
print(f"Products: {len(dim_products):,}")
print(f"Dates: {len(dim_date):,}")
print(f"Transactions: {len(fact_transactions):,}")
print("\nFiles saved in data/raw/")
