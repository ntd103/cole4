"""
Snowflake Schema implementation - Normalized dimensional modeling.
"""
import json
from datetime import datetime, date
from typing import List, Dict, Any
from utils.database import ClickHouseManager
from rich.console import Console

console = Console()

class SnowflakeSchemaManager:
    """Manages Snowflake Schema data loading and operations."""
    
    def __init__(self, db: ClickHouseManager):
        self.db = db
        self.database = "snowflake_schema"
        
    def load_normalized_time_dimensions(self, time_data: List[Dict[str, Any]]):
        """Load normalized time hierarchy dimensions."""
        console.print("Loading normalized time dimensions...")
        
        # Load year dimension
        years = {}
        year_records = []
        for time_record in time_data:
            year = time_record["year"]
            if year not in years:
                years[year] = len(years) + 1
                year_record = {
                    "year_key": years[year],
                    "year_number": year,
                    "fiscal_year": time_record["fiscal_year"],
                    "is_leap_year": year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
                }
                year_records.append(year_record)
        
        self.db.execute_insert("dim_year", year_records, self.database)
        
        # Load quarter dimension
        quarters = {}
        quarter_records = []
        for time_record in time_data:
            quarter_key = f"{time_record['year']}_Q{time_record['quarter']}"
            if quarter_key not in quarters:
                quarters[quarter_key] = len(quarters) + 1
                quarter_record = {
                    "quarter_key": quarters[quarter_key],
                    "year_key": years[time_record["year"]],
                    "quarter_number": time_record["quarter"],
                    "quarter_name": f"Q{time_record['quarter']} {time_record['year']}",
                    "fiscal_quarter": time_record["fiscal_quarter"]
                }
                quarter_records.append(quarter_record)
        
        self.db.execute_insert("dim_quarter", quarter_records, self.database)
        
        # Load month dimension
        months = {}
        month_records = []
        for time_record in time_data:
            month_key = f"{time_record['year']}{time_record['month']:02d}"
            if month_key not in months:
                months[month_key] = len(months) + 1
                quarter_key = f"{time_record['year']}_Q{time_record['quarter']}"
                month_record = {
                    "month_key": months[month_key],
                    "quarter_key": quarters[quarter_key],
                    "month_number": time_record["month"],
                    "month_name": time_record["month_name"],
                    "month_abbr": time_record["month_name"][:3],
                    "days_in_month": self._get_days_in_month(time_record["year"], time_record["month"]),
                    "fiscal_month": time_record["fiscal_month"]
                }
                month_records.append(month_record)
        
        self.db.execute_insert("dim_month", month_records, self.database)
        
        # Load date dimension
        date_records = []
        for time_record in time_data:
            month_key = f"{time_record['year']}{time_record['month']:02d}"
            date_record = {
                "date_key": time_record["time_key"],
                "month_key": months[month_key],
                "date": time_record["date"],
                "day_number": time_record["day"],
                "day_name": time_record["day_name"],
                "day_abbr": time_record["day_name"][:3],
                "day_of_week": time_record["day_of_week"],
                "day_of_year": self._get_day_of_year(time_record["date"]),
                "week_of_year": time_record["week_of_year"],
                "is_weekend": time_record["is_weekend"],
                "is_holiday": time_record["is_holiday"],
                "holiday_name": time_record["holiday_name"]
            }
            date_records.append(date_record)
        
        # Insert in batches
        batch_size = 1000
        for i in range(0, len(date_records), batch_size):
            batch = date_records[i:i + batch_size]
            self.db.execute_insert("dim_date", batch, self.database)
        
        console.print("✓ Loaded normalized time dimensions")
        return {"years": years, "quarters": quarters, "months": months}
    
    def load_normalized_geography_dimensions(self, customers: List[Dict[str, Any]]):
        """Load normalized geography hierarchy dimensions."""
        console.print("Loading normalized geography dimensions...")
        
        # Load continent dimension
        continents = {}
        continent_records = []
        continents_data = [
            {"code": "NA", "name": "North America"},
            {"code": "EU", "name": "Europe"},
            {"code": "AS", "name": "Asia"},
            {"code": "SA", "name": "South America"},
            {"code": "AF", "name": "Africa"},
            {"code": "OC", "name": "Oceania"},
            {"code": "AN", "name": "Antarctica"}
        ]
        
        for i, continent in enumerate(continents_data):
            continents[continent["name"]] = i + 1
            continent_record = {
                "continent_key": i + 1,
                "continent_code": continent["code"],
                "continent_name": continent["name"]
            }
            continent_records.append(continent_record)
        
        self.db.execute_insert("dim_continent", continent_records, self.database)
        
        # Load country dimension
        countries = {}
        country_records = []
        country_key = 1
        
        for customer in customers:
            country = customer["country"]
            if country not in countries:
                countries[country] = country_key
                continent_name = self._get_continent(country)
                country_record = {
                    "country_key": country_key,
                    "continent_key": continents.get(continent_name, 1),
                    "country_code": country[:2].upper(),
                    "country_name": country,
                    "currency_code": self._get_currency(country),
                    "phone_prefix": f"+{country_key}"
                }
                country_records.append(country_record)
                country_key += 1
        
        self.db.execute_insert("dim_country", country_records, self.database)
        
        # Load state dimension
        states = {}
        state_records = []
        state_key = 1
        
        for customer in customers:
            state_id = f"{customer['country']}_{customer['state']}"
            if state_id not in states:
                states[state_id] = state_key
                state_record = {
                    "state_key": state_key,
                    "country_key": countries[customer["country"]],
                    "state_code": customer["state"],
                    "state_name": customer["state"],
                    "capital_city": f"Capital of {customer['state']}",
                    "population": self._get_state_population()
                }
                state_records.append(state_record)
                state_key += 1
        
        self.db.execute_insert("dim_state", state_records, self.database)
        
        # Load city dimension
        cities = {}
        city_records = []
        city_key = 1
        
        for customer in customers:
            city_id = f"{customer['country']}_{customer['state']}_{customer['city']}"
            if city_id not in cities:
                cities[city_id] = city_key
                state_id = f"{customer['country']}_{customer['state']}"
                city_record = {
                    "city_key": city_key,
                    "state_key": states[state_id],
                    "city_name": customer["city"],
                    "zip_code": customer["zip_code"],
                    "population": self._get_city_population(),
                    "area_code": customer["zip_code"][:3] if customer["zip_code"] else "000",
                    "time_zone": self._get_timezone(customer["state"])
                }
                city_records.append(city_record)
                city_key += 1
        
        self.db.execute_insert("dim_city", city_records, self.database)
        
        console.print("✓ Loaded normalized geography dimensions")
        return {"continents": continents, "countries": countries, "states": states, "cities": cities}
    
    def load_normalized_product_dimensions(self, products: List[Dict[str, Any]]):
        """Load normalized product hierarchy dimensions."""
        console.print("Loading normalized product dimensions...")
        
        # Load brand dimension
        brands = {}
        brand_records = []
        brand_key = 1
        
        for product in products:
            brand = product["brand"]
            if brand not in brands:
                brands[brand] = brand_key
                brand_record = {
                    "brand_key": brand_key,
                    "brand_code": brand[:3].upper(),
                    "brand_name": brand,
                    "brand_owner": f"{brand} Corporation",
                    "established_year": 1990 + (brand_key % 30)
                }
                brand_records.append(brand_record)
                brand_key += 1
        
        self.db.execute_insert("dim_brand", brand_records, self.database)
        
        # Load category level 1 dimension
        categories_l1 = {}
        category_l1_records = []
        cat_l1_key = 1
        
        for product in products:
            cat_l1 = product["category_l1"]
            if cat_l1 not in categories_l1:
                categories_l1[cat_l1] = cat_l1_key
                cat_l1_record = {
                    "category_l1_key": cat_l1_key,
                    "category_l1_code": cat_l1[:4].upper(),
                    "category_l1_name": cat_l1,
                    "category_manager": f"Manager for {cat_l1}"
                }
                category_l1_records.append(cat_l1_record)
                cat_l1_key += 1
        
        self.db.execute_insert("dim_category_l1", category_l1_records, self.database)
        
        # Load category level 2 dimension
        categories_l2 = {}
        category_l2_records = []
        cat_l2_key = 1
        
        for product in products:
            cat_l2_id = f"{product['category_l1']}_{product['category_l2']}"
            if cat_l2_id not in categories_l2:
                categories_l2[cat_l2_id] = cat_l2_key
                cat_l2_record = {
                    "category_l2_key": cat_l2_key,
                    "category_l1_key": categories_l1[product["category_l1"]],
                    "category_l2_code": product["category_l2"][:4].upper(),
                    "category_l2_name": product["category_l2"]
                }
                category_l2_records.append(cat_l2_record)
                cat_l2_key += 1
        
        self.db.execute_insert("dim_category_l2", category_l2_records, self.database)
        
        # Load category level 3 dimension
        categories_l3 = {}
        category_l3_records = []
        cat_l3_key = 1
        
        for product in products:
            cat_l3 = product.get("category_l3", f"{product['category_l2']} - Default")
            cat_l3_id = f"{product['category_l1']}_{product['category_l2']}_{cat_l3}"
            if cat_l3_id not in categories_l3:
                categories_l3[cat_l3_id] = cat_l3_key
                cat_l2_id = f"{product['category_l1']}_{product['category_l2']}"
                cat_l3_record = {
                    "category_l3_key": cat_l3_key,
                    "category_l2_key": categories_l2[cat_l2_id],
                    "category_l3_code": cat_l3[:4].upper(),
                    "category_l3_name": cat_l3
                }
                category_l3_records.append(cat_l3_record)
                cat_l3_key += 1
        
        self.db.execute_insert("dim_category_l3", category_l3_records, self.database)
        
        # Load product dimension
        product_records = []
        for i, product in enumerate(products):
            cat_l3 = product.get("category_l3", f"{product['category_l2']} - Default")
            cat_l3_id = f"{product['category_l1']}_{product['category_l2']}_{cat_l3}"
            
            product_record = {
                "product_key": i + 1,
                "category_l3_key": categories_l3[cat_l3_id],
                "brand_key": brands[product["brand"]],
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "sku": product["sku"],
                "model": product.get("model", ""),
                "color": product.get("color", ""),
                "size": product.get("size", ""),
                "weight": float(product.get("weight", 0)),
                "cost": float(product["cost"]),
                "list_price": float(product["list_price"]),
                "launch_date": product.get("launch_date"),
                "status": product.get("status", "Active"),
                "rating": float(product.get("rating", 0)),
                "is_active": product.get("status") == "Active"
            }
            product_records.append(product_record)
        
        self.db.execute_insert("dim_product", product_records, self.database)
        
        console.print("✓ Loaded normalized product dimensions")
        return {"brands": brands, "categories_l1": categories_l1, "categories_l2": categories_l2, "categories_l3": categories_l3}
    
    def load_normalized_customer_dimensions(self, customers: List[Dict[str, Any]], geography_map: Dict[str, Any]):
        """Load normalized customer dimensions."""
        console.print("Loading normalized customer dimensions...")
        
        # Load customer segment dimension
        segments = {}
        segment_records = []
        segments_data = [
            {"code": "PREM", "name": "Premium", "description": "High-value customers with premium needs"},
            {"code": "GOLD", "name": "Gold", "description": "Loyal customers with good spending patterns"},
            {"code": "SILV", "name": "Silver", "description": "Regular customers with moderate spending"},
            {"code": "BRON", "name": "Bronze", "description": "Entry-level customers"},
            {"code": "STAN", "name": "Standard", "description": "Standard customer segment"}
        ]
        
        for i, segment in enumerate(segments_data):
            segments[segment["name"]] = i + 1
            segment_record = {
                "segment_key": i + 1,
                "segment_code": segment["code"],
                "segment_name": segment["name"],
                "segment_description": segment["description"]
            }
            segment_records.append(segment_record)
        
        self.db.execute_insert("dim_customer_segment", segment_records, self.database)
        
        # Load loyalty status dimension
        loyalty_statuses = {}
        loyalty_records = []
        loyalty_data = [
            {"code": "PLAT", "name": "Platinum", "min_points": 10000, "discount_rate": 15.0},
            {"code": "GOLD", "name": "Gold", "min_points": 5000, "discount_rate": 10.0},
            {"code": "SILV", "name": "Silver", "min_points": 2000, "discount_rate": 5.0},
            {"code": "BRON", "name": "Bronze", "min_points": 0, "discount_rate": 2.0}
        ]
        
        for i, loyalty in enumerate(loyalty_data):
            loyalty_statuses[loyalty["name"]] = i + 1
            loyalty_record = {
                "loyalty_key": i + 1,
                "loyalty_code": loyalty["code"],
                "loyalty_name": loyalty["name"],
                "min_points": loyalty["min_points"],
                "discount_rate": float(loyalty["discount_rate"])
            }
            loyalty_records.append(loyalty_record)
        
        self.db.execute_insert("dim_loyalty_status", loyalty_records, self.database)
        
        # Load customer dimension
        customer_records = []
        for i, customer in enumerate(customers):
            city_id = f"{customer['country']}_{customer['state']}_{customer['city']}"
            city_key = geography_map["cities"].get(city_id, 1)
            
            segment = customer.get("customer_segment", "Standard")
            loyalty = customer.get("loyalty_status", "Bronze")
            
            customer_record = {
                "customer_key": i + 1,
                "city_key": city_key,
                "segment_key": segments.get(segment, 5),
                "loyalty_key": loyalty_statuses.get(loyalty, 4),
                "customer_id": customer["customer_id"],
                "first_name": customer["first_name"],
                "last_name": customer["last_name"],
                "full_name": f"{customer['first_name']} {customer['last_name']}",
                "email": customer["email"],
                "phone": customer["phone"],
                "birth_date": customer.get("birth_date"),
                "gender": customer.get("gender", "Unknown"),
                "address": customer["address"],
                "registration_date": customer.get("registration_date"),
                "credit_rating": customer.get("credit_rating", "Good"),
                "is_active": customer.get("is_active", True)
            }
            customer_records.append(customer_record)
        
        self.db.execute_insert("dim_customer", customer_records, self.database)
        
        console.print("✓ Loaded normalized customer dimensions")
        return {"segments": segments, "loyalty_statuses": loyalty_statuses}
    
    def load_normalized_supplier_dimensions(self, suppliers: List[Dict[str, Any]], geography_map: Dict[str, Any]):
        """Load normalized supplier dimensions."""
        console.print("Loading normalized supplier dimensions...")
        
        # Load supplier rating dimension
        ratings = {}
        rating_records = []
        rating_data = [
            {"code": "EXCL", "name": "Excellent", "min_score": 4.5, "max_score": 5.0},
            {"code": "GOOD", "name": "Good", "min_score": 3.5, "max_score": 4.49},
            {"code": "FAIR", "name": "Fair", "min_score": 2.5, "max_score": 3.49},
            {"code": "POOR", "name": "Poor", "min_score": 1.0, "max_score": 2.49}
        ]
        
        for i, rating in enumerate(rating_data):
            ratings[rating["name"]] = i + 1
            rating_record = {
                "rating_key": i + 1,
                "rating_code": rating["code"],
                "rating_name": rating["name"],
                "min_score": float(rating["min_score"]),
                "max_score": float(rating["max_score"])
            }
            rating_records.append(rating_record)
        
        self.db.execute_insert("dim_supplier_rating", rating_records, self.database)
        
        # Load supplier dimension
        supplier_records = []
        for i, supplier in enumerate(suppliers):
            # Find city key for supplier location
            city_id = f"{supplier['country']}_{supplier.get('state', 'Unknown')}_{supplier['city']}"
            city_key = geography_map["cities"].get(city_id, 1)
            
            # Determine rating category
            rating_value = float(supplier["rating"])
            if rating_value >= 4.5:
                rating_key = 1  # Excellent
            elif rating_value >= 3.5:
                rating_key = 2  # Good
            elif rating_value >= 2.5:
                rating_key = 3  # Fair
            else:
                rating_key = 4  # Poor
            
            supplier_record = {
                "supplier_key": i + 1,
                "city_key": city_key,
                "rating_key": rating_key,
                "supplier_id": supplier["supplier_id"],
                "supplier_name": supplier["supplier_name"],
                "contact_person": supplier["contact_person"],
                "email": supplier["email"],
                "phone": supplier["phone"],
                "address": supplier["address"],
                "contract_start_date": supplier.get("contract_start_date"),
                "contract_end_date": supplier.get("contract_end_date"),
                "is_active": supplier.get("is_active", True)
            }
            supplier_records.append(supplier_record)
        
        self.db.execute_insert("dim_supplier", supplier_records, self.database)
        
        console.print("✓ Loaded normalized supplier dimensions")
    
    def load_normalized_channel_and_promotion_dimensions(self):
        """Load normalized channel and promotion dimensions."""
        console.print("Loading normalized channel and promotion dimensions...")
        
        # Load channel type dimension
        channel_types = {}
        channel_type_records = []
        channel_type_data = [
            {"code": "DIG", "name": "Digital", "commission_base_rate": 2.0},
            {"code": "PHY", "name": "Physical", "commission_base_rate": 5.0},
            {"code": "CALL", "name": "Call Center", "commission_base_rate": 7.0},
            {"code": "EXT", "name": "External", "commission_base_rate": 10.0}
        ]
        
        for i, channel_type in enumerate(channel_type_data):
            channel_types[channel_type["name"]] = i + 1
            channel_type_record = {
                "channel_type_key": i + 1,
                "channel_type_code": channel_type["code"],
                "channel_type_name": channel_type["name"],
                "commission_base_rate": float(channel_type["commission_base_rate"])
            }
            channel_type_records.append(channel_type_record)
        
        self.db.execute_insert("dim_channel_type", channel_type_records, self.database)
        
        # Load sales channel dimension
        channels = [
            {"id": "ONL", "name": "Online", "type": "Digital", "manager": "Alice Johnson", "commission": 2.5},
            {"id": "RET", "name": "Retail Store", "type": "Physical", "manager": "Bob Smith", "commission": 5.0},
            {"id": "MOB", "name": "Mobile App", "type": "Digital", "manager": "Carol Brown", "commission": 2.0},
            {"id": "PHN", "name": "Phone", "type": "Call Center", "manager": "David Wilson", "commission": 7.5},
            {"id": "PAR", "name": "Partner", "type": "External", "manager": "Eva Davis", "commission": 10.0}
        ]
        
        channel_records = []
        for i, channel in enumerate(channels):
            channel_record = {
                "channel_key": i + 1,
                "channel_type_key": channel_types[channel["type"]],
                "channel_id": channel["id"],
                "channel_name": channel["name"],
                "manager_name": channel["manager"],
                "commission_rate": float(channel["commission"]),
                "is_active": True
            }
            channel_records.append(channel_record)
        
        self.db.execute_insert("dim_sales_channel", channel_records, self.database)
        
        # Load promotion type dimension
        promotion_types = {}
        promotion_type_records = []
        promotion_type_data = [
            {"code": "NONE", "name": "No Promotion", "default_discount": 0.0},
            {"code": "PCT", "name": "Percentage", "default_discount": 10.0},
            {"code": "FIX", "name": "Fixed Amount", "default_discount": 50.0},
            {"code": "SPEC", "name": "Special", "default_discount": 25.0}
        ]
        
        for i, promo_type in enumerate(promotion_type_data):
            promotion_types[promo_type["name"]] = i + 1
            promo_type_record = {
                "promotion_type_key": i + 1,
                "promotion_type_code": promo_type["code"],
                "promotion_type_name": promo_type["name"],
                "default_discount_percent": float(promo_type["default_discount"])
            }
            promotion_type_records.append(promo_type_record)
        
        self.db.execute_insert("dim_promotion_type", promotion_type_records, self.database)
        
        # Load promotion dimension
        promotions = [
            {"id": "NONE", "name": "No Promotion", "type": "No Promotion", "discount_type": "None", "value": 0.0},
            {"id": "SAVE10", "name": "Save 10%", "type": "Percentage", "discount_type": "Percentage", "value": 10.0},
            {"id": "SAVE20", "name": "Save 20%", "type": "Percentage", "discount_type": "Percentage", "value": 20.0},
            {"id": "FLAT50", "name": "Flat $50 Off", "type": "Fixed Amount", "discount_type": "Fixed", "value": 50.0},
            {"id": "BOGO", "name": "Buy One Get One", "type": "Special", "discount_type": "Special", "value": 50.0}
        ]
        
        promotion_records = []
        for i, promotion in enumerate(promotions):
            promotion_record = {
                "promotion_key": i + 1,
                "promotion_type_key": promotion_types[promotion["type"]],
                "promotion_id": promotion["id"],
                "promotion_name": promotion["name"],
                "discount_type": promotion["discount_type"],
                "discount_value": float(promotion["value"]),
                "start_date": date(2022, 1, 1),
                "end_date": date(2025, 12, 31),
                "is_active": True
            }
            promotion_records.append(promotion_record)
        
        self.db.execute_insert("dim_promotion", promotion_records, self.database)
        
        console.print("✓ Loaded normalized channel and promotion dimensions")
    
    def load_fact_sales(self, customers: List[Dict[str, Any]], products: List[Dict[str, Any]], 
                       orders: List[Dict[str, Any]], order_lines: List[Dict[str, Any]], 
                       geography_map: Dict[str, Any]):
        """Load fact table for snowflake schema."""
        console.print("Loading snowflake fact sales table...")
        
        # Create lookups
        customer_lookup = {customers[i]["customer_id"]: i + 1 for i in range(len(customers))}
        product_lookup = {products[i]["product_id"]: i + 1 for i in range(len(products))}
        order_lookup = {o["order_id"]: o for o in orders}
        
        # Channel and promotion mappings
        channel_map = {"Online": 1, "Retail Store": 2, "Mobile App": 3, "Phone": 4, "Partner": 5}
        
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
            
            # Get customer for city lookup
            customer = next((c for c in customers if c["customer_id"] == order["customer_id"]), None)
            if not customer:
                continue
            
            # City keys for normalized geography
            city_id = f"{customer['country']}_{customer['state']}_{customer['city']}"
            shipping_city_key = geography_map["cities"].get(city_id, 1)
            billing_city_key = shipping_city_key  # Same for demo
            
            # Random supplier assignment
            import random
            supplier_key = random.randint(1, min(100, len(products)))
            
            # Other dimension keys
            channel_key = channel_map.get(order.get("sales_channel", "Online"), 1)
            promotion_key = 1  # Default to no promotion
            
            if order.get("promotion_code"):
                if "10" in order["promotion_code"]:
                    promotion_key = 2
                elif "20" in order["promotion_code"]:
                    promotion_key = 3
                else:
                    promotion_key = 4
            
            # Convert order date to date key
            order_date = order["order_date"]
            if isinstance(order_date, str):
                order_datetime = datetime.fromisoformat(order_date.replace('Z', '+00:00'))
            else:
                order_datetime = order_date
            
            date_key = int(order_datetime.strftime("%Y%m%d"))
            
            # Calculate metrics
            profit_amount = float(line["line_total"]) - (float(line.get("cost_amount", line["unit_price"])) if "cost_amount" in line else float(line["unit_price"]) * 0.6)
            profit_margin = (profit_amount / float(line["line_total"])) * 100 if float(line["line_total"]) > 0 else 0
            
            fact_record = {
                "sales_key": sales_key,
                "date_key": date_key,
                "customer_key": customer_key,
                "product_key": product_key,
                "supplier_key": supplier_key,
                "shipping_city_key": shipping_city_key,
                "billing_city_key": billing_city_key,
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
        
        console.print(f"✓ Loaded {sales_key - 1} snowflake fact sales records")
    
    def _get_days_in_month(self, year: int, month: int) -> int:
        """Get number of days in a month."""
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        elif month == 2:
            return 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28
        return 30
    
    def _get_day_of_year(self, date_obj) -> int:
        """Get day of year."""
        if isinstance(date_obj, str):
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00')).date()
        elif isinstance(date_obj, datetime):
            date_obj = date_obj.date()
        return date_obj.timetuple().tm_yday
    
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
    
    def _get_currency(self, country: str) -> str:
        """Get currency based on country."""
        currency_map = {
            "USA": "USD", "Canada": "CAD", "Mexico": "MXN",
            "UK": "GBP", "Germany": "EUR", "France": "EUR",
            "China": "CNY", "Japan": "JPY", "India": "INR"
        }
        return currency_map.get(country, "USD")
    
    def _get_state_population(self) -> int:
        """Get random state population."""
        import random
        return random.randint(500000, 40000000)
    
    def _get_city_population(self) -> int:
        """Get random city population."""
        import random
        return random.randint(10000, 1000000)
    
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
    
    def _count_order_lines(self, order_id: str, order_lines: List[Dict[str, Any]]) -> int:
        """Count number of lines in an order."""
        return len([line for line in order_lines if line["order_id"] == order_id])
    
    def load_data(self):
        """Load all data into snowflake schema."""
        console.print("[bold blue]Loading Snowflake Schema...[/bold blue]")
        
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
        
        # Load normalized dimensions
        time_map = self.load_normalized_time_dimensions(time_data)
        geography_map = self.load_normalized_geography_dimensions(customers)
        product_map = self.load_normalized_product_dimensions(products)
        customer_map = self.load_normalized_customer_dimensions(customers, geography_map)
        self.load_normalized_supplier_dimensions(suppliers, geography_map)
        self.load_normalized_channel_and_promotion_dimensions()
        
        # Load fact table
        self.load_fact_sales(customers, products, orders, order_lines, geography_map)
        
        console.print("[bold green]✓ Snowflake Schema loading completed![/bold green]")
    
    def get_hierarchical_sales_report(self) -> List[Any]:
        """Get sales report with hierarchical drill-down capability."""
        query = f"""
        SELECT 
            dc1.category_l1_name,
            dc2.category_l2_name,
            dc3.category_l3_name,
            db.brand_name,
            dp.product_name,
            sum(fs.line_total) as total_sales,
            sum(fs.quantity) as total_quantity,
            count() as transaction_count
        FROM {self.database}.fact_sales fs
        LEFT JOIN {self.database}.dim_product dp ON fs.product_key = dp.product_key
        LEFT JOIN {self.database}.dim_category_l3 dc3 ON dp.category_l3_key = dc3.category_l3_key
        LEFT JOIN {self.database}.dim_category_l2 dc2 ON dc3.category_l2_key = dc2.category_l2_key
        LEFT JOIN {self.database}.dim_category_l1 dc1 ON dc2.category_l1_key = dc1.category_l1_key
        LEFT JOIN {self.database}.dim_brand db ON dp.brand_key = db.brand_key
        GROUP BY dc1.category_l1_name, dc2.category_l2_name, dc3.category_l3_name, db.brand_name, dp.product_name
        ORDER BY total_sales DESC
        LIMIT 20
        """
        
        result = self.db.execute_query(query)
        return result.result_rows
