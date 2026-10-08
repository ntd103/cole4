"""
Data Vault 1.0 implementation - Traditional Hub, Link, Satellite architecture.
"""
import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from utils.database import ClickHouseManager
from rich.console import Console

console = Console()

class DataVault1Manager:
    """Manages Data Vault 1.0 data loading and operations."""
    
    def __init__(self, db: ClickHouseManager):
        self.db = db
        self.database = "data_vault_1"
        self.record_source = "ECOMMERCE_SYSTEM"
        
    def _generate_hash_key(self, business_key: str) -> str:
        """Generate hash key from business key."""
        return hashlib.md5(business_key.encode()).hexdigest()
    
    def _generate_hash_diff(self, attributes: Dict[str, Any]) -> str:
        """Generate hash diff for change detection."""
        # Sort keys to ensure consistent hashing
        sorted_attrs = {k: str(v) for k, v in sorted(attributes.items()) if v is not None}
        attr_string = json.dumps(sorted_attrs, sort_keys=True)
        return hashlib.md5(attr_string.encode()).hexdigest()
    
    def _safe_insert(self, table_name: str, data_rows: List[tuple]):
        """Safely insert data as tuples into ClickHouse table."""
        try:
            self.db.client.insert(f"{self.database}.{table_name}", data_rows)
            console.print(f"✓ Inserted {len(data_rows)} records into {table_name}")
        except Exception as e:
            console.print(f"❌ Insert failed for {table_name}: {e}")
            raise
    
    def load_customer_hub(self, customers: List[Dict[str, Any]]):
        """Load customer hub data."""
        console.print("Loading customer hub...")
        
        hub_data = []
        for customer in customers:
            hub_record = (
                self._generate_hash_key(str(customer["customer_id"])),
                str(customer["customer_id"]),
                datetime.now(),
                self.record_source
            )
            hub_data.append(hub_record)
        
        self._safe_insert("hub_customer", hub_data)
        
    def load_customer_satellite(self, customers: List[Dict[str, Any]]):
        """Load customer satellite data."""
        console.print("Loading customer satellite...")
        
        sat_data = []
        for customer in customers:
            # Extract satellite attributes
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
            
            sat_record = (
                self._generate_hash_key(str(customer["customer_id"])),  # customer_hk
                datetime.now(),  # load_date
                None,  # load_end_date
                self.record_source,  # record_source
                self._generate_hash_diff(sat_attributes),  # hash_diff
                customer["first_name"],
                customer["last_name"],
                customer["email"],
                customer["phone"],
                customer["address"],
                customer["city"],
                customer["state"],
                customer["zip_code"],
                customer["country"]
            )
            sat_data.append(sat_record)
        
        self._safe_insert("sat_customer", sat_data)
    
    def load_customers(self, customers: List[Dict[str, Any]]):
        """Load customer data (hub + satellite)."""
        self.load_customer_hub(customers)
        self.load_customer_satellite(customers)
    
    def load_products(self, products: List[Dict[str, Any]]):
        """Load product data (hub + satellite)."""
        console.print("Loading product hub...")
        hub_data = []
        for product in products:
            hub_record = (
                self._generate_hash_key(str(product["product_id"])),
                str(product["product_id"]),
                datetime.now(),
                self.record_source
            )
            hub_data.append(hub_record)
        self._safe_insert("hub_product", hub_data)
        
        console.print("Loading product satellite...")
        sat_data = []
        for product in products:
            sat_record = (
                self._generate_hash_key(str(product["product_id"])),  # product_hk
                datetime.now(),  # load_date
                None,  # load_end_date
                self.record_source,  # record_source
                self._generate_hash_diff({
                    "product_name": product["product_name"],
                    "category": product["category_l1"],
                    "brand": product["brand"],
                    "price": float(product["list_price"])
                }),  # hash_diff
                product["product_name"],
                product["category_l1"],
                product["brand"],
                float(product["list_price"]),
                product.get("description", "")
            )
            sat_data.append(sat_record)
        self._safe_insert("sat_product", sat_data)
    
    def load_suppliers(self, suppliers: List[Dict[str, Any]]):
        """Load supplier data (hub + satellite)."""
        console.print("Loading supplier hub...")
        hub_data = []
        for supplier in suppliers:
            hub_record = (
                self._generate_hash_key(str(supplier["supplier_id"])),
                str(supplier["supplier_id"]),
                datetime.now(),
                self.record_source
            )
            hub_data.append(hub_record)
        self._safe_insert("hub_supplier", hub_data)
        
        console.print("Loading supplier satellite...")
        sat_data = []
        for supplier in suppliers:
            sat_record = (
                self._generate_hash_key(str(supplier["supplier_id"])),  # supplier_hk
                datetime.now(),  # load_date
                None,  # load_end_date
                self.record_source,  # record_source
                self._generate_hash_diff({
                    "supplier_name": supplier["supplier_name"],
                    "contact_person": supplier["contact_person"],
                    "email": supplier["email"],
                    "rating": float(supplier["rating"])
                }),  # hash_diff
                supplier["supplier_name"],
                supplier["contact_person"],
                supplier["email"],
                supplier["phone"],
                supplier["address"],
                supplier["city"],
                supplier["country"],
                float(supplier["rating"])
            )
            sat_data.append(sat_record)
        self._safe_insert("sat_supplier", sat_data)
    
    def load_orders(self, orders: List[Dict[str, Any]]):
        """Load order data (hub + satellite + customer links)."""
        console.print("Loading order hub...")
        hub_data = []
        for order in orders:
            hub_record = (
                self._generate_hash_key(str(order["order_id"])),
                str(order["order_id"]),
                datetime.now(),
                self.record_source
            )
            hub_data.append(hub_record)
        self._safe_insert("hub_order", hub_data)
        
        console.print("Loading order satellite...")
        sat_data = []
        for order in orders:
            sat_record = (
                self._generate_hash_key(str(order["order_id"])),  # order_hk
                datetime.now(),  # load_date
                None,  # load_end_date
                self.record_source,  # record_source
                self._generate_hash_diff({
                    "order_date": order["order_date"],
                    "order_status": order["order_status"],
                    "total_amount": float(order["total_amount"])
                }),  # hash_diff
                order["order_date"],
                order["order_status"],
                float(order["total_amount"]),
                order["shipping_address"],
                order["payment_method"]
            )
            sat_data.append(sat_record)
        self._safe_insert("sat_order", sat_data)
        
        console.print("Loading order-customer links...")
        link_data = []
        for order in orders:
            customer_hk = self._generate_hash_key(str(order["customer_id"]))
            order_hk = self._generate_hash_key(str(order["order_id"]))
            link_hk = self._generate_hash_key(f"{order_hk}{customer_hk}")
            
            link_record = (
                link_hk,
                order_hk,
                customer_hk,
                datetime.now(),
                self.record_source
            )
            link_data.append(link_record)
        self._safe_insert("link_order_customer", link_data)
    
    def load_order_lines(self, order_lines: List[Dict[str, Any]]):
        """Load order line data (link + satellite)."""
        console.print("Loading order-product links...")
        link_data = []
        sat_data = []
        
        for line in order_lines:
            order_hk = self._generate_hash_key(str(line["order_id"]))
            product_hk = self._generate_hash_key(str(line["product_id"]))
            link_hk = self._generate_hash_key(f"{order_hk}{product_hk}{line['order_line_id']}")
            
            # Link record
            link_record = (
                link_hk,
                order_hk,
                product_hk,
                datetime.now(),
                self.record_source
            )
            link_data.append(link_record)
            
            # Satellite for order line details
            sat_attributes = {
                "quantity": int(line["quantity"]),
                "unit_price": float(line["unit_price"]),
                "discount_percent": float(line["discount_percent"]),
                "line_total": float(line["line_total"])
            }
            
            sat_record = (
                link_hk,
                datetime.now(),
                None,
                self.record_source,
                self._generate_hash_diff(sat_attributes),
                int(line["quantity"]),
                float(line["unit_price"]),
                float(line["discount_percent"]),
                float(line["line_total"])
            )
            sat_data.append(sat_record)
        
        self._safe_insert("link_order_product", link_data)
        self._safe_insert("sat_order_line", sat_data)
    
    def load_time_dimension(self, time_data: List[Dict[str, Any]]):
        """Load time dimension data (not typical for Data Vault but included for completeness)."""
        # Data Vault typically doesn't have time dimensions, but we'll skip this
        console.print("Skipping time dimension for Data Vault 1.0 (not applicable)")
        pass

    def get_customer_360_view(self, customer_id: str) -> Dict[str, Any]:
        """Get 360-degree view of a customer using Data Vault 1.0."""
        customer_hk = self._generate_hash_key(str(customer_id))
        
        query = f"""
        SELECT 
            h.customer_id,
            s.first_name,
            s.last_name,
            s.email,
            s.address,
            s.city,
            s.state,
            s.country,
            count(DISTINCT lc.order_hk) as total_orders,
            sum(so.total_amount) as total_spent
        FROM {self.database}.hub_customer h
        LEFT JOIN {self.database}.sat_customer s ON h.customer_hk = s.customer_hk AND s.load_end_date IS NULL
        LEFT JOIN {self.database}.link_order_customer lc ON h.customer_hk = lc.customer_hk
        LEFT JOIN {self.database}.sat_order so ON lc.order_hk = so.order_hk AND so.load_end_date IS NULL
        WHERE h.customer_hk = '{customer_hk}'
        GROUP BY h.customer_id, s.first_name, s.last_name, s.email, s.address, s.city, s.state, s.country
        """
        
        result = self.db.execute_query(query)
        return result.result_rows[0] if result.result_rows else None
