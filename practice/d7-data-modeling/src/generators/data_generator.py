"""
Data generation utilities for creating sample e-commerce data.
"""
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
from faker import Faker
import pandas as pd
from rich.console import Console
import json
import os

console = Console()
fake = Faker()

class DataGenerator:
    """Generates realistic sample data for e-commerce business."""
    
    def __init__(self):
        self.fake = Faker()
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Seed for reproducible data
        Faker.seed(42)
        random.seed(42)
        
        # Business logic constants
        self.product_categories = {
            "Electronics": ["Smartphones", "Laptops", "Tablets", "Accessories"],
            "Clothing": ["Men's Clothing", "Women's Clothing", "Kids' Clothing", "Shoes"],
            "Home & Garden": ["Furniture", "Kitchen", "Bathroom", "Garden"],
            "Sports": ["Fitness", "Outdoor", "Team Sports", "Water Sports"],
            "Books": ["Fiction", "Non-Fiction", "Educational", "Children's Books"]
        }
        
        self.brands = {
            "Electronics": ["Apple", "Samsung", "Sony", "LG", "Dell", "HP"],
            "Clothing": ["Nike", "Adidas", "H&M", "Zara", "Uniqlo", "Gap"],
            "Home & Garden": ["IKEA", "Ashley", "Wayfair", "Home Depot", "Lowes"],
            "Sports": ["Nike", "Adidas", "Under Armour", "Puma", "Reebok"],
            "Books": ["Penguin", "Random House", "Harper Collins", "Simon & Schuster"]
        }
        
        self.customer_segments = ["Premium", "Standard", "Budget", "Enterprise"]
        self.loyalty_statuses = ["Bronze", "Silver", "Gold", "Platinum"]
        self.sales_channels = ["Online", "Retail Store", "Mobile App", "Phone", "Partner"]
    
    def generate_customers(self, count: int) -> List[Dict[str, Any]]:
        """Generate customer data."""
        customers = []
        
        for i in range(count):
            customer = {
                "customer_id": f"CUST_{i+1:06d}",
                "first_name": self.fake.first_name(),
                "last_name": self.fake.last_name(),
                "email": self.fake.email(),
                "phone": self.fake.phone_number(),
                "birth_date": self.fake.date_of_birth(minimum_age=18, maximum_age=80),
                "gender": random.choice(["M", "F", "Other"]),
                "address": self.fake.street_address(),
                "city": self.fake.city(),
                "state": self.fake.state(),
                "zip_code": self.fake.zipcode(),
                "country": self.fake.country(),
                "registration_date": self.fake.date_between(start_date="-3y", end_date="today"),
                "customer_segment": random.choice(self.customer_segments),
                "loyalty_status": random.choice(self.loyalty_statuses),
                "credit_rating": random.choice(["Excellent", "Good", "Fair", "Poor"]),
                "annual_income": random.randint(25000, 200000),
                "is_active": random.choice([True, True, True, False])  # 75% active
            }
            customers.append(customer)
        
        return customers
    
    def generate_products(self, count: int) -> List[Dict[str, Any]]:
        """Generate product data."""
        products = []
        
        for i in range(count):
            category_l1 = random.choice(list(self.product_categories.keys()))
            category_l2 = random.choice(self.product_categories[category_l1])
            brand = random.choice(self.brands[category_l1])
            
            product = {
                "product_id": f"PROD_{i+1:06d}",
                "product_name": f"{brand} {self.fake.word().title()} {category_l2}",
                "sku": f"{brand[:3].upper()}{random.randint(1000, 9999)}",
                "category_l1": category_l1,
                "category_l2": category_l2,
                "category_l3": f"{category_l2} - {self.fake.word().title()}",
                "brand": brand,
                "model": f"Model {random.randint(100, 999)}",
                "color": self.fake.color_name(),
                "size": random.choice(["XS", "S", "M", "L", "XL", "XXL", "N/A"]),
                "weight": round(random.uniform(0.1, 50.0), 2),
                "cost": round(random.uniform(10, 500), 2),
                "list_price": 0,  # Will be calculated based on cost
                "launch_date": self.fake.date_between(start_date="-2y", end_date="today"),
                "status": random.choice(["Active", "Active", "Active", "Discontinued"]),  # 75% active
                "rating": round(random.uniform(1.0, 5.0), 2),
                "description": self.fake.text(max_nb_chars=200)
            }
            
            # Calculate list price with markup
            markup = random.uniform(1.5, 3.0)
            product["list_price"] = round(product["cost"] * markup, 2)
            
            products.append(product)
        
        return products
    
    def generate_suppliers(self, count: int) -> List[Dict[str, Any]]:
        """Generate supplier data."""
        suppliers = []
        
        for i in range(count):
            supplier = {
                "supplier_id": f"SUPP_{i+1:04d}",
                "supplier_name": self.fake.company(),
                "contact_person": self.fake.name(),
                "email": self.fake.company_email(),
                "phone": self.fake.phone_number(),
                "address": self.fake.street_address(),
                "city": self.fake.city(),
                "state": self.fake.state(),
                "country": self.fake.country(),
                "region": random.choice(["North America", "Europe", "Asia", "South America", "Africa"]),
                "rating": round(random.uniform(1.0, 5.0), 2),
                "contract_start_date": self.fake.date_between(start_date="-5y", end_date="-1y"),
                "contract_end_date": self.fake.date_between(start_date="today", end_date="+2y"),
                "is_active": random.choice([True, True, True, False])
            }
            suppliers.append(supplier)
        
        return suppliers
    
    def generate_orders(self, customers: List[Dict], products: List[Dict], count: int) -> List[Dict[str, Any]]:
        """Generate order data with line items."""
        orders = []
        order_lines = []
        
        for i in range(count):
            customer = random.choice(customers)
            order_date = self.fake.date_time_between(start_date="-2y", end_date="now")
            
            order = {
                "order_id": f"ORD_{i+1:08d}",
                "customer_id": customer["customer_id"],
                "order_date": order_date,
                "order_status": random.choice(["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]),
                "payment_method": random.choice(["Credit Card", "Debit Card", "PayPal", "Bank Transfer"]),
                "payment_status": random.choice(["Paid", "Pending", "Failed"]),
                "shipping_method": random.choice(["Standard", "Express", "Overnight", "Ground"]),
                "shipping_carrier": random.choice(["UPS", "FedEx", "DHL", "USPS"]),
                "shipping_address": customer["address"],
                "shipping_city": customer["city"],
                "shipping_state": customer["state"],
                "shipping_country": customer["country"],
                "billing_address": customer["address"],
                "billing_city": customer["city"],
                "billing_state": customer["state"],
                "billing_country": customer["country"],
                "sales_channel": random.choice(self.sales_channels),
                "promotion_code": random.choice([None, None, None, f"PROMO{random.randint(100, 999)}"]),
                "total_amount": 0,  # Will be calculated from line items
                "tax_amount": 0,
                "shipping_cost": round(random.uniform(0, 25), 2),
                "created_timestamp": order_date,
                "updated_timestamp": order_date
            }
            
            # Generate order line items
            num_items = random.randint(1, 5)
            order_total = 0
            
            for j in range(num_items):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                unit_price = product["list_price"]
                discount_percent = random.choice([0, 0, 0, 5, 10, 15, 20])
                discount_amount = round(unit_price * quantity * discount_percent / 100, 2)
                line_total = round(unit_price * quantity - discount_amount, 2)
                
                order_line = {
                    "order_line_id": f"{order['order_id']}_L{j+1:02d}",
                    "order_id": order["order_id"],
                    "product_id": product["product_id"],
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "list_price": product["list_price"],
                    "discount_amount": discount_amount,
                    "discount_percent": discount_percent,
                    "line_total": line_total,
                    "cost_amount": round(product["cost"] * quantity, 2),
                    "profit_amount": round(line_total - (product["cost"] * quantity), 2)
                }
                
                order_lines.append(order_line)
                order_total += line_total
            
            # Update order totals
            order["total_amount"] = round(order_total, 2)
            order["tax_amount"] = round(order_total * 0.08, 2)  # 8% tax
            
            # Add timestamps for shipped/delivered orders
            if order["order_status"] in ["Shipped", "Delivered"]:
                order["shipped_timestamp"] = order_date + timedelta(days=random.randint(1, 3))
                if order["order_status"] == "Delivered":
                    order["delivered_timestamp"] = order["shipped_timestamp"] + timedelta(days=random.randint(1, 7))
            
            orders.append(order)
        
        return orders, order_lines
    
    def generate_time_dimension(self, start_date: str = "2022-01-01", end_date: str = "2025-12-31") -> List[Dict[str, Any]]:
        """Generate time dimension data."""
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        time_data = []
        current_date = start
        
        while current_date <= end:
            time_record = {
                "time_key": int(current_date.strftime("%Y%m%d")),
                "date": current_date,
                "year": current_date.year,
                "quarter": (current_date.month - 1) // 3 + 1,
                "month": current_date.month,
                "month_name": current_date.strftime("%B"),
                "day": current_date.day,
                "day_of_week": current_date.weekday() + 1,
                "day_name": current_date.strftime("%A"),
                "week_of_year": current_date.isocalendar()[1],
                "is_weekend": current_date.weekday() >= 5,
                "is_holiday": False,  # Simplified
                "holiday_name": None,
                "season": self._get_season(current_date.month),
                "fiscal_year": current_date.year if current_date.month >= 4 else current_date.year - 1,
                "fiscal_quarter": ((current_date.month - 4) % 12) // 3 + 1,
                "fiscal_month": ((current_date.month - 4) % 12) + 1
            }
            
            time_data.append(time_record)
            current_date += timedelta(days=1)
        
        return time_data
    
    def _get_season(self, month: int) -> str:
        """Get season based on month."""
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Fall"
    
    def generate_sample_data(self, scale: int = 1000):
        """Generate complete sample dataset."""
        console.print(f"[bold blue]Generating sample data (scale: {scale})[/bold blue]")
        
        # Generate base entities
        customers = self.generate_customers(scale)
        products = self.generate_products(scale // 2)
        suppliers = self.generate_suppliers(scale // 10)
        
        # Generate transactional data
        orders, order_lines = self.generate_orders(customers, products, scale * 2)
        
        # Generate time dimension
        time_data = self.generate_time_dimension()
        
        # Save to files
        datasets = {
            "customers": customers,
            "products": products,
            "suppliers": suppliers,
            "orders": orders,
            "order_lines": order_lines,
            "time_dimension": time_data
        }
        
        for name, data in datasets.items():
            # Save as JSON
            with open(f"{self.data_dir}/{name}.json", "w") as f:
                json.dump(data, f, indent=2, default=str)
            
            # Save as CSV
            df = pd.DataFrame(data)
            df.to_csv(f"{self.data_dir}/{name}.csv", index=False)
            
            console.print(f"✓ Generated {len(data)} {name} records")
        
        console.print(f"[bold green]✓ Sample data generation completed![/bold green]")
        return datasets
