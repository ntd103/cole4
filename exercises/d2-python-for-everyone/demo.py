# Python Introduction - Interactive Demo
# This notebook demonstrates Python's key features and capabilities for data engineering

# Cell 1: Python Basics - Dynamic Typing and Data Structures
print("=== Python Basics Demo ===")

# Dynamic typing demonstration
variable = "I'm a string"
print(f"Variable type: {type(variable)}, Value: {variable}")

variable = 42
print(f"Variable type: {type(variable)}, Value: {variable}")

variable = [1, 2, 3, "mixed", True]
print(f"Variable type: {type(variable)}, Value: {variable}")

# Dictionary demonstration
person = {
    "name": "John Doe",
    "age": 30,
    "skills": ["Python", "SQL", "Data Engineering"],
    "is_employed": True
}
print(f"\nPerson data: {person}")
print(f"Skills: {person['skills']}")

# Cell 2: List Comprehensions and Functional Programming
print("\n=== Python's Expressive Syntax ===")

# List comprehension
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_squares = [x**2 for x in numbers if x % 2 == 0]
print(f"Even squares: {even_squares}")

# Dictionary comprehension
word_lengths = {word: len(word) for word in ["python", "data", "engineering", "rocks"]}
print(f"Word lengths: {word_lengths}")

# Lambda functions and map/filter
squared = list(map(lambda x: x**2, numbers[:5]))
print(f"Squared numbers: {squared}")

filtered = list(filter(lambda x: x > 5, numbers))
print(f"Numbers > 5: {filtered}")

# Cell 3: Error Handling and Context Managers
print("\n=== Error Handling & Resource Management ===")

# Exception handling
def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        return None
    except TypeError:
        print("Invalid input types!")
        return None
    finally:
        print(f"Division operation attempted: {a} / {b}")

print("Safe division examples:")
print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("10", 2))

# Context manager simulation (file-like operations)
class SimpleResource:
    def __init__(self, name):
        self.name = name
    
    def __enter__(self):
        print(f"Opening resource: {self.name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing resource: {self.name}")
    
    def process(self):
        return f"Processing data from {self.name}"

# Using context manager
with SimpleResource("database_connection") as resource:
    result = resource.process()
    print(result)

# Cell 4: Object-Oriented Programming
print("\n=== Object-Oriented Programming ===")

class DataProcessor:
    def __init__(self, name):
        self.name = name
        self.processed_count = 0
    
    def process_batch(self, data_batch):
        """Process a batch of data"""
        self.processed_count += len(data_batch)
        return [item.upper() if isinstance(item, str) else item * 2 for item in data_batch]
    
    def get_stats(self):
        return f"{self.name} has processed {self.processed_count} items"
    
    def __repr__(self):
        return f"DataProcessor('{self.name}')"

# Create and use the processor
processor = DataProcessor("ETL_Pipeline")
print(f"Created: {processor}")

# Process some data
batch1 = ["hello", "world", 42]
batch2 = ["python", "rocks", 100]

result1 = processor.process_batch(batch1)
result2 = processor.process_batch(batch2)

print(f"Batch 1 result: {result1}")
print(f"Batch 2 result: {result2}")
print(processor.get_stats())

# Cell 5: Working with Data - Pandas-style operations (without pandas)
print("\n=== Data Manipulation (Native Python) ===")

# Simulate working with structured data
employees = [
    {"name": "Alice", "department": "Engineering", "salary": 90000, "years": 3},
    {"name": "Bob", "department": "Marketing", "salary": 70000, "years": 5},
    {"name": "Charlie", "department": "Engineering", "salary": 95000, "years": 7},
    {"name": "Diana", "department": "Sales", "salary": 80000, "years": 2},
    {"name": "Eve", "department": "Engineering", "salary": 85000, "years": 4}
]

print("Original data:")
for emp in employees:
    print(f"  {emp}")

# Filter engineers
engineers = [emp for emp in employees if emp["department"] == "Engineering"]
print(f"\nEngineers: {len(engineers)} found")

# Calculate average salary for engineers
avg_salary = sum(emp["salary"] for emp in engineers) / len(engineers)
print(f"Average engineer salary: ${avg_salary:,.2f}")

# Group by department
from collections import defaultdict
dept_groups = defaultdict(list)
for emp in employees:
    dept_groups[emp["department"]].append(emp)

