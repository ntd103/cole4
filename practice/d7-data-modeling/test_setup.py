#!/usr/bin/env python3
"""
Test script to validate the data modeling project setup
"""

import sys
import os
sys.path.append('/app/src')

def test_imports():
    """Test that all modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test data generator
        from src.generators.data_generator import DataGenerator
        print("✅ DataGenerator import successful")
        
        # Test database utilities
        from src.utils.database import ClickHouseManager
        print("✅ ClickHouseManager import successful")
        
        # Test all modeling techniques
        from src.models.data_vault_1 import DataVault1Manager
        from src.models.data_vault_2 import DataVault2Manager
        from src.models.scd import SCDManager
        from src.models.big_fact import BigFactManager
        from src.models.star_schema import StarSchemaManager
        from src.models.snowflake_schema import SnowflakeSchemaManager
        print("✅ All modeling managers import successful")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_connection():
    """Test ClickHouse connection"""
    try:
        from src.utils.database import ClickHouseManager
        
        manager = ClickHouseManager()
        if manager.test_connection():
            print("✅ ClickHouse connection successful")
            return True
        else:
            print("❌ ClickHouse connection failed")
            return False
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Data Modeling Project Setup Test ===")
    
    # Test imports
    imports_ok = test_imports()
    
    # Test database connection
    connection_ok = test_connection()
    
    if imports_ok and connection_ok:
        print("\n🎉 All tests passed! The project setup is ready.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Check the setup.")
        sys.exit(1)
