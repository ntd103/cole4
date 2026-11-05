#!/usr/bin/env python3
"""
Exercise 2: Data Processidef solution_exercise2():
    """Solution for exercise 2"""
    hdfs = InsecureClient('http://namenode:9870')with HDFS
Level: Intermediate

Learning Objectives:
- Read CSV data from HDFS
- Process data using pandas
- Perform data analysis
- Save results back to HDFS
- Handle different file formats

Tasks:
1. Read the employees CSV file from HDFS
2. Calculate statistical summaries
3. Filter data based on criteria
4. Group data and perform aggregations
5. Save processed results to HDFS in different formats
"""

from hdfs import InsecureClient
import pandas as pd
from io import StringIO
import json

def exercise2():
    """Complete the data processing tasks"""
    
    # Initialize HDFS connection
    hdfs = InsecureClient('http://namenode:9870')
    
    # TODO: Task 1 - Read CSV data from HDFS
    # Read /exercises/exercise1/employees.csv and create a pandas DataFrame
    
    # TODO: Task 2 - Calculate statistical summaries
    # Calculate mean, median, min, max for salary and age columns
    
    # TODO: Task 3 - Filter data
    # Filter employees with salary > 75000
    # Filter employees with age < 30
    
    # TODO: Task 4 - Group data and aggregate
    # Group by city and calculate average salary
    # Count employees by age groups (20-25, 26-30, 31-35, 36+)
    
    # TODO: Task 5 - Save results
    # Save filtered data as CSV
    # Save city analysis as JSON
    # Save age group analysis as text report
    
    print("Exercise 2 completed!")

def solution_exercise2():
    """Solution for exercise 2"""
    hdfs = InsecureClient('http://namenode:9870')
    
    # Task 1: Read CSV data
    with hdfs.read('/exercises/exercise1/employees.csv', encoding='utf-8') as reader:
        csv_content = reader.read()
    
    df = pd.read_csv(StringIO(csv_content))
    print("Data loaded:")
    print(df.head())
    print(f"Total records: {len(df)}")
    
    # Task 2: Statistical summaries
    print("\nStatistical Summary:")
    print(f"Average salary: ${df['salary'].mean():.2f}")
    print(f"Median salary: ${df['salary'].median():.2f}")
    print(f"Salary range: ${df['salary'].min():.2f} - ${df['salary'].max():.2f}")
    print(f"Average age: {df['age'].mean():.1f}")
    print(f"Age range: {df['age'].min()} - {df['age'].max()}")
    
    # Task 3: Filter data
    high_salary = df[df['salary'] > 75000]
    young_employees = df[df['age'] < 30]
    
    print(f"\nEmployees with salary > $75,000: {len(high_salary)}")
    print(f"Employees under 30: {len(young_employees)}")
    
    # Task 4: Group and aggregate
    city_analysis = df.groupby('city')['salary'].agg(['mean', 'count']).round(2)
    print("\nSalary by City:")
    print(city_analysis)
    
    # Age groups
    age_bins = [0, 25, 30, 35, 100]
    age_labels = ['20-25', '26-30', '31-35', '36+']
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=True)
    age_group_analysis = df['age_group'].value_counts()
    print("\nEmployees by Age Group:")
    print(age_group_analysis)
    
    # Task 5: Save results
    hdfs.mkdir('/exercises/exercise2/')
    
    # Save high salary employees as CSV
    high_salary_csv = high_salary.to_csv(index=False)
    with hdfs.open('/exercises/exercise2/high_salary_employees.csv', 'wt') as f:
        f.write(high_salary_csv)
    
    # Save city analysis as JSON
    city_json = city_analysis.to_dict()
    with hdfs.open('/exercises/exercise2/city_analysis.json', 'wt') as f:
        json.dump(city_json, f, indent=2)
    
    # Save comprehensive report
    report = f"""
Employee Data Analysis Report
============================

Dataset Summary:
- Total Employees: {len(df)}
- Average Salary: ${df['salary'].mean():.2f}
- Average Age: {df['age'].mean():.1f}

High Earners (>$75K): {len(high_salary)} employees
Young Employees (<30): {len(young_employees)} employees

City Analysis:
{city_analysis.to_string()}

Age Group Distribution:
{age_group_analysis.to_string()}
"""
    
    with hdfs.open('/exercises/exercise2/analysis_report.txt', 'wt') as f:
        f.write(report)
    
    print("\nResults saved to /exercises/exercise2/")
    print("Exercise 2 completed!")

if __name__ == "__main__":
    # Run your solution here
    exercise2()
    
    # Uncomment to see the complete solution
    # solution_exercise2()

# Expected Output:
"""
Data loaded:
        name  age         city  salary
0   John Doe   28     New York   75000
1  Jane Smith   32  Los Angeles   82000
...

Statistical Summary:
Average salary: $75900.00
Median salary: $75500.00
Salary range: $68000.00 - $85000.00
Average age: 29.6
Age range: 25 - 35

Employees with salary > $75,000: 6
Employees under 30: 4

Salary by City:
              mean  count
city                    
Chicago    68000.0      1
Dallas     81000.0      1
...

Results saved to /exercises/exercise2/
Exercise 2 completed!
"""