print("\nGrouped by department:")
for dept, emp_list in dept_groups.items():
    avg_sal = sum(emp["salary"] for emp in emp_list) / len(emp_list)
    print(f"  {dept}: {len(emp_list)} employees, avg salary: ${avg_sal:,.2f}")

# Cell 6: File I/O and Data Processing
print("\n=== File Processing & Data Pipeline ===")

import json
from datetime import datetime

# Create sample data
sample_data = {
    "timestamp": datetime.now().isoformat(),
    "events": [
        {"user_id": 1001, "action": "login", "timestamp": "2024-01-15T10:30:00"},
        {"user_id": 1002, "action": "purchase", "timestamp": "2024-01-15T10:35:00", "amount": 99.99},
        {"user_id": 1001, "action": "logout", "timestamp": "2024-01-15T11:00:00"},
        {"user_id": 1003, "action": "login", "timestamp": "2024-01-15T11:15:00"},
        {"user_id": 1002, "action": "view_product", "timestamp": "2024-01-15T11:20:00"}
    ],
    "metadata": {
        "source": "web_app",
        "version": "1.0"
    }
}

# Simulate writing to file (in memory for demo)
json_data = json.dumps(sample_data, indent=2)
print("Sample JSON data structure:")
print(json_data[:200] + "...")

# Process the data
events = sample_data["events"]
print(f"\nProcessing {len(events)} events...")

# Analyze events
user_actions = defaultdict(list)
for event in events:
    user_actions[event["user_id"]].append(event["action"])

print("User activity summary:")
for user_id, actions in user_actions.items():
    print(f"  User {user_id}: {', '.join(actions)}")

# Calculate some metrics
total_purchases = len([e for e in events if e["action"] == "purchase"])
total_revenue = sum(e.get("amount", 0) for e in events if e["action"] == "purchase")
print(f"\nMetrics:")
print(f"  Total purchases: {total_purchases}")
print(f"  Total revenue: ${total_revenue:.2f}")

# Cell 7: API Simulation and Data Validation
print("\n=== API Integration & Data Validation ===")

import re
from typing import Dict, List, Optional

class DataValidator:
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        # Simple phone validation
        cleaned = re.sub(r'[^\d]', '', phone)
        return len(cleaned) >= 10
    
    @staticmethod
    def validate_user_data(user_data: Dict) -> Dict:
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ["name", "email", "age"]
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                errors.append(f"Missing required field: {field}")
        
        # Email validation
        if "email" in user_data and user_data["email"]:
            if not DataValidator.validate_email(user_data["email"]):
                errors.append("Invalid email format")
        
        # Age validation
        if "age" in user_data:
            try:
                age = int(user_data["age"])
                if age < 0 or age > 150:
                    warnings.append("Age seems unrealistic")
            except (ValueError, TypeError):
                errors.append("Age must be a number")
        
        # Phone validation
        if "phone" in user_data and user_data["phone"]:
            if not DataValidator.validate_phone(user_data["phone"]):
                warnings.append("Phone number format may be invalid")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

# Simulate API data processing
api_responses = [
    {"name": "John Doe", "email": "john@example.com", "age": 30, "phone": "555-1234"},
    {"name": "Jane Smith", "email": "invalid-email", "age": 25},
    {"name": "", "email": "bob@test.com", "age": "thirty"},
    {"name": "Alice Johnson", "email": "alice@company.co.uk", "age": 28, "phone": "+1-555-987-6543"}
]

print("Processing API responses:")
valid_users = []
invalid_users = []

for i, user_data in enumerate(api_responses):
    validation = DataValidator.validate_user_data(user_data)
    print(f"\nUser {i+1}: {user_data.get('name', 'Unknown')}")
    
    if validation["valid"]:
        print("  ✓ Valid")
        valid_users.append(user_data)
    else:
        print("  ✗ Invalid")
        invalid_users.append(user_data)
    
    for error in validation["errors"]:
        print(f"    Error: {error}")
    
    for warning in validation["warnings"]:
        print(f"    Warning: {warning}")

print(f"\nSummary: {len(valid_users)} valid, {len(invalid_users)} invalid users")

# Cell 8: Performance Comparison and Optimization
print("\n=== Performance Demonstration ===")

import time
from functools import wraps

