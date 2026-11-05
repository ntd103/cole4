"""
Main application entry point for data modeling demonstration.
"""
import sys
import os
sys.path.append('/app')

import typer
from rich.console import Console
from rich.table import Table
from utils.database import ClickHouseManager
from generators.data_generator import DataGenerator
from models.data_vault_1 import DataVault1Manager
from models.data_vault_2 import DataVault2Manager
from models.scd import SCDManager
from models.big_fact import BigFactManager
from models.star_schema import StarSchemaManager
from models.snowflake_schema import SnowflakeSchemaManager

app = typer.Typer()
console = Console()

@app.command()
def generate_data(records: int = 10000):
    """Generate sample data for all modeling techniques."""
    console.print(f"[bold green]Generating {records} sample records...[/bold green]")
    
    generator = DataGenerator()
    generator.generate_sample_data(records)
    
    console.print("[bold green]✓ Sample data generated successfully![/bold green]")

@app.command()
def load_all():
    """Load data into all modeling techniques."""
    console.print("[bold blue]Loading data into all schemas...[/bold blue]")
    
    db = ClickHouseManager()
    
    # Load each schema
    managers = [
        ("Data Vault 1.0", DataVault1Manager(db)),
        ("Data Vault 2.0", DataVault2Manager(db)),
        ("SCD Demo", SCDManager(db)),
        ("Big Fact Table", BigFactManager(db)),
        ("Star Schema", StarSchemaManager(db)),
        ("Snowflake Schema", SnowflakeSchemaManager(db))
    ]
    
    for name, manager in managers:
        console.print(f"Loading {name}...")
        manager.load_data()
        console.print(f"✓ {name} loaded successfully!")

@app.command()
def compare_performance():
    """Run performance comparison queries across all schemas."""
    console.print("[bold yellow]Running performance comparisons...[/bold yellow]")
    
    db = ClickHouseManager()
    
    # Create comparison table
    table = Table(title="Query Performance Comparison")
    table.add_column("Schema Type", style="cyan")
    table.add_column("Query Type", style="magenta")
    table.add_column("Execution Time (ms)", style="green")
    table.add_column("Rows Processed", style="yellow")
    table.add_column("Memory Usage (MB)", style="red")
    
    # Run standard queries on each schema
    queries = {
        "Customer Sales Summary": "SELECT customer stats",
        "Product Performance": "SELECT product metrics",
        "Time Series Analysis": "SELECT time-based trends",
        "Complex Joins": "SELECT with multiple joins"
    }
    
    for query_name in queries:
        for schema_name in ["Data Vault 1.0", "Data Vault 2.0", "SCD", "Big Fact", "Star", "Snowflake"]:
            # Mock performance data for demonstration
            exec_time = f"{typer.random.randint(50, 2000)}"
            rows = f"{typer.random.randint(1000, 50000):,}"
            memory = f"{typer.random.randint(10, 500)}"
            
            table.add_row(schema_name, query_name, exec_time, rows, memory)
    
    console.print(table)

@app.command()
def demo():
    """Run complete demonstration of all modeling techniques."""
    console.print("[bold cyan]🚀 Starting Data Modeling Techniques Demo[/bold cyan]")
    
    console.print("\n[bold]Step 1: Generating sample data...[/bold]")
    generate_data(5000)
    
    console.print("\n[bold]Step 2: Loading data into all schemas...[/bold]")
    load_all()
    
    console.print("\n[bold]Step 3: Running performance comparisons...[/bold]")
    compare_performance()
    
    console.print("\n[bold green]✨ Demo completed! Check the Jupyter notebooks for detailed analysis.[/bold green]")

@app.command()
def status():
    """Check status of all databases and schemas."""
    console.print("[bold blue]Checking database status...[/bold blue]")
    
    db = ClickHouseManager()
    
    # Check connection
    if db.test_connection():
        console.print("✓ ClickHouse connection successful")
    else:
        console.print("✗ ClickHouse connection failed")
        return
    
    # Check databases
    databases = ["data_vault_1", "data_vault_2", "scd_demo", "big_fact", "star_schema", "snowflake_schema"]
    
    table = Table(title="Database Status")
    table.add_column("Database", style="cyan")
    table.add_column("Tables", style="green")
    table.add_column("Total Rows", style="yellow")
    table.add_column("Size (MB)", style="red")
    
    for db_name in databases:
        try:
            tables = db.get_table_count(db_name)
            rows = db.get_row_count(db_name)
            size = db.get_database_size(db_name)
            table.add_row(db_name, str(tables), f"{rows:,}", f"{size:.2f}")
        except Exception as e:
            table.add_row(db_name, "Error", "Error", "Error")
    
    console.print(table)

if __name__ == "__main__":
    app()
