# Data Modeling Techniques Comparison

This project demonstrates various data modeling techniques using ClickHouse and Python:

## Data Modeling Techniques Covered

1. **Data Vault 1.0** - Traditional hub, link, and satellite structure
2. **Data Vault 2.0** - Enhanced with business vault and point-in-time tables
3. **SCD (Slowly Changing Dimensions)** - Types 1, 2, and 3
4. **Big Fact Table** - Denormalized approach
5. **Star Schema** - Traditional dimensional modeling
6. **Snowflake Schema** - Normalized dimensional modeling

## Technology Stack

- **Database**: ClickHouse
- **Language**: Python
- **Notebooks**: Jupyter Lab
- **Containerization**: Docker & Docker Compose

## Quick Start

1. Clone the repository
2. Run the project:
   ```bash
   docker-compose up -d
   ```

3. Access Jupyter Lab:
   - Main app: http://localhost:8888
   - Standalone Jupyter: http://localhost:8889

4. Access ClickHouse:
   - HTTP interface: http://localhost:8123
   - Native client: localhost:9000

## Project Structure

```
├── docker-compose.yml          # Docker services configuration
├── Dockerfile                  # Python application container
├── requirements.txt           # Python dependencies
├── src/                       # Source code
│   ├── models/               # Data model implementations
│   ├── generators/           # Data generators
│   ├── utils/               # Utility functions
│   └── main.py              # Main application
├── sql/                      # SQL scripts
│   └── init/                # Database initialization scripts
├── notebooks/               # Jupyter notebooks with examples
└── data/                   # Generated data files
```

## Sample Business Scenario

We'll model an e-commerce business with:
- **Customers** with changing addresses and preferences
- **Products** with evolving categories and pricing
- **Orders** with multiple line items
- **Suppliers** with changing information
- **Time-based events** for tracking changes

## Usage Examples

Each modeling technique is implemented with:
- Schema creation scripts
- Data loading procedures
- Sample queries demonstrating benefits/trade-offs
- Performance comparisons

## Credentials

- **ClickHouse**: admin/admin123
- **Jupyter**: No token required

## Performance Notes

This setup is optimized for learning and demonstration. For production use:
- Configure proper ClickHouse settings
- Set up appropriate security
- Optimize for your specific use case
