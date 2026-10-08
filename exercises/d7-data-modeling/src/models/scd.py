"""
Slowly Changing Dimensions (SCD) implementation.
Demonstrates SCD Types 1, 2, 3, 4, and 6.
"""
import json
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from utils.database import ClickHouseManager
from rich.console import Console

console = Console()

class SCDManager:
    """Manages SCD data loading and operations."""
    
    def __init__(self, db: ClickHouseManager):
        self.db = db
        self.database = "scd_demo"
        
    def load_scd_type1(self, customers: List[Dict[str, Any]]):
        """Load SCD Type 1 - Overwrite (No History)."""
        console.print("Loading SCD Type 1 customers...")
        
        customer_data = []
        for i, customer in enumerate(customers):
            customer_record = {
                "customer_key": i + 1,
                "customer_id": customer["customer_id"],
                "first_name": customer["first_name"],
                "last_name": customer["last_name"],
                "email": customer["email"],
                "phone": customer["phone"],
                "address": customer["address"],
                "city": customer["city"],
                "state": customer["state"],
                "zip_code": customer["zip_code"],
                "country": customer["country"],
                "last_updated": datetime.now()
            }
            customer_data.append(customer_record)
        
        self.db.execute_insert("dim_customer_type1", customer_data, self.database)
    
    def load_scd_type2(self, customers: List[Dict[str, Any]]):
        """Load SCD Type 2 - Add New Record (Full History)."""
        console.print("Loading SCD Type 2 customers...")
        
        customer_data = []
        for i, customer in enumerate(customers):
            customer_record = {
                "customer_key": i + 1,
                "customer_id": customer["customer_id"],
                "first_name": customer["first_name"],
                "last_name": customer["last_name"],
                "email": customer["email"],
                "phone": customer["phone"],
                "address": customer["address"],
                "city": customer["city"],
                "state": customer["state"],
                "zip_code": customer["zip_code"],
                "country": customer["country"],
                "effective_date": datetime.now(),
                "expiry_date": None,
                "is_current": True,
                "version_number": 1
            }
            customer_data.append(customer_record)
        
        self.db.execute_insert("dim_customer_type2", customer_data, self.database)
    
    def load_scd_type3(self, customers: List[Dict[str, Any]]):
        """Load SCD Type 3 - Add New Attribute (Limited History)."""
        console.print("Loading SCD Type 3 customers...")
        
        customer_data = []
        for i, customer in enumerate(customers):
            customer_record = {
                "customer_key": i + 1,
                "customer_id": customer["customer_id"],
                "first_name": customer["first_name"],
                "last_name": customer["last_name"],
                "email": customer["email"],
                "phone": customer["phone"],
                "current_address": customer["address"],
                "previous_address": None,  # No previous data initially
                "address_change_date": None,
                "current_city": customer["city"],
                "previous_city": None,
                "city_change_date": None,
                "state": customer["state"],
                "zip_code": customer["zip_code"],
                "country": customer["country"],
                "last_updated": datetime.now()
            }
            customer_data.append(customer_record)
        
        self.db.execute_insert("dim_customer_type3", customer_data, self.database)
    
    def load_scd_type6(self, customers: List[Dict[str, Any]]):
        """Load SCD Type 6 - Hybrid (combines Type 1, 2, and 3)."""
        console.print("Loading SCD Type 6 customers...")
        
        customer_data = []
        for i, customer in enumerate(customers):
            customer_record = {
                "customer_key": i + 1,
                "customer_id": customer["customer_id"],
                # Type 1 attributes (always current)
                "first_name": customer["first_name"],
                "last_name": customer["last_name"],
                "email": customer["email"],
                "phone": customer["phone"],
                # Type 2 attributes (historical)
                "historical_address": customer["address"],
                "historical_city": customer["city"],
                "historical_state": customer["state"],
                # Type 3 attributes (current + previous)
                "current_address": customer["address"],
                "previous_address": None,
                "address_change_date": None,
                # Type 2 control fields
                "effective_date": datetime.now(),
                "expiry_date": None,
                "is_current": True,
                "version_number": 1,
                # Additional fields
                "zip_code": customer["zip_code"],
                "country": customer["country"],
                "last_updated": datetime.now()
            }
            customer_data.append(customer_record)
        
        self.db.execute_insert("dim_customer_type6", customer_data, self.database)
    
    def load_products_type2(self, products: List[Dict[str, Any]]):
        """Load products using SCD Type 2."""
        console.print("Loading SCD Type 2 products...")
        
        product_data = []
        for i, product in enumerate(products):
            product_record = {
                "product_key": i + 1,
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "category": product["category_l1"],
                "brand": product["brand"],
                "price": float(product["list_price"]),
                "cost": float(product["cost"]),
                "effective_date": datetime.now(),
                "expiry_date": None,
                "is_current": True,
                "version_number": 1
            }
            product_data.append(product_record)
        
        self.db.execute_insert("dim_product_type2", product_data, self.database)
    
    def load_customer_profiles_type4(self, customers: List[Dict[str, Any]]):
        """Load SCD Type 4 - Mini-Dimension for rapidly changing attributes."""
        console.print("Loading SCD Type 4 customer profiles...")
        
        # Create unique profiles
        profiles = {}
        profile_data = []
        bridge_data = []
        
        for i, customer in enumerate(customers):
            # Create profile based on customer segment and loyalty
            segment = customer.get("customer_segment", "Standard")
            loyalty = customer.get("loyalty_status", "Bronze")
            credit = customer.get("credit_rating", "Good")
            income_range = self._get_income_range(customer.get("annual_income", 50000))
            
            profile_key = f"{segment}_{loyalty}_{credit}_{income_range}"
            
            if profile_key not in profiles:
                profile_id = len(profiles) + 1
                profiles[profile_key] = profile_id
                
                profile_record = {
                    "profile_key": profile_id,
                    "customer_segment": segment,
                    "credit_rating": credit,
                    "annual_income_range": income_range,
                    "loyalty_status": loyalty,
                    "effective_date": datetime.now(),
                    "expiry_date": None,
                    "is_current": True
                }
                profile_data.append(profile_record)
            
            # Create bridge record
            bridge_record = {
                "customer_key": i + 1,
                "profile_key": profiles[profile_key],
                "effective_date": datetime.now(),
                "expiry_date": None,
                "is_current": True
            }
            bridge_data.append(bridge_record)
        
        self.db.execute_insert("dim_customer_profile", profile_data, self.database)
        self.db.execute_insert("bridge_customer_profile", bridge_data, self.database)
    
    def _get_income_range(self, income: int) -> str:
        """Categorize income into ranges."""
        if income < 30000:
            return "Under 30K"
        elif income < 50000:
            return "30K-50K"
        elif income < 75000:
            return "50K-75K"
        elif income < 100000:
            return "75K-100K"
        else:
            return "Over 100K"
    
    def load_fact_orders(self, orders: List[Dict[str, Any]], order_lines: List[Dict[str, Any]]):
        """Load fact table with references to SCD dimensions."""
        console.print("Loading fact orders...")
        
        # Create a lookup for customer keys (simplified - assuming sequential)
        customer_lookup = {}
        customers_result = self.db.execute_query(f"SELECT customer_key, customer_id FROM {self.database}.dim_customer_type2 WHERE is_current = true")
        for row in customers_result.result_rows:
            customer_lookup[row[1]] = row[0]
        
        # Create a lookup for product keys
        product_lookup = {}
        products_result = self.db.execute_query(f"SELECT product_key, product_id FROM {self.database}.dim_product_type2 WHERE is_current = true")
        for row in products_result.result_rows:
            product_lookup[row[1]] = row[0]
        
        fact_data = []
        order_key = 1
        
        for line in order_lines:
            order_id = line["order_id"]
            
            # Find the corresponding order
            order_info = next((o for o in orders if o["order_id"] == order_id), None)
            if not order_info:
                continue
            
            customer_key = customer_lookup.get(order_info["customer_id"])
            product_key = product_lookup.get(line["product_id"])
            
            if customer_key and product_key:
                fact_record = {
                    "order_key": order_key,
                    "order_id": order_id,
                    "customer_key": customer_key,
                    "product_key": product_key,
                    "order_date": order_info["order_date"],
                    "quantity": int(line["quantity"]),
                    "unit_price": float(line["unit_price"]),
                    "total_amount": float(line["line_total"])
                }
                fact_data.append(fact_record)
                order_key += 1
        
        if fact_data:
            self.db.execute_insert("fact_orders", fact_data, self.database)
    
    def simulate_scd_changes(self):
        """Simulate SCD changes to demonstrate different types."""
        console.print("Simulating SCD changes...")
        
        # Simulate Type 1 change (address update - overwrites)
        update_query = f"""
        ALTER TABLE {self.database}.dim_customer_type1 
        UPDATE address = '123 New Street', last_updated = now()
        WHERE customer_id = 'CUST_000001'
        """
        self.db.execute_query(update_query)
        
        # Simulate Type 2 change (add new version)
        # First, expire the current record
        expire_query = f"""
        ALTER TABLE {self.database}.dim_customer_type2 
        UPDATE expiry_date = now(), is_current = false
        WHERE customer_id = 'CUST_000001' AND is_current = true
        """
        self.db.execute_query(expire_query)
        
        # Then insert new record
        new_record = [{
            "customer_key": 100001,  # New surrogate key
            "customer_id": "CUST_000001",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@email.com",
            "phone": "555-0123",
            "address": "456 Updated Avenue",  # Changed
            "city": "New City",             # Changed
            "state": "NY",
            "zip_code": "10001",
            "country": "USA",
            "effective_date": datetime.now(),
            "expiry_date": None,
            "is_current": True,
            "version_number": 2
        }]
        self.db.execute_insert("dim_customer_type2", new_record, self.database)
        
        # Simulate Type 3 change (update current and move to previous)
        type3_update = f"""
        ALTER TABLE {self.database}.dim_customer_type3 
        UPDATE 
            previous_address = current_address,
            current_address = '789 Type3 Street',
            address_change_date = now(),
            previous_city = current_city,
            current_city = 'Type3 City',
            city_change_date = now(),
            last_updated = now()
        WHERE customer_id = 'CUST_000001'
        """
        self.db.execute_query(type3_update)
    
    def load_data(self):
        """Load all SCD data."""
        console.print("[bold blue]Loading SCD Demo...[/bold blue]")
        
        # Load sample data
        import json
        
        with open("data/customers.json", "r") as f:
            customers = json.load(f)
        
        with open("data/products.json", "r") as f:
            products = json.load(f)
        
        with open("data/orders.json", "r") as f:
            orders = json.load(f)
        
        with open("data/order_lines.json", "r") as f:
            order_lines = json.load(f)
        
        # Load different SCD types
        self.load_scd_type1(customers[:1000])  # Subset for demo
        self.load_scd_type2(customers[:1000])
        self.load_scd_type3(customers[:1000])
        self.load_scd_type6(customers[:1000])
        self.load_products_type2(products[:500])
        self.load_customer_profiles_type4(customers[:1000])
        self.load_fact_orders(orders[:2000], order_lines[:5000])
        
        # Simulate some changes
        self.simulate_scd_changes()
        
        console.print("[bold green]✓ SCD Demo loading completed![/bold green]")
    
    def compare_scd_types(self, customer_id: str) -> Dict[str, Any]:
        """Compare how different SCD types handle the same customer."""
        comparison = {}
        
        # Type 1 - Current state only
        type1_query = f"SELECT * FROM {self.database}.dim_customer_type1 WHERE customer_id = '{customer_id}'"
        type1_result = self.db.execute_query(type1_query)
        comparison["type1"] = type1_result.result_rows[0] if type1_result.result_rows else None
        
        # Type 2 - All versions
        type2_query = f"SELECT * FROM {self.database}.dim_customer_type2 WHERE customer_id = '{customer_id}' ORDER BY version_number"
        type2_result = self.db.execute_query(type2_query)
        comparison["type2"] = type2_result.result_rows
        
        # Type 3 - Current and previous
        type3_query = f"SELECT * FROM {self.database}.dim_customer_type3 WHERE customer_id = '{customer_id}'"
        type3_result = self.db.execute_query(type3_query)
        comparison["type3"] = type3_result.result_rows[0] if type3_result.result_rows else None
        
        return comparison
