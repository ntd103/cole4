"""
Star Schema implementation - Traditional dimensional modeling.
"""
import json
from datetime import datetime, date
from typing import List, Dict, Any
from utils.database import ClickHouseManager
from rich.console import Console

console = Console()

class StarSchemaManager:
    """Manages Star Schema data loading and operations."""
    
    def __init__(self, db: ClickHouseManager):
        self.db = db
        self.database = "star_schema"
        
    def load_time_dimension(self, time_data: List[Dict[str, Any]]):
        """Load time dimension table."""
        console.print("Loading time dimension...")
        
        time_records = []
        for time_record in time_data:
            dim_record = {
                "time_key": time_record["time_key"],
                "date": time_record["date"],
                "year": time_record["year"],
                "quarter": time_record["quarter"],
                "month": time_record["month"],
                "month_name": time_record["month_name"],
                "day": time_record["day"],
                "day_of_week": time_record["day_of_week"],
                "day_name": time_record["day_name"],
                "week_of_year": time_record["week_of_year"],
                "is_weekend": time_record["is_weekend"],
                "is_holiday": time_record["is_holiday"],
                "holiday_name": time_record["holiday_name"],
                "season": time_record["season"],
                "fiscal_year": time_record["fiscal_year"],
                "fiscal_quarter": time_record["fiscal_quarter"],
                "fiscal_month": time_record["fiscal_month"]
            }
            time_records.append(dim_record)
        
        # Insert in batches
        batch_size = 1000
        for i in range(0, len(time_records), batch_size):
            batch = time_records[i:i + batch_size]
            self.db.execute_insert("dim_time", batch, self.database)
        
        console.print(f"✓ Loaded {len(time_records)} time dimension records")
    
    def load_customer_dimension(self, customers: List[Dict[str, Any]]):
        """Load customer dimension table."""
        console.print("Loading customer dimension...")
        
        customer_records = []
        for i, customer in enumerate(customers):
            dim_record = {
                "customer_key": i + 1,
                "customer_id": customer["customer_id"],
                "first_name": customer["first_name"],
                "last_name": customer["last_name"],
                "full_name": f"{customer['first_name']} {customer['last_name']}",
                "email": customer["email"],
                "phone": customer["phone"],
                "birth_date": customer.get("birth_date"),
                "gender": customer.get("gender", "Unknown"),
                "address": customer["address"],
                "city": customer["city"],
                "state": customer["state"],
                "zip_code": customer["zip_code"],
                "country": customer["country"],
                "registration_date": customer.get("registration_date"),
                "customer_segment": customer.get("customer_segment", "Standard"),
                "loyalty_status": customer.get("loyalty_status", "Bronze"),
                "credit_rating": customer.get("credit_rating", "Good"),
                "is_active": customer.get("is_active", True),
                "effective_date": datetime.now(),
                "expiry_date": None
            }
            customer_records.append(dim_record)
        
        self.db.execute_insert("dim_customer", customer_records, self.database)
        console.print(f"✓ Loaded {len(customer_records)} customer dimension records")
    
    def load_product_dimension(self, products: List[Dict[str, Any]]):
        """Load product dimension table."""
        console.print("Loading product dimension...")
        
        product_records = []
        for i, product in enumerate(products):
            dim_record = {
                "product_key": i + 1,
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "sku": product["sku"],
                "category": product["category_l1"],
                "subcategory": product["category_l2"],
                "brand": product["brand"],
                "model": product.get("model", ""),
                "color": product.get("color", ""),
                "size": product.get("size", ""),
                "weight": float(product.get("weight", 0)),
                "cost": float(product["cost"]),
                "list_price": float(product["list_price"]),
                "launch_date": product.get("launch_date"),
                "status": product.get("status", "Active"),
                "rating": float(product.get("rating", 0)),
                "is_active": product.get("status") == "Active",
                "effective_date": datetime.now(),
                "expiry_date": None
            }
            product_records.append(dim_record)
        
        self.db.execute_insert("dim_product", product_records, self.database)
        console.print(f"✓ Loaded {len(product_records)} product dimension records")
    
    def load_geography_dimension(self, customers: List[Dict[str, Any]]):
        """Load geography dimension from customer addresses."""
        console.print("Loading geography dimension...")
        
        # Create unique geography records
        geography_map = {}
        geography_records = []
        geo_key = 1
        
        for customer in customers:
            geo_identifier = f"{customer['address']}|{customer['city']}|{customer['state']}|{customer['zip_code']}|{customer['country']}"
            
            if geo_identifier not in geography_map:
                geography_map[geo_identifier] = geo_key
                
                dim_record = {
                    "geography_key": geo_key,
                    "address": customer["address"],
                    "city": customer["city"],
                    "state": customer["state"],
                    "zip_code": customer["zip_code"],
                    "country": customer["country"],
                    "region": self._get_region(customer["country"]),
                    "continent": self._get_continent(customer["country"]),
                    "time_zone": self._get_timezone(customer["state"]),
                    "population": self._get_city_population(customer["city"]),
                    "area_code": customer["zip_code"][:3] if customer["zip_code"] else "000"
                }
                geography_records.append(dim_record)
                geo_key += 1
        
        self.db.execute_insert("dim_geography", geography_records, self.database)
        console.print(f"✓ Loaded {len(geography_records)} geography dimension records")
        
        return geography_map
    
    def load_supplier_dimension(self, suppliers: List[Dict[str, Any]]):
        """Load supplier dimension table."""
        console.print("Loading supplier dimension...")
        
        supplier_records = []
        for i, supplier in enumerate(suppliers):
            dim_record = {
                "supplier_key": i + 1,
                "supplier_id": supplier["supplier_id"],
                "supplier_name": supplier["supplier_name"],
                "contact_person": supplier["contact_person"],
                "email": supplier["email"],
                "phone": supplier["phone"],
                "address": supplier["address"],
                "city": supplier["city"],
                "country": supplier["country"],
                "region": supplier.get("region", "Unknown"),
                "rating": float(supplier["rating"]),
                "contract_start_date": supplier.get("contract_start_date"),
                "contract_end_date": supplier.get("contract_end_date"),
                "is_active": supplier.get("is_active", True)
            }
            supplier_records.append(dim_record)
        
        self.db.execute_insert("dim_supplier", supplier_records, self.database)
        console.print(f"✓ Loaded {len(supplier_records)} supplier dimension records")
    
    def load_sales_channel_dimension(self):
        """Load sales channel dimension table."""
        console.print("Loading sales channel dimension...")
        
        channels = [
            {"channel_id": "ONL", "channel_name": "Online", "channel_type": "Digital", "channel_category": "E-commerce", "manager_name": "Alice Johnson", "commission_rate": 2.5},
            {"channel_id": "RET", "channel_name": "Retail Store", "channel_type": "Physical", "channel_category": "Brick & Mortar", "manager_name": "Bob Smith", "commission_rate": 5.0},
            {"channel_id": "MOB", "channel_name": "Mobile App", "channel_type": "Digital", "channel_category": "Mobile", "manager_name": "Carol Brown", "commission_rate": 2.0},
            {"channel_id": "PHN", "channel_name": "Phone", "channel_type": "Call Center", "channel_category": "Telemarketing", "manager_name": "David Wilson", "commission_rate": 7.5},
            {"channel_id": "PAR", "channel_name": "Partner", "channel_type": "External", "channel_category": "Channel Partner", "manager_name": "Eva Davis", "commission_rate": 10.0}
        ]
        
        channel_records = []
        for i, channel in enumerate(channels):
            dim_record = {
                "channel_key": i + 1,
                "channel_id": channel["channel_id"],
                "channel_name": channel["channel_name"],
                "channel_type": channel["channel_type"],
                "channel_category": channel["channel_category"],
                "manager_name": channel["manager_name"],
                "commission_rate": float(channel["commission_rate"]),
                "is_active": True
            }
            channel_records.append(dim_record)
        
        self.db.execute_insert("dim_sales_channel", channel_records, self.database)
        console.print(f"✓ Loaded {len(channel_records)} sales channel dimension records")
    
    def load_promotion_dimension(self):
        """Load promotion dimension table."""
        console.print("Loading promotion dimension...")
        
        promotions = [
            {"promotion_id": "NONE", "promotion_name": "No Promotion", "promotion_type": "None", "discount_type": "None", "discount_value": 0.0},
            {"promotion_id": "SAVE10", "promotion_name": "Save 10%", "promotion_type": "Percentage", "discount_type": "Percentage", "discount_value": 10.0},
            {"promotion_id": "SAVE20", "promotion_name": "Save 20%", "promotion_type": "Percentage", "discount_type": "Percentage", "discount_value": 20.0},
            {"promotion_id": "FLAT50", "promotion_name": "Flat $50 Off", "promotion_type": "Fixed Amount", "discount_type": "Fixed", "discount_value": 50.0},
            {"promotion_id": "BOGO", "promotion_name": "Buy One Get One", "promotion_type": "BOGO", "discount_type": "Special", "discount_value": 50.0}
        ]
        
        promotion_records = []
        for i, promotion in enumerate(promotions):
            dim_record = {
                "promotion_key": i + 1,
                "promotion_id": promotion["promotion_id"],
                "promotion_name": promotion["promotion_name"],
                "promotion_type": promotion["promotion_type"],
                "discount_type": promotion["discount_type"],
                "discount_value": float(promotion["discount_value"]),
                "start_date": date(2022, 1, 1),
                "end_date": date(2025, 12, 31),
                "is_active": True
            }
            promotion_records.append(dim_record)
        
        self.db.execute_insert("dim_promotion", promotion_records, self.database)
        console.print(f"✓ Loaded {len(promotion_records)} promotion dimension records")
    
    def load_fact_sales(self, customers: List[Dict[str, Any]], products: List[Dict[str, Any]], 
                       suppliers: List[Dict[str, Any]], orders: List[Dict[str, Any]], 
                       order_lines: List[Dict[str, Any]], geography_map: Dict[str, int]):
        """Load central fact table."""
        console.print("Loading fact sales table...")
        
        # Create lookups for dimension keys
        customer_lookup = {customers[i]["customer_id"]: i + 1 for i in range(len(customers))}
        product_lookup = {products[i]["product_id"]: i + 1 for i in range(len(products))}
        supplier_lookup = {}
        
        # Assign suppliers to products randomly for demo
        import random
        for i, product in enumerate(products):
            supplier_key = random.randint(1, len(suppliers))
            supplier_lookup[product["product_id"]] = supplier_key
        
        # Channel and promotion mappings
        channel_map = {"Online": 1, "Retail Store": 2, "Mobile App": 3, "Phone": 4, "Partner": 5}
        
        order_lookup = {o["order_id"]: o for o in orders}
        
        fact_records = []
        sales_key = 1
        
        for line in order_lines:
            order = order_lookup.get(line["order_id"])
            if not order:
                continue
            
            customer_key = customer_lookup.get(order["customer_id"])
            product_key = product_lookup.get(line["product_id"])
            
            if not customer_key or not product_key:
                continue
            
            # Get customer for geography lookup
            customer = next((c for c in customers if c["customer_id"] == order["customer_id"]), None)
            if not customer:
                continue
            
            # Geography keys
            geo_identifier = f"{customer['address']}|{customer['city']}|{customer['state']}|{customer['zip_code']}|{customer['country']}"
            geography_key = geography_map.get(geo_identifier, 1)
            
            # Other dimension keys
            supplier_key = supplier_lookup.get(line["product_id"], 1)
            channel_key = channel_map.get(order.get("sales_channel", "Online"), 1)
            promotion_key = 1  # Default to no promotion
            
            if order.get("promotion_code"):
                if "10" in order["promotion_code"]:
                    promotion_key = 2
                elif "20" in order["promotion_code"]:
                    promotion_key = 3
                else:
                    promotion_key = 4
            
            # Convert order date to time key
            order_date = order["order_date"]
            if isinstance(order_date, str):
                order_datetime = datetime.fromisoformat(order_date.replace('Z', '+00:00'))
            else:
                order_datetime = order_date
            
            time_key = int(order_datetime.strftime("%Y%m%d"))
            
            # Calculate metrics
            profit_amount = float(line["line_total"]) - (float(line["cost_amount"]) if "cost_amount" in line else 0)
            profit_margin = (profit_amount / float(line["line_total"])) * 100 if float(line["line_total"]) > 0 else 0
            
            fact_record = {
                "sales_key": sales_key,
                "time_key": time_key,
                "customer_key": customer_key,
                "product_key": product_key,
                "supplier_key": supplier_key,
                "geography_key": geography_key,
                "billing_geography_key": geography_key,  # Same as shipping for demo
                "channel_key": channel_key,
                "promotion_key": promotion_key,
                
                # Degenerate dimensions
                "order_id": line["order_id"],
                "order_line_id": line["order_line_id"],
                "invoice_number": f"INV{order['order_id'][4:]}",
                
                # Measures
                "quantity": int(line["quantity"]),
                "unit_price": float(line["unit_price"]),
                "discount_amount": float(line["discount_amount"]),
                "line_total": float(line["line_total"]),
                "cost_amount": float(line.get("cost_amount", line["unit_price"]) if "cost_amount" in line else float(line["unit_price"]) * 0.6),
                "profit_amount": round(profit_amount, 2),
                "tax_amount": round(float(line["line_total"]) * 0.08, 2),
                "shipping_cost": round(float(order.get("shipping_cost", 10.00)) / max(self._count_order_lines(order["order_id"], order_lines), 1), 2),
                
                # Semi-additive measures
                "inventory_quantity": random.randint(10, 1000),
                "unit_cost": float(line.get("cost_amount", line["unit_price"]) if "cost_amount" in line else float(line["unit_price"]) * 0.6),
                
                # Non-additive measures
                "profit_margin": round(profit_margin, 2),
                "discount_percent": float(line["discount_percent"]),
                
                # Flags
                "is_returned": random.choice([True, False, False, False, False]),
                "is_exchange": False,
                
                # Timestamps
                "order_timestamp": order_datetime,
                "shipped_timestamp": order.get("shipped_timestamp"),
                "delivered_timestamp": order.get("delivered_timestamp")
            }
            
            fact_records.append(fact_record)
            sales_key += 1
            
            # Insert in batches
            if len(fact_records) >= 1000:
                self.db.execute_insert("fact_sales", fact_records, self.database)
                fact_records = []
        
        # Insert remaining records
        if fact_records:
            self.db.execute_insert("fact_sales", fact_records, self.database)
        
        console.print(f"✓ Loaded {sales_key - 1} fact sales records")
    
    def _get_region(self, country: str) -> str:
        """Get region based on country."""
        if country in ["USA", "Canada", "Mexico"]:
            return "North America"
        elif country in ["UK", "Germany", "France", "Italy", "Spain"]:
            return "Europe"
        elif country in ["China", "Japan", "India", "South Korea"]:
            return "Asia"
        else:
            return "Other"
    
    def _get_continent(self, country: str) -> str:
        """Get continent based on country."""
        if country in ["USA", "Canada", "Mexico"]:
            return "North America"
        elif country in ["UK", "Germany", "France", "Italy", "Spain"]:
            return "Europe"
        elif country in ["China", "Japan", "India", "South Korea"]:
            return "Asia"
        else:
            return "Other"
    
    def _get_timezone(self, state: str) -> str:
        """Get timezone based on state."""
        eastern = ["NY", "FL", "GA", "NC", "SC", "VA", "WV", "OH", "PA", "NJ", "CT", "RI", "MA", "VT", "NH", "ME", "DE", "MD", "DC"]
        central = ["TX", "OK", "KS", "NE", "SD", "ND", "MN", "IA", "MO", "AR", "LA", "MS", "AL", "TN", "KY", "IL", "WI", "IN", "MI"]
        mountain = ["MT", "WY", "CO", "NM", "ID", "UT", "AZ"]
        pacific = ["CA", "OR", "WA", "NV"]
        
        if state in eastern:
            return "Eastern"
        elif state in central:
            return "Central"
        elif state in mountain:
            return "Mountain"
        elif state in pacific:
            return "Pacific"
        else:
            return "Unknown"
    
    def _get_city_population(self, city: str) -> int:
        """Get estimated city population."""
        import random
        return random.randint(10000, 1000000)
    
    def _count_order_lines(self, order_id: str, order_lines: List[Dict[str, Any]]) -> int:
        """Count number of lines in an order."""
        return len([line for line in order_lines if line["order_id"] == order_id])
    
    def load_data(self):
        """Load all data into star schema."""
        console.print("[bold blue]Loading Star Schema...[/bold blue]")
        
        # Load sample data
        import json
        
        with open("data/customers.json", "r") as f:
            customers = json.load(f)
        
        with open("data/products.json", "r") as f:
            products = json.load(f)
        
        with open("data/suppliers.json", "r") as f:
            suppliers = json.load(f)
        
        with open("data/orders.json", "r") as f:
            orders = json.load(f)
        
        with open("data/order_lines.json", "r") as f:
            order_lines = json.load(f)
        
        with open("data/time_dimension.json", "r") as f:
            time_data = json.load(f)
        
        # Load dimensions first
        self.load_time_dimension(time_data)
        self.load_customer_dimension(customers)
        self.load_product_dimension(products)
        geography_map = self.load_geography_dimension(customers)
        self.load_supplier_dimension(suppliers)
        self.load_sales_channel_dimension()
        self.load_promotion_dimension()
        
        # Load fact table
        self.load_fact_sales(customers, products, suppliers, orders, order_lines, geography_map)
        
        console.print("[bold green]✓ Star Schema loading completed![/bold green]")
    
    def get_sales_by_dimension(self, dimension: str, limit: int = 10) -> List[Any]:
        """Get top sales by specified dimension."""
        dimension_columns = {
            "customer": "dc.full_name",
            "product": "dp.product_name",
            "geography": "dg.city",
            "time": "dt.month_name",
            "channel": "dsc.channel_name"
        }
        
        if dimension not in dimension_columns:
            return []
        
        query = f"""
        SELECT 
            {dimension_columns[dimension]} as dimension_value,
            sum(fs.line_total) as total_sales,
            sum(fs.quantity) as total_quantity,
            count() as transaction_count
        FROM {self.database}.fact_sales fs
        LEFT JOIN {self.database}.dim_customer dc ON fs.customer_key = dc.customer_key
        LEFT JOIN {self.database}.dim_product dp ON fs.product_key = dp.product_key
        LEFT JOIN {self.database}.dim_geography dg ON fs.geography_key = dg.geography_key
        LEFT JOIN {self.database}.dim_time dt ON fs.time_key = dt.time_key
        LEFT JOIN {self.database}.dim_sales_channel dsc ON fs.channel_key = dsc.channel_key
        GROUP BY {dimension_columns[dimension]}
        ORDER BY total_sales DESC
        LIMIT {limit}
        """
        
        result = self.db.execute_query(query)
        return result.result_rows