def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@timer_decorator
def process_with_loops(data):
    """Process data using traditional loops"""
    result = []
    for item in data:
        if item % 2 == 0:
            result.append(item ** 2)
    return result

@timer_decorator
def process_with_comprehension(data):
    """Process data using list comprehension"""
    return [item ** 2 for item in data if item % 2 == 0]

@timer_decorator
def process_with_filter_map(data):
    """Process data using filter and map"""
    return list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, data)))

# Test with different data sizes
test_data = list(range(10000))
print(f"Processing {len(test_data)} numbers:")

result1 = process_with_loops(test_data)
result2 = process_with_comprehension(test_data)
result3 = process_with_filter_map(test_data)

# Verify results are the same
print(f"All methods produce same result: {result1 == result2 == result3}")
print(f"Result length: {len(result1)}")

# Cell 9: Async Programming Demo (Simulated)
print("\n=== Asynchronous Programming Concepts ===")

import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading

def simulate_io_task(task_id, duration):
    """Simulate an I/O bound task"""
    print(f"  Task {task_id} started (thread: {threading.current_thread().name})")
    time.sleep(duration)  # Simulate I/O wait
    result = f"Task {task_id} completed after {duration}s"
    print(f"  Task {task_id} finished")
    return result

# Synchronous approach
print("Synchronous execution:")
start_time = time.time()
sync_results = []
for i in range(3):
    result = simulate_io_task(i+1, 1.0)
    sync_results.append(result)
sync_time = time.time() - start_time
print(f"Synchronous total time: {sync_time:.2f}s\n")

# Multithreading approach
print("Multithreaded execution:")
start_time = time.time()
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(simulate_io_task, i+1, 1.0) for i in range(3)]
    thread_results = [future.result() for future in futures]
thread_time = time.time() - start_time
print(f"Multithreaded total time: {thread_time:.2f}s")
print(f"Speed improvement: {sync_time/thread_time:.1f}x faster\n")

# Cell 10: Data Engineering Pipeline Simulation
print("\n=== Data Engineering Pipeline Demo ===")

class DataPipeline:
    def __init__(self, name):
        self.name = name
        self.steps = []
        self.metrics = {"processed": 0, "errors": 0, "warnings": 0}
    
    def add_step(self, step_func, step_name):
        self.steps.append((step_func, step_name))
        return self
    
    def execute(self, data):
        print(f"Executing pipeline: {self.name}")
        current_data = data
        
        for i, (step_func, step_name) in enumerate(self.steps, 1):
            print(f"  Step {i}: {step_name}")
            try:
                current_data = step_func(current_data)
                print(f"    ✓ Processed {len(current_data) if hasattr(current_data, '__len__') else 'N/A'} items")
            except Exception as e:
                print(f"    ✗ Error: {e}")
                self.metrics["errors"] += 1
                raise
        
        self.metrics["processed"] += len(current_data) if hasattr(current_data, '__len__') else 1
        return current_data

# Define pipeline steps
def extract_step(data):
    """Simulate data extraction"""
    # In real scenario: fetch from database, API, files
    extracted_data = [
        {"id": 1, "name": "Product A", "price": "29.99", "category": "electronics"},
        {"id": 2, "name": "Product B", "price": "invalid", "category": "books"},
        {"id": 3, "name": "Product C", "price": "15.50", "category": "clothing"},
        {"id": 4, "name": "", "price": "99.99", "category": "electronics"}
    ]
    return extracted_data

def transform_step(data):
    """Transform and clean data"""
    transformed = []
    for item in data:
        # Data cleaning and transformation
        try:
            # Clean price
            if item["price"] != "invalid":
                price = float(item["price"])
            else:
                price = 0.0  # Default for invalid prices
            
            # Clean name
            name = item["name"].strip()
            if not name:
                name = f"Unknown Product {item['id']}"
            
            transformed_item = {
                "id": item["id"],
                "name": name,
                "price": price,
                "category": item["category"].lower(),
                "processed_at": datetime.now().isoformat()
            }
            transformed.append(transformed_item)
        except Exception as e:
            print(f"    Warning: Error processing item {item['id']}: {e}")
    
    return transformed

