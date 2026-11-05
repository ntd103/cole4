# Pandas Advanced Analytics Assignment
## E-Commerce Sales Data Analysis

### Assignment Overview
You will work with a real-world e-commerce dataset to demonstrate your mastery of advanced pandas techniques. This assignment covers all the concepts from our technical deep dive session.

### Dataset Information
**Dataset**: E-Commerce Sales Data (2019-2023)
**Source**: [Kaggle E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (or similar)
**Size**: ~100,000 transactions
**Format**: CSV files

### Learning Objectives
By completing this assignment, you will demonstrate proficiency in:
- Advanced data cleaning and imputation techniques
- Complex grouping and aggregation operations
- Multi-table data merging strategies
- MultiIndex manipulation and hierarchical analysis
- Data reshaping with pivot tables and stacking
- Performance optimization with vectorized operations

---

## Part 1: Data Acquisition and Initial Setup (10 points)

### Task 1.1: Data Download and Loading
```python
# Download the dataset from the provided link
# Load the main sales data and any additional tables (customers, products, etc.)
# Display basic information about the dataset structure
```

**Requirements:**
1. Download the e-commerce dataset (instructions will be provided)
2. Load all CSV files into separate DataFrames
3. Display shape, columns, and data types for each DataFrame
4. Provide a brief description of what each table contains

### Task 1.2: Data Quality Assessment
```python
# Assess data quality across all tables
# Identify missing values, duplicates, and potential inconsistencies
```

**Deliverables:**
1. Missing value analysis for each table
2. Duplicate record identification
3. Data type inconsistencies report
4. Initial observations about data quality issues

---

## Part 2: Advanced Data Cleaning (20 points)

### Task 2.1: Replacing and Thresholding
```python
# Clean inconsistent categorical values
# Apply thresholding to numerical outliers
# Standardize text data (case, formatting)
```

**Requirements:**
1. Identify and fix inconsistent categorical values (e.g., different spellings, cases)
2. Use statistical thresholds (percentiles) to cap extreme outliers
3. Replace invalid or suspicious values with appropriate alternatives
4. Document all cleaning decisions with explanations

### Task 2.2: Intelligent Imputation Strategy
```python
# Implement sophisticated imputation techniques
# Use group-based imputation where appropriate
# Apply different strategies for different data types
```

**Advanced Requirements:**
1. **Numerical data**: Use group-based mean/median imputation
2. **Categorical data**: Use mode or forward-fill based on context
3. **Time-based data**: Use interpolation or seasonal patterns
4. **Business logic**: Apply domain knowledge for sensible defaults

### Task 2.3: Data Validation
```python
# Validate cleaning results
# Ensure data integrity after modifications
```

**Validation Steps:**
1. Confirm no impossible values exist (negative quantities, future dates, etc.)
2. Verify referential integrity between tables
3. Check that distributions remain reasonable after cleaning

---

## Part 3: Function Application Mastery (15 points)

### Task 3.1: Performance Comparison
```python
# Implement the same transformation using apply, map, and vectorized operations
# Compare performance and explain when to use each approach
```

**Challenge Task:**
Create a customer lifetime value (CLV) calculation using all three methods:
1. **Vectorized**: Using pandas/numpy operations
2. **Apply**: Using a custom function with complex business logic
3. **Map**: Using a pre-computed lookup dictionary

Measure and compare execution times.

### Task 3.2: Complex Business Logic Implementation
```python
# Implement sophisticated customer segmentation
# Create product recommendation scores
# Calculate advanced metrics using apply functions
```

**Business Rules to Implement:**
1. **Customer Segmentation**: Based on RFM analysis (Recency, Frequency, Monetary)
2. **Product Scoring**: Seasonal demand patterns, profit margins, inventory turnover
3. **Loyalty Programs**: Dynamic tier assignment based on multiple factors

---

## Part 4: Advanced Grouping Operations (20 points)

### Task 4.1: Multi-level Grouping Analysis
```python
# Perform complex grouping operations
# Use multiple aggregation functions simultaneously
# Implement custom aggregation logic
```

**Required Analyses:**
1. **Sales Performance**: By product category, region, and time period
2. **Customer Behavior**: Segmented analysis of purchase patterns
3. **Seasonal Trends**: Month-over-month and year-over-year comparisons

### Task 4.2: Transform Operations
```python
# Use transform for within-group calculations
# Calculate rolling statistics and ranks
# Perform group-wise normalization
```

**Transform Examples:**
1. Calculate each customer's percentile rank within their segment
2. Compute rolling 3-month average sales by product
3. Standardize sales amounts within each category (z-score)

### Task 4.3: Named Aggregations and Custom Functions
```python
# Implement named aggregations for clarity
# Create custom aggregation functions for business metrics
```

**Custom Metrics to Calculate:**
1. **Customer Retention Rate**: Percentage of customers who made repeat purchases
2. **Product Performance Score**: Composite metric combining sales, margins, and growth
3. **Regional Market Share**: Each region's contribution to total sales

---

## Part 5: Data Integration and Merging (15 points)

### Task 5.1: Complex Merge Operations
```python
# Merge multiple tables using different join types
# Handle merge conflicts and validate results
# Create a comprehensive analytical dataset
```

**Merge Requirements:**
1. Combine sales, customer, and product data
2. Handle one-to-many and many-to-many relationships appropriately
3. Use merge indicators to track data lineage
4. Validate merge results and handle unmatched records

### Task 5.2: Data Enrichment
```python
# Add calculated fields from merged data
# Create derived metrics across tables
# Build feature-rich dataset for analysis
```

**Enrichment Tasks:**
1. Calculate customer acquisition cost and lifetime value
2. Add product profitability and inventory metrics
3. Create geographic and demographic enrichment
4. Generate time-based features (seasonality, trends)

---

## Part 6: MultiIndex and Hierarchical Data (10 points)

### Task 6.1: MultiIndex Creation and Manipulation
```python
# Create meaningful MultiIndex structures
# Perform cross-sectional analysis
# Navigate hierarchical data efficiently
```

**MultiIndex Applications:**
1. **Time Series**: Year-Month-Day hierarchy for temporal analysis
2. **Geographic**: Country-Region-City hierarchy for location analysis
3. **Product**: Category-Subcategory-Product hierarchy for product analysis

### Task 6.2: Advanced MultiIndex Operations
```python
# Use xs(), loc[], and level-based operations
# Perform aggregations at different hierarchy levels
# Navigate between index levels efficiently
```

---

## Part 7: Pivoting and Reshaping (10 points)

### Task 7.1: Comprehensive Pivot Analysis
```python
# Create pivot tables with margins
# Handle multiple value columns
# Generate business-ready summary tables
```

**Pivot Table Requirements:**
1. **Sales Dashboard**: Products × Time periods with margins
2. **Performance Matrix**: Sales reps × Regions with multiple metrics
3. **Customer Analysis**: Segments × Purchase behaviors with totals

### Task 7.2: Stacking and Unstacking
```python
# Demonstrate stacking/unstacking for data reshaping
# Convert between wide and long formats
# Prepare data for visualization and further analysis
```

---

## Part 8: Advanced Analytics and Insights (Bonus: 10 points)

### Task 8.1: Business Intelligence Dashboard
```python
# Create a comprehensive analytical summary
# Generate actionable business insights
# Build key performance indicators (KPIs)
```

**Dashboard Components:**
1. **Executive Summary**: Key metrics and trends
2. **Performance Analytics**: Top/bottom performers identification
3. **Predictive Insights**: Trends and forecasting indicators
4. **Recommendations**: Data-driven business suggestions

### Task 8.2: Advanced Statistical Analysis
```python
# Perform correlation analysis
# Identify trends and patterns
# Create customer cohort analysis
```

---

## Submission Requirements

### Code Requirements
1. **Jupyter Notebook**: Well-commented, professional presentation
2. **Code Quality**: Follow PEP 8 standards, use meaningful variable names
3. **Error Handling**: Include appropriate try-catch blocks for data operations
4. **Performance**: Use efficient pandas operations, avoid loops where possible

### Documentation Requirements
1. **Executive Summary**: 1-page summary of key findings and insights
2. **Technical Documentation**: Explanation of complex operations and decisions
3. **Data Dictionary**: Description of all calculated fields and transformations
4. **Assumptions**: Document any assumptions made during analysis

### Deliverables Checklist
- [ ] Complete Jupyter notebook with all tasks
- [ ] Executive summary document
- [ ] Data quality report
- [ ] Performance comparison results
- [ ] Business insights and recommendations
- [ ] Clean, processed datasets (exported as CSV)

---

## Evaluation Criteria

### Technical Skills (70%)
- **Data Cleaning**: Sophistication and appropriateness of cleaning techniques
- **Function Application**: Correct use of apply/map/vectorized operations
- **Grouping Operations**: Complex aggregations and transformations
- **Data Merging**: Proper handling of multiple table joins
- **MultiIndex**: Effective use of hierarchical indexing
- **Pivoting**: Advanced reshaping and summarization

### Business Acumen (20%)
- **Insight Generation**: Quality and relevance of business insights
- **Recommendations**: Actionable suggestions based on data analysis
- **KPI Development**: Meaningful metrics for business monitoring

### Presentation (10%)
- **Code Quality**: Clean, readable, well-documented code
- **Documentation**: Clear explanations and methodology
- **Visualization**: Effective use of plots and tables

---

## Bonus Challenges

### Challenge 1: Performance Optimization
Compare processing times for different approaches and optimize slow operations.

### Challenge 2: Memory Efficiency
Handle large datasets efficiently using chunking and memory-optimized data types.

### Challenge 3: Advanced Visualizations
Create interactive dashboards using plotly or create publication-ready plots.

---

## Academic Integrity
This is an individual assignment. While you may discuss concepts with classmates, all code and analysis must be your own original work. Properly cite any external resources or code snippets used.

**Good luck with your analysis!**