"""
Big Fact Table implementation - Denormalized approach.
"""
import json
from datetime import datetime
from typing import List, Dict, Any
from utils.database import ClickHouseManager
from rich.console import Console

console = Console()

class BigFactManager:
    """Manages Big Fact Table data loading and operations."""
    
    def __init__(self, db: ClickHouseManager):
        self.db = db
        self.database = "big_fact"
        
    def load_big_fact_table(self, customers: List[Dict[str, Any]], products: List[Dict[str, Any]], 
                           suppliers: List[Dict[str, Any]], orders: List[Dict[str, Any]], 
                           order_lines: List[Dict[str, Any]]):
        """Load the big denormalized fact table."""
        console.print("Loading big fact table...")
        
        # Create lookups for joining data
        customer_lookup = {c["customer_id"]: c for c in customers}
        product_lookup = {p["product_id"]: p for p in products}
        supplier_lookup = {s["supplier_id"]: s for s in suppliers}
        order_lookup = {o["order_id"]: o for o in orders}
        
        # Assign products to suppliers randomly for demo
        import random
        for product in products:
            product["supplier_id"] = random.choice(suppliers)["supplier_id"]
        
        big_fact_data = []
        transaction_id = 1
        
        for line in order_lines:
            order = order_lookup.get(line["order_id"])
            if not order:
                continue
                
            customer = customer_lookup.get(order["customer_id"])
            product = product_lookup.get(line["product_id"])
            
            if not customer or not product:
                continue
            
            # Get supplier for this product
            supplier = supplier_lookup.get(product["supplier_id"])
            if not supplier:
                supplier = suppliers[0]  # Fallback
            
            # Convert dates
            order_date = order["order_date"]
            if isinstance(order_date, str):
                order_datetime = datetime.fromisoformat(order_date.replace('Z', '+00:00'))
                order_date = order_datetime.date()
            else:
                order_datetime = order_date
                order_date = order_date.date()
            
            # Calculate derived fields
            profit_amount = float(line["line_total"]) - (float(product["cost"]) * int(line["quantity"]))
            profit_margin = (profit_amount / float(line["line_total"])) * 100 if float(line["line_total"]) > 0 else 0
            
            # Determine customer age
            customer_age = 30  # Simplified for demo
            if customer.get("birth_date"):
                try:
                    birth_date = datetime.fromisoformat(str(customer["birth_date"]).replace('Z', '+00:00')).date()
                    customer_age = (order_date - birth_date).days // 365
                except:
                    customer_age = 30
            
            # Big fact record with all denormalized data
            big_fact_record = {
                # Primary identifiers
                "transaction_id": f"TXN_{transaction_id:010d}",
                "order_id": line["order_id"],
                "order_line_id": line["order_line_id"],
                
                # Time dimensions (denormalized)
                "order_date": order_date,
                "order_datetime": order_datetime,
                "order_year": order_date.year,
                "order_quarter": (order_date.month - 1) // 3 + 1,
                "order_month": order_date.month,
                "order_day": order_date.day,
                "order_day_of_week": order_date.weekday() + 1,
                "order_week": order_date.isocalendar()[1],
                "is_weekend": order_date.weekday() >= 5,
                "is_holiday": False,
                "season": self._get_season(order_date.month),
                
                # Customer dimensions (denormalized)
                "customer_id": customer["customer_id"],
                "customer_first_name": customer["first_name"],
                "customer_last_name": customer["last_name"],
                "customer_full_name": f"{customer['first_name']} {customer['last_name']}",
                "customer_email": customer["email"],
                "customer_phone": customer["phone"],
                "customer_birth_date": customer.get("birth_date"),
                "customer_age": customer_age,
                "customer_gender": customer.get("gender", "Unknown"),
                "customer_address": customer["address"],
                "customer_city": customer["city"],
                "customer_state": customer["state"],
                "customer_zip_code": customer["zip_code"],
                "customer_country": customer["country"],
                "customer_registration_date": customer.get("registration_date"),
                "customer_segment": customer.get("customer_segment", "Standard"),
                "customer_loyalty_status": customer.get("loyalty_status", "Bronze"),
                "customer_credit_rating": customer.get("credit_rating", "Good"),
                "customer_annual_income": float(customer.get("annual_income", 50000)),
                
                # Product dimensions (denormalized)
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "product_sku": product["sku"],
                "product_category_l1": product["category_l1"],
                "product_category_l2": product["category_l2"],
                "product_category_l3": product.get("category_l3", ""),
                "product_brand": product["brand"],
                "product_model": product.get("model", ""),
                "product_color": product.get("color", ""),
                "product_size": product.get("size", ""),
                "product_weight": float(product.get("weight", 0)),
                "product_cost": float(product["cost"]),
                "product_list_price": float(product["list_price"]),
                "product_launch_date": product.get("launch_date"),
                "product_status": product.get("status", "Active"),
                "product_rating": float(product.get("rating", 0)),
                
                # Supplier dimensions (denormalized)
                "supplier_id": supplier["supplier_id"],
                "supplier_name": supplier["supplier_name"],
                "supplier_country": supplier["country"],
                "supplier_region": supplier.get("region", "Unknown"),
                "supplier_rating": float(supplier["rating"]),
                "supplier_contact_person": supplier["contact_person"],
                "supplier_email": supplier["email"],
                "supplier_phone": supplier["phone"],
                
                # Geography dimensions (denormalized)
                "shipping_address": order.get("shipping_address", customer["address"]),
                "shipping_city": order.get("shipping_city", customer["city"]),
                "shipping_state": order.get("shipping_state", customer["state"]),
                "shipping_zip_code": customer["zip_code"],
                "shipping_country": order.get("shipping_country", customer["country"]),
                "shipping_region": self._get_region(customer["country"]),
                "billing_address": order.get("billing_address", customer["address"]),
                "billing_city": order.get("billing_city", customer["city"]),
                "billing_state": order.get("billing_state", customer["state"]),
                "billing_zip_code": customer["zip_code"],
                "billing_country": order.get("billing_country", customer["country"]),
                
                # Sales metrics
                "quantity": int(line["quantity"]),
                "unit_price": float(line["unit_price"]),
                "list_price": float(product["list_price"]),
                "discount_amount": float(line["discount_amount"]),
                "discount_percent": float(line["discount_percent"]),
                "line_total": float(line["line_total"]),
                "cost_amount": float(product["cost"]) * int(line["quantity"]),
                "profit_amount": round(profit_amount, 2),
                "profit_margin": round(profit_margin, 2),
                
                # Order level metrics (repeated for each line)
                "order_total_amount": float(order["total_amount"]),
                "order_total_items": self._count_order_items(order["order_id"], order_lines),
                "order_total_weight": self._calculate_order_weight(order["order_id"], order_lines, product_lookup),
                "shipping_cost": float(order.get("shipping_cost", 10.00)),
                "tax_amount": float(order.get("tax_amount", float(order["total_amount"]) * 0.08)),
                
                # Operational dimensions
                "order_status": order["order_status"],
                "payment_method": order["payment_method"],
                "payment_status": order.get("payment_status", "Paid"),
                "shipping_method": order.get("shipping_method", "Standard"),
                "shipping_carrier": order.get("shipping_carrier", "UPS"),
                "tracking_number": f"TRK{random.randint(1000000000, 9999999999)}",
                "warehouse_id": f"WH{random.randint(1, 5):02d}",
                "warehouse_name": f"Warehouse {random.randint(1, 5)}",
                "warehouse_region": random.choice(["North", "South", "East", "West", "Central"]),
                "sales_rep_id": f"REP{random.randint(1, 50):03d}",
                "sales_rep_name": f"Rep {random.randint(1, 50)}",
                "sales_channel": order.get("sales_channel", "Online"),
                "promotion_code": order.get("promotion_code"),
                "promotion_name": f"Promotion {order.get('promotion_code', '')}" if order.get("promotion_code") else None,
                "promotion_type": "Discount" if order.get("promotion_code") else None,
                
                # Flags and indicators
                "is_first_purchase": random.choice([True, False]),
                "is_repeat_customer": random.choice([True, True, True, False]),
                "is_bulk_order": int(line["quantity"]) > 5,
                "is_expedited_shipping": order.get("shipping_method") == "Express",
                "is_gift_order": random.choice([True, False]),
                "has_discount": float(line["discount_percent"]) > 0,
                "has_promotion": order.get("promotion_code") is not None,
                "is_returned": random.choice([True, False, False, False, False]),
                "return_date": None,
                "return_reason": None,
                
                # Timestamps
                "created_timestamp": order_datetime,
                "updated_timestamp": order_datetime,
                "shipped_timestamp": order.get("shipped_timestamp"),
                "delivered_timestamp": order.get("delivered_timestamp")
            }
            
            big_fact_data.append(big_fact_record)
            transaction_id += 1
            
            # Insert in batches to avoid memory issues
            if len(big_fact_data) >= 1000:
                self.db.execute_insert("big_fact_sales", big_fact_data, self.database)
                big_fact_data = []
        
        # Insert remaining records
        if big_fact_data:
            self.db.execute_insert("big_fact_sales", big_fact_data, self.database)
        
        console.print(f"✓ Loaded {transaction_id - 1} records into big fact table")
    
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
    
    def _get_region(self, country: str) -> str:
        """Get region based on country."""
        # Simplified mapping
        if country in ["USA", "Canada", "Mexico"]:
            return "North America"
        elif country in ["UK", "Germany", "France", "Italy", "Spain"]:
            return "Europe"
        elif country in ["China", "Japan", "India", "South Korea"]:
            return "Asia"
        else:
            return "Other"
    
    def _count_order_items(self, order_id: str, order_lines: List[Dict[str, Any]]) -> int:
        """Count total items in an order."""
        total_items = 0
        for line in order_lines:
            if line["order_id"] == order_id:
                total_items += int(line["quantity"])
        return total_items
    
    def _calculate_order_weight(self, order_id: str, order_lines: List[Dict[str, Any]], 
                              product_lookup: Dict[str, Dict[str, Any]]) -> float:
        """Calculate total weight of an order."""
        total_weight = 0.0
        for line in order_lines:
            if line["order_id"] == order_id:
                product = product_lookup.get(line["product_id"])
                if product:
                    weight = float(product.get("weight", 0))
                    quantity = int(line["quantity"])
                    total_weight += weight * quantity
        return round(total_weight, 2)
    
    def load_data(self):
        """Load all data into big fact table."""
        console.print("[bold blue]Loading Big Fact Table...[/bold blue]")
        
        # Load sample data
        import json
        import random
        
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
        
        # Load the big fact table
        self.load_big_fact_table(customers, products, suppliers, orders, order_lines)
        
        console.print("[bold green]✓ Big Fact Table loading completed![/bold green]")
    
    def get_customer_summary(self, customer_id: str) -> Dict[str, Any]:
        """Get customer summary from big fact table."""
        query = f"""
        SELECT 
            customer_id,
            customer_full_name,
            customer_segment,
            customer_loyalty_status,
            count() as total_transactions,
            sum(quantity) as total_items_purchased,
            sum(line_total) as total_spent,
            avg(line_total) as avg_transaction_value,
            sum(profit_amount) as total_profit_generated,
            min(order_date) as first_purchase_date,
            max(order_date) as last_purchase_date,
            uniq(product_category_l1) as categories_purchased,
            uniq(product_brand) as brands_purchased
        FROM {self.database}.big_fact_sales
        WHERE customer_id = '{customer_id}'
        GROUP BY customer_id, customer_full_name, customer_segment, customer_loyalty_status
        """
        
        result = self.db.execute_query(query)
        return result.result_rows[0] if result.result_rows else None
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get overall performance metrics from big fact table."""
        query = f"""
        SELECT 
            count() as total_transactions,
            sum(line_total) as total_revenue,
            sum(profit_amount) as total_profit,
            avg(profit_margin) as avg_profit_margin,
            uniq(customer_id) as unique_customers,
            uniq(product_id) as unique_products,
            avg(quantity) as avg_quantity_per_transaction,
            avg(line_total) as avg_transaction_value
        FROM {self.database}.big_fact_sales
        """
        
        result = self.db.execute_query(query)
        return result.result_rows[0] if result.result_rows else None
