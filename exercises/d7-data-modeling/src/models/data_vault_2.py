"""
Data Vault 2.0 implementation - Enhanced with Business Vault layer.
"""
import hashlib
import json
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
from utils.database import ClickHouseManager
from rich.console import Console

console = Console()

class DataVault2Manager:
    """Manages Data Vault 2.0 data loading and operations."""
    
    def __init__(self, db: ClickHouseManager):
        self.db = db
        self.database = "data_vault_2"
        self.record_source = "ECOMMERCE_SYSTEM"
        
    def _generate_hash_key(self, business_key: str) -> str:
        """Generate hash key from business key."""
        return hashlib.md5(business_key.encode()).hexdigest()
    
    def _generate_hash_diff(self, attributes: Dict[str, Any]) -> str:
        """Generate hash diff for change detection."""
        sorted_attrs = {k: str(v) for k, v in sorted(attributes.items()) if v is not None}
        attr_string = json.dumps(sorted_attrs, sort_keys=True)
        return hashlib.md5(attr_string.encode()).hexdigest()
    
    def load_enhanced_customer_hub(self, customers: List[Dict[str, Any]]):
        """Load customer hub with DV 2.0 enhancements."""
        console.print("Loading enhanced customer hub...")
        
        hub_data = []
        current_time = datetime.now()
        
        for customer in customers:
            hub_record = {
                "customer_hk": self._generate_hash_key(customer["customer_id"]),
                "customer_id": customer["customer_id"],
                "load_date": current_time,
                "record_source": self.record_source,
                "applied_date": current_time,  # DV 2.0 addition
                "last_seen_date": current_time  # DV 2.0 addition
            }
            hub_data.append(hub_record)
        
        self.db.execute_insert("hub_customer", hub_data, self.database)
    
    def load_customer_satellite(self, customers: List[Dict[str, Any]]):
        """Load customer satellite data."""
        console.print("Loading customer satellite...")
        
        sat_data = []
        for customer in customers:
            sat_attributes = {
                "first_name": customer["first_name"],
                "last_name": customer["last_name"],
                "email": customer["email"],
                "phone": customer["phone"],
                "address": customer["address"],
                "city": customer["city"],
                "state": customer["state"],
                "zip_code": customer["zip_code"],
                "country": customer["country"]
            }
            
            sat_record = {
                "customer_hk": self._generate_hash_key(customer["customer_id"]),
                "load_date": datetime.now(),
                "load_end_date": None,
                "record_source": self.record_source,
                "hash_diff": self._generate_hash_diff(sat_attributes),
                **sat_attributes
            }
            sat_data.append(sat_record)
        
        self.db.execute_insert("sat_customer", sat_data, self.database)
    
    def load_multi_active_satellite(self, customers: List[Dict[str, Any]]):
        """Load multi-active satellite for customer preferences (DV 2.0 feature)."""
        console.print("Loading multi-active satellite for preferences...")
        
        sat_data = []
        preferences_list = [
            "Email Notifications", "SMS Notifications", "Product Recommendations",
            "Discount Offers", "New Product Alerts", "Newsletter"
        ]
        
        for customer in customers:
            customer_hk = self._generate_hash_key(customer["customer_id"])
            
            # Generate random preferences for each customer
            import random
            num_prefs = random.randint(2, 5)
            selected_prefs = random.sample(preferences_list, num_prefs)
            
            for i, pref in enumerate(selected_prefs):
                pref_attributes = {
                    "preference_type": pref,
                    "preference_value": random.choice(["Enabled", "Disabled"]),
                    "preference_order": i + 1
                }
                
                sat_record = {
                    "customer_hk": customer_hk,
                    "load_date": datetime.now(),
                    "load_end_date": None,
                    "record_source": self.record_source,
                    "hash_diff": self._generate_hash_diff(pref_attributes),
                    **pref_attributes
                }
                sat_data.append(sat_record)
        
        self.db.execute_insert("sat_customer_preferences", sat_data, self.database)
    
    def load_reference_tables(self):
        """Load reference tables (Business Vault)."""
        console.print("Loading reference tables...")
        
        # Product category reference
        categories = [
            {"category_code": "ELEC", "category_name": "Electronics", "category_description": "Electronic devices and accessories", "parent_category": None},
            {"category_code": "CLOTH", "category_name": "Clothing", "category_description": "Apparel and fashion items", "parent_category": None},
            {"category_code": "HOME", "category_name": "Home & Garden", "category_description": "Home improvement and garden items", "parent_category": None},
            {"category_code": "SPORT", "category_name": "Sports", "category_description": "Sports and fitness equipment", "parent_category": None},
            {"category_code": "BOOK", "category_name": "Books", "category_description": "Books and educational materials", "parent_category": None}
        ]
        
        ref_data = []
        for cat in categories:
            ref_record = {
                **cat,
                "is_active": True,
                "load_date": datetime.now(),
                "record_source": self.record_source
            }
            ref_data.append(ref_record)
        
        self.db.execute_insert("ref_product_category", ref_data, self.database)
    
    def load_calculated_satellites(self, customers: List[Dict[str, Any]], orders: List[Dict[str, Any]]):
        """Load calculated satellite with customer metrics (Business Vault)."""
        console.print("Loading calculated satellites...")
        
        # Calculate customer metrics
        customer_metrics = {}
        for order in orders:
            customer_id = order["customer_id"]
            if customer_id not in customer_metrics:
                customer_metrics[customer_id] = {
                    "total_orders": 0,
                    "total_spent": 0.0,
                    "last_order_date": None,
                    "first_order_date": None
                }
            
            customer_metrics[customer_id]["total_orders"] += 1
            customer_metrics[customer_id]["total_spent"] += float(order["total_amount"])
            
            order_date = order["order_date"]
            if isinstance(order_date, str):
                order_date = datetime.fromisoformat(order_date.replace('Z', '+00:00'))
            
            if customer_metrics[customer_id]["last_order_date"] is None or order_date > customer_metrics[customer_id]["last_order_date"]:
                customer_metrics[customer_id]["last_order_date"] = order_date
            
            if customer_metrics[customer_id]["first_order_date"] is None or order_date < customer_metrics[customer_id]["first_order_date"]:
                customer_metrics[customer_id]["first_order_date"] = order_date
        
        sat_data = []
        for customer in customers:
            customer_id = customer["customer_id"]
            metrics = customer_metrics.get(customer_id, {
                "total_orders": 0,
                "total_spent": 0.0,
                "last_order_date": None,
                "first_order_date": None
            })
            
            avg_order_value = metrics["total_spent"] / max(metrics["total_orders"], 1)
            
            # Simple customer segmentation
            if metrics["total_spent"] >= 5000:
                segment = "Premium"
            elif metrics["total_spent"] >= 2000:
                segment = "Gold"
            elif metrics["total_spent"] >= 500:
                segment = "Silver"
            else:
                segment = "Bronze"
            
            # Calculate CLV (simplified)
            clv = metrics["total_spent"] * 2.5  # Simple multiplier
            
            sat_attributes = {
                "total_orders": metrics["total_orders"],
                "total_spent": round(metrics["total_spent"], 2),
                "avg_order_value": round(avg_order_value, 2),
                "last_order_date": metrics["last_order_date"],
                "customer_lifetime_value": round(clv, 2),
                "customer_segment": segment
            }
            
            sat_record = {
                "customer_hk": self._generate_hash_key(customer_id),
                "load_date": datetime.now(),
                "load_end_date": None,
                "record_source": "CALCULATED",
                "hash_diff": self._generate_hash_diff(sat_attributes),
                **sat_attributes
            }
            sat_data.append(sat_record)
        
        self.db.execute_insert("sat_customer_metrics", sat_data, self.database)
    
    def load_point_in_time_tables(self, snapshot_date: date = None):
        """Load Point-in-Time tables (Business Vault)."""
        console.print("Loading Point-in-Time tables...")
        
        if snapshot_date is None:
            snapshot_date = date.today()
        
        # Get all customers and their latest satellite records
        query = f"""
        SELECT DISTINCT
            h.customer_hk,
            s.load_date as sat_customer_load_date,
            sp.load_date as sat_preferences_load_date
        FROM {self.database}.hub_customer h
        LEFT JOIN (
            SELECT customer_hk, max(load_date) as load_date
            FROM {self.database}.sat_customer
            WHERE load_date <= '{snapshot_date}'
            GROUP BY customer_hk
        ) s ON h.customer_hk = s.customer_hk
        LEFT JOIN (
            SELECT customer_hk, max(load_date) as load_date
            FROM {self.database}.sat_customer_preferences
            WHERE load_date <= '{snapshot_date}'
            GROUP BY customer_hk
        ) sp ON h.customer_hk = sp.customer_hk
        """
        
        result = self.db.execute_query(query)
        
        pit_data = []
        for row in result.result_rows:
            pit_record = {
                "customer_hk": row[0],
                "snapshot_date": snapshot_date,
                "sat_customer_load_date": row[1],
                "sat_customer_preferences_load_date": row[2]
            }
            pit_data.append(pit_record)
        
        if pit_data:
            self.db.execute_insert("pit_customer", pit_data, self.database)
    
    def load_enhanced_links(self, orders: List[Dict[str, Any]]):
        """Load enhanced links with DV 2.0 features."""
        console.print("Loading enhanced order-customer links...")
        
        link_data = []
        current_time = datetime.now()
        
        for order in orders:
            customer_hk = self._generate_hash_key(order["customer_id"])
            order_hk = self._generate_hash_key(order["order_id"])
            link_hk = self._generate_hash_key(f"{order_hk}{customer_hk}")
            
            link_record = {
                "link_hk": link_hk,
                "order_hk": order_hk,
                "customer_hk": customer_hk,
                "load_date": current_time,
                "record_source": self.record_source,
                "applied_date": current_time,      # DV 2.0 enhancement
                "last_seen_date": current_time     # DV 2.0 enhancement
            }
            link_data.append(link_record)
        
        self.db.execute_insert("link_order_customer", link_data, self.database)
    
    def load_data(self):
        """Load all data into Data Vault 2.0 structure."""
        console.print("[bold blue]Loading Data Vault 2.0...[/bold blue]")
        
        # Load sample data
        import json
        
        with open("data/customers.json", "r") as f:
            customers = json.load(f)
        
        with open("data/products.json", "r") as f:
            products = json.load(f)
        
        with open("data/orders.json", "r") as f:
            orders = json.load(f)
        
        # Load Raw Vault
        self.load_enhanced_customer_hub(customers)
        self.load_customer_satellite(customers)
        self.load_multi_active_satellite(customers)
        self.load_enhanced_links(orders)
        
        # Load Business Vault
        self.load_reference_tables()
        self.load_calculated_satellites(customers, orders)
        self.load_point_in_time_tables()
        
        console.print("[bold green]✓ Data Vault 2.0 loading completed![/bold green]")
    
    def get_customer_360_with_business_vault(self, customer_id: str) -> Dict[str, Any]:
        """Get 360-degree view using Business Vault features."""
        customer_hk = self._generate_hash_key(customer_id)
        
        query = f"""
        SELECT 
            h.customer_id,
            s.first_name,
            s.last_name,
            s.email,
            sm.total_orders,
            sm.total_spent,
            sm.avg_order_value,
            sm.customer_lifetime_value,
            sm.customer_segment,
            groupArray(sp.preference_type) as preferences
        FROM {self.database}.hub_customer h
        LEFT JOIN {self.database}.sat_customer s ON h.customer_hk = s.customer_hk AND s.load_end_date IS NULL
        LEFT JOIN {self.database}.sat_customer_metrics sm ON h.customer_hk = sm.customer_hk AND sm.load_end_date IS NULL
        LEFT JOIN {self.database}.sat_customer_preferences sp ON h.customer_hk = sp.customer_hk AND sp.load_end_date IS NULL
        WHERE h.customer_hk = '{customer_hk}'
        GROUP BY h.customer_id, s.first_name, s.last_name, s.email, sm.total_orders, sm.total_spent, sm.avg_order_value, sm.customer_lifetime_value, sm.customer_segment
        """
        
        result = self.db.execute_query(query)
        return result.result_rows[0] if result.result_rows else None
