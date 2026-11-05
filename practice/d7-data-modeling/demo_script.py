#!/usr/bin/env python3
"""
Complete demo script showing all data modeling techniques
"""
import sys
import os
sys.path.append('/app')
sys.path.append('/app/src')

from generators.data_generator import DataGenerator
from utils.database import ClickHouseManager
from models.data_vault_1 import DataVault1Manager
from models.data_vault_2 import DataVault2Manager
from models.scd import SCDManager
from models.big_fact import BigFactManager
from models.star_schema import StarSchemaManager
from models.snowflake_schema import SnowflakeSchemaManager

def run_complete_demo():
    """Run a complete demonstration of all data modeling techniques"""
    
    print("🚀 Starting Complete Data Modeling Demonstration")
    print("=" * 60)
    
    # Step 1: Generate sample data
    print("\n📊 Step 1: Generating Sample Data")
    generator = DataGenerator()
    data = generator.generate_sample_data(1000)  # Generate 1000 scale
    print("✅ Sample data generated successfully")
    
    # Step 2: Test database connection
    print("\n🔌 Step 2: Testing Database Connection")
    db_manager = ClickHouseManager()
    if not db_manager.test_connection():
        print("❌ Database connection failed")
        return False
    print("✅ Database connection successful")
    
    # Step 3: Load data into each modeling technique
    print("\n📈 Step 3: Loading Data into All Modeling Techniques")
    
    managers = {
        "Data Vault 1.0": DataVault1Manager(db_manager),
        "Data Vault 2.0": DataVault2Manager(db_manager),
        "SCD (Slowly Changing Dimensions)": SCDManager(db_manager),
        "Big Fact Table": BigFactManager(db_manager),
        "Star Schema": StarSchemaManager(db_manager),
        "Snowflake Schema": SnowflakeSchemaManager(db_manager)
    }
    
    for name, manager in managers.items():
        print(f"\n  Loading data into {name}...")
        try:
            if hasattr(manager, 'load_customers'):
                manager.load_customers(data['customers'])
            if hasattr(manager, 'load_products'):
                manager.load_products(data['products'])
            if hasattr(manager, 'load_suppliers'):
                manager.load_suppliers(data['suppliers'])
            if hasattr(manager, 'load_orders'):
                manager.load_orders(data['orders'])
            if hasattr(manager, 'load_order_lines'):
                manager.load_order_lines(data['order_lines'])
            if hasattr(manager, 'load_time_dimension'):
                manager.load_time_dimension(data['time_dimension'])
            print(f"  ✅ {name} data loading completed")
        except Exception as e:
            print(f"  ❌ {name} data loading failed: {str(e)}")
    
    # Step 4: Run sample queries
    print("\n🔍 Step 4: Running Sample Queries")
    
    # Example query for each technique
    queries = {
        "Data Vault 1.0": """
            SELECT h.customer_id, s.first_name, s.last_name 
            FROM data_vault_1.hub_customer h
            JOIN data_vault_1.sat_customer s ON h.customer_hk = s.customer_hk
            WHERE s.load_end_date IS NULL
            LIMIT 5
        """,
        "Star Schema": """
            SELECT 
                c.first_name,
                c.last_name,
                p.product_name,
                f.quantity,
                f.unit_price
            FROM star_schema.fact_sales f
            JOIN star_schema.dim_customer c ON f.customer_key = c.customer_key
            JOIN star_schema.dim_product p ON f.product_key = p.product_key
            LIMIT 5
        """,
        "Big Fact Table": """
            SELECT 
                customer_first_name,
                customer_last_name,
                product_name,
                quantity,
                unit_price
            FROM big_fact.big_fact_sales
            ORDER BY unit_price DESC
            LIMIT 5
        """
    }
    
    for technique, query in queries.items():
        try:
            result = db_manager.client.query(query)
            print(f"\n  📋 {technique} Sample Query Results:")
            rows = result.result_rows
            if rows:
                for i, row in enumerate(rows[:3]):  # Show first 3 rows
                    print(f"    Row {i+1}: {row}")
            else:
                print("    No results returned")
        except Exception as e:
            print(f"    ❌ Query failed: {str(e)}")
    
    print("\n🎉 Complete demonstration finished!")
    print("=" * 60)
    print("\n📝 Summary:")
    print("- Generated sample e-commerce data")
    print("- Loaded data into 6 different modeling techniques")
    print("- Demonstrated queries across multiple schemas")
    print("\n🔗 Access Points:")
    print("- Jupyter Lab (with our notebook): http://localhost:8890")
    print("- Jupyter DataScience Notebook: http://localhost:8889")
    print("- ClickHouse HTTP Interface: http://localhost:8123")
    print("\n💡 Next Steps:")
    print("- Open the Jupyter notebook for detailed analysis")
    print("- Run performance comparisons")
    print("- Explore the different modeling approaches")

if __name__ == "__main__":
    run_complete_demo()