def validate_step(data):
    """Validate transformed data"""
    validated = []
    for item in data:
        # Business rules validation
        is_valid = True
        if item["price"] < 0:
            print(f"    Warning: Negative price for item {item['id']}")
            is_valid = False
        
        if len(item["name"]) < 3:
            print(f"    Warning: Name too short for item {item['id']}")
        
        if is_valid:
            validated.append(item)
    
    return validated

def load_step(data):
    """Simulate loading data to destination"""
    # In real scenario: insert to database, write to file, send to API
    print(f"    Loading {len(data)} validated records to destination")
    return {"loaded_count": len(data), "data": data}

# Create and execute pipeline
pipeline = (DataPipeline("Product Data Pipeline")
           .add_step(extract_step, "Extract from source")
           .add_step(transform_step, "Transform and clean")
           .add_step(validate_step, "Validate business rules")
           .add_step(load_step, "Load to destination"))

try:
    result = pipeline.execute([])
    print(f"\nPipeline completed successfully!")
    print(f"Loaded {result['loaded_count']} records")
    print(f"Sample record: {result['data'][0] if result['data'] else 'No data'}")
except Exception as e:
    print(f"Pipeline failed: {e}")

print(f"\nPipeline metrics: {pipeline.metrics}")

# Cell 11: Configuration and Environment Management
print("\n=== Configuration Management ===")

import os

class Config:
    """Configuration management class"""
    
    def __init__(self):
        self.settings = {
            # Database settings
            "DATABASE_URL": os.getenv("DATABASE_URL", "postgresql://localhost:5432/mydb"),
            "DATABASE_POOL_SIZE": int(os.getenv("DATABASE_POOL_SIZE", "10")),
            
            # API settings
            "API_BASE_URL": os.getenv("API_BASE_URL", "https://api.example.com"),
            "API_TIMEOUT": int(os.getenv("API_TIMEOUT", "30")),
            "API_RATE_LIMIT": int(os.getenv("API_RATE_LIMIT", "100")),
            
            # Processing settings
            "BATCH_SIZE": int(os.getenv("BATCH_SIZE", "1000")),
            "MAX_RETRIES": int(os.getenv("MAX_RETRIES", "3")),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
            
            # Feature flags
            "ENABLE_CACHING": os.getenv("ENABLE_CACHING", "true").lower() == "true",
            "ENABLE_MONITORING": os.getenv("ENABLE_MONITORING", "true").lower() == "true"
        }
    
    def get(self, key, default=None):
        return self.settings.get(key, default)
    
    def display_config(self):
        print("Current configuration:")
        for key, value in self.settings.items():
            # Mask sensitive information
            if "PASSWORD" in key or "SECRET" in key or "TOKEN" in key:
                display_value = "*" * len(str(value))
            else:
                display_value = value
            print(f"  {key}: {display_value}")

# Create configuration instance
config = Config()
config.display_config()

print(f"\nUsing configuration in application:")
print(f"Database URL: {config.get('DATABASE_URL')}")
print(f"Batch size: {config.get('BATCH_SIZE')}")
print(f"Caching enabled: {config.get('ENABLE_CACHING')}")

# Cell 12: Logging and Monitoring
print("\n=== Logging and Monitoring ===")

import logging
from datetime import datetime

class SimpleLogger:
    def __init__(self, name):
        self.name = name
        self.logs = []
    
    def _log(self, level, message):
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {level} - {self.name}: {message}"
        self.logs.append(log_entry)
        print(log_entry)
    
    def info(self, message):
        self._log("INFO", message)
    
    def warning(self, message):
        self._log("WARNING", message)
    
    def error(self, message):
        self._log("ERROR", message)
    
    def get_logs(self):
        return self.logs

class MetricsCollector:
    def __init__(self):
        self.metrics = {}
    
    def increment(self, metric_name, value=1):
        self.metrics[metric_name] = self.metrics.get(metric_name, 0) + value
    
    def set_gauge(self, metric_name, value):
        self.metrics[metric_name] = value
    
    def get_metrics(self):
        return self.metrics.copy()

# Demonstrate logging and metrics
logger = SimpleLogger("DataProcessor")
metrics = MetricsCollector()

# Simulate processing with logging and metrics
logger.info("Starting data processing job")
metrics.increment("jobs_started")

try:
    # Simulate some work
    data_items = ["item1", "item2", "invalid_item", "item4"]
    processed_count = 0
    error_count = 0
    
    for item in data_items:
        if "invalid" in item:
            logger.warning(f"Invalid item detected: {item}")
            metrics.increment("invalid_items")
            error_count += 1
        else:
            logger.info(f"Processed item: {item}")
            processed_count += 1
    
    metrics.set_gauge("items_processed", processed_count)
    metrics.set_gauge("processing_errors", error_count)
    
    logger.info(f"Processing completed. Processed: {processed_count}, Errors: {error_count}")
    metrics.increment("jobs_completed")

except Exception as e:
    logger.error(f"Processing failed: {e}")
    metrics.increment("jobs_failed")

print(f"\nFinal metrics: {metrics.get_metrics()}")

# Cell 13: Testing Demonstration
print("\n=== Testing Framework Demo ===")

class Calculator:
    @staticmethod
    def add(a, b):
        return a + b
    
    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    @staticmethod
    def multiply(a, b):
        return a * b

class SimpleTestRunner:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
    
    def assert_equal(self, actual, expected, test_name):
        self.tests_run += 1
        if actual == expected:
            print(f"✓ {test_name}")
            self.tests_passed += 1
        else:
            print(f"✗ {test_name}: Expected {expected}, got {actual}")
            self.tests_failed += 1
    
    def assert_raises(self, exception_type, func, args, test_name):
        self.tests_run += 1
        try:
            func(*args)
            print(f"✗ {test_name}: Expected {exception_type.__name__} but no exception was raised")
            self.tests_failed += 1
        except exception_type:
            print(f"✓ {test_name}")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ {test_name}: Expected {exception_type.__name__} but got {type(e).__name__}")
            self.tests_failed += 1
    
    def summary(self):
        print(f"\nTest Summary: {self.tests_run} run, {self.tests_passed} passed, {self.tests_failed} failed")

# Run tests
test_runner = SimpleTestRunner()

print("Running Calculator tests:")

# Test addition
test_runner.assert_equal(Calculator.add(2, 3), 5, "Addition: 2 + 3 = 5")
test_runner.assert_equal(Calculator.add(-1, 1), 0, "Addition: -1 + 1 = 0")

# Test multiplication
test_runner.assert_equal(Calculator.multiply(3, 4), 12, "Multiplication: 3 * 4 = 12")
test_runner.assert_equal(Calculator.multiply(0, 5), 0, "Multiplication: 0 * 5 = 0")

# Test division
test_runner.assert_equal(Calculator.divide(10, 2), 5, "Division: 10 / 2 = 5")
test_runner.assert_raises(ValueError, Calculator.divide, (10, 0), "Division by zero raises ValueError")

test_runner.summary()

# Cell 14: Final Summary and Best Practices
print("\n" + "="*50)
print("PYTHON DEMO SUMMARY")
print("="*50)

print("""
This notebook demonstrated key Python features:

1. 🐍 LANGUAGE FEATURES:
   • Dynamic typing and flexible data structures
   • List/dict comprehensions for expressive code
   • Exception handling and context managers
   • Object-oriented programming capabilities

2. 📊 DATA PROCESSING:
   • Native data manipulation techniques
   • File I/O and JSON processing
   • Data validation and cleaning
   • ETL pipeline implementation

3. ⚡ PERFORMANCE CONSIDERATIONS:
   • Different approaches to data processing
   • Timing and performance measurement
   • Multithreading for I/O-bound tasks
   • Memory-efficient programming patterns

4. 🏗️ ENGINEERING PRACTICES:
   • Configuration management
   • Logging and monitoring
   • Error handling strategies
   • Testing methodologies

5. 🔧 PRACTICAL APPLICATIONS:
   • API data processing simulation
   • Data pipeline orchestration
   • Metrics collection and monitoring
   • Production-ready code patterns

KEY TAKEAWAYS:
✅ Python excels at rapid development and data processing
✅ Rich ecosystem enables complex data engineering tasks
✅ Built-in features support enterprise-grade applications
✅ Performance can be optimized through proper techniques
✅ Extensive testing and monitoring capabilities

NEXT STEPS:
1. Install Python 3.11+ and Jupyter notebooks
2. Explore pandas, numpy, and requests libraries
3. Try building a simple data pipeline
4. Practice with real data sources and APIs
5. Implement proper testing and monitoring
""")

print("="*50)
print("Demo completed successfully! 🎉")
print("="*50)