#!/usr/bin/env python3
"""
Exercise 4: Advanced Data Pipeline
Level: Advanced

Learning Objectives:
- Build complete data processing pipelines
- Handle multiple data sources
- Implement error handling and logging
- Create reusable data processing functions
- Generate comprehensive analytics

Tasks:
1. Create a data ingestion pipeline
2. Implement data validation and cleaning
3. Perform multi-step data transformations
4. Create aggregated reports and visualizations
5. Implement proper error handling
6. Build a reusable data processing class
"""

from hdfs import InsecureClient
import pandas as pd
import json
import logging
from datetime import datetime
from io import StringIO
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HDFSDataPipeline:
    """A comprehensive data processing pipeline for HDFS"""
    
    def __init__(self, hdfs_host='namenode', hdfs_port=8020):
        """Initialize the data pipeline"""
        # TODO: Initialize HDFS connection and setup logging
        pass
    
    def validate_data(self, df, required_columns):
        """Validate DataFrame structure and data quality"""
        # TODO: Implement data validation
        # Check for required columns
        # Check for missing values
        # Check for data types
        # Log validation results
        pass
    
    def clean_data(self, df):
        """Clean and preprocess data"""
        # TODO: Implement data cleaning
        # Handle missing values
        # Remove duplicates
        # Standardize formats
        # Log cleaning results
        pass
    
    def aggregate_data(self, df, group_by_columns, agg_functions):
        """Perform data aggregations"""
        # TODO: Implement aggregation logic
        # Group data by specified columns
        # Apply aggregation functions
        # Return aggregated results
        pass
    
    def generate_insights(self, df):
        """Generate business insights from data"""
        # TODO: Implement insight generation
        # Calculate key metrics
        # Identify trends and patterns
        # Create summary statistics
        pass
    
    def save_results(self, data, filename, format='csv'):
        """Save processed data to HDFS"""
        # TODO: Implement save functionality
        # Support multiple formats (CSV, JSON, TXT)
        # Handle errors gracefully
        # Log save operations
        pass
    
    def run_pipeline(self, input_path, output_dir):
        """Execute the complete data pipeline"""
        # TODO: Implement main pipeline logic
        # 1. Read data from HDFS
        # 2. Validate data
        # 3. Clean data
        # 4. Process and aggregate
        # 5. Generate insights
        # 6. Save results
        # 7. Create summary report
        pass

def exercise4():
    """Complete the advanced data pipeline"""
    
    # TODO: Create sample dataset for processing
    # Generate sales data with multiple dimensions
    
    # TODO: Initialize and run the data pipeline
    # Use your HDFSDataPipeline class
    
    # TODO: Implement error handling
    # Handle connection errors, file not found, etc.
    
    print("Exercise 4 completed!")

def solution_exercise4():
    """Solution for exercise 4"""
    
    class HDFSDataPipelineSolution:
        def __init__(self, hdfs_host='namenode', hdfs_port=8020):
            self.hdfs = HDFileSystem(host=hdfs_host, port=hdfs_port)
            self.logger = logging.getLogger(__name__)
            self.logger.info("Data pipeline initialized")
        
        def validate_data(self, df, required_columns):
            """Validate DataFrame structure and data quality"""
            validation_results = {
                'is_valid': True,
                'missing_columns': [],
                'null_counts': {},
                'data_types': {},
                'total_rows': len(df)
            }
            
            # Check required columns
            missing_cols = set(required_columns) - set(df.columns)
            if missing_cols:
                validation_results['missing_columns'] = list(missing_cols)
                validation_results['is_valid'] = False
                self.logger.error(f"Missing required columns: {missing_cols}")
            
            # Check for null values
            validation_results['null_counts'] = df.isnull().sum().to_dict()
            
            # Check data types
            validation_results['data_types'] = df.dtypes.to_dict()
            
            self.logger.info(f"Data validation completed. Valid: {validation_results['is_valid']}")
            return validation_results
        
        def clean_data(self, df):
            """Clean and preprocess data"""
            original_rows = len(df)
            
            # Remove duplicates
            df_cleaned = df.drop_duplicates()
            
            # Handle missing values
            for column in df_cleaned.columns:
                if df_cleaned[column].dtype in ['int64', 'float64']:
                    df_cleaned[column].fillna(df_cleaned[column].median(), inplace=True)
                else:
                    df_cleaned[column].fillna('Unknown', inplace=True)
            
            # Standardize text columns
            text_columns = df_cleaned.select_dtypes(include=['object']).columns
            for col in text_columns:
                if col != 'date':  # Don't standardize date columns
                    df_cleaned[col] = df_cleaned[col].str.title()
            
            cleaned_rows = len(df_cleaned)
            self.logger.info(f"Data cleaning completed. {original_rows} -> {cleaned_rows} rows")
            
            return df_cleaned
        
        def aggregate_data(self, df, group_by_columns, agg_functions):
            """Perform data aggregations"""
            try:
                aggregated = df.groupby(group_by_columns).agg(agg_functions).round(2)
                self.logger.info(f"Data aggregated by {group_by_columns}")
                return aggregated
            except Exception as e:
                self.logger.error(f"Aggregation failed: {e}")
                return None
        
        def generate_insights(self, df):
            """Generate business insights from data"""
            insights = {
                'timestamp': datetime.now().isoformat(),
                'total_records': len(df),
                'date_range': {
                    'start': df['date'].min() if 'date' in df.columns else None,
                    'end': df['date'].max() if 'date' in df.columns else None
                }
            }
            
            # Numeric column insights
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            for col in numeric_columns:
                insights[f'{col}_stats'] = {
                    'mean': round(df[col].mean(), 2),
                    'median': round(df[col].median(), 2),
                    'std': round(df[col].std(), 2),
                    'min': round(df[col].min(), 2),
                    'max': round(df[col].max(), 2)
                }
            
            # Categorical insights
            categorical_columns = df.select_dtypes(include=['object']).columns
            for col in categorical_columns:
                if col != 'date':
                    insights[f'{col}_distribution'] = df[col].value_counts().head(5).to_dict()
            
            self.logger.info("Business insights generated")
            return insights
        
        def save_results(self, data, filename, format='csv'):
            """Save processed data to HDFS"""
            try:
                if format == 'csv' and isinstance(data, pd.DataFrame):
                    content = data.to_csv(index=True)
                elif format == 'json':
                    content = json.dumps(data, indent=2)
                elif format == 'txt':
                    content = str(data)
                else:
                    content = str(data)
                
                with self.hdfs.open(filename, 'wt') as f:
                    f.write(content)
                
                self.logger.info(f"Data saved to {filename}")
                return True
            except Exception as e:
                self.logger.error(f"Failed to save {filename}: {e}")
                return False
        
        def run_pipeline(self, input_path, output_dir):
            """Execute the complete data pipeline"""
            try:
                self.logger.info("Starting data pipeline execution")
                
                # 1. Read data from HDFS
                with self.hdfs.open(input_path, 'rt') as f:
                    content = f.read()
                df = pd.read_csv(StringIO(content))
                self.logger.info(f"Data loaded: {len(df)} records")
                
                # 2. Validate data
                required_columns = df.columns.tolist()
                validation = self.validate_data(df, required_columns)
                
                # 3. Clean data
                df_clean = self.clean_data(df)
                
                # 4. Create output directory
                self.hdfs.mkdir(output_dir)
                
                # 5. Perform aggregations
                if 'salary' in df_clean.columns and 'city' in df_clean.columns:
                    city_agg = self.aggregate_data(
                        df_clean, 
                        ['city'], 
                        {'salary': ['mean', 'count', 'sum'], 'age': 'mean'}
                    )
                    if city_agg is not None:
                        self.save_results(city_agg, f'{output_dir}/city_analysis.csv')
                
                # 6. Generate insights
                insights = self.generate_insights(df_clean)
                self.save_results(insights, f'{output_dir}/insights.json', 'json')
                
                # 7. Save cleaned data
                self.save_results(df_clean, f'{output_dir}/cleaned_data.csv')
                
                # 8. Create summary report
                report = f"""
Data Processing Pipeline Report
==============================
Execution Time: {datetime.now().isoformat()}

Input: {input_path}
Output Directory: {output_dir}

Data Summary:
- Original Records: {validation['total_rows']}
- Processed Records: {len(df_clean)}
- Data Quality: {'PASS' if validation['is_valid'] else 'FAIL'}

Generated Files:
- cleaned_data.csv: Processed dataset
- city_analysis.csv: City-wise aggregations
- insights.json: Business insights
- pipeline_report.txt: This summary

Pipeline Status: COMPLETED SUCCESSFULLY
"""
                self.save_results(report, f'{output_dir}/pipeline_report.txt', 'txt')
                
                self.logger.info("Data pipeline completed successfully")
                return True
                
            except Exception as e:
                self.logger.error(f"Pipeline failed: {e}")
                return False
    
    # Generate sample data for the pipeline
    hdfs = HDFileSystem(host='namenode', port=8020)
    
    # Create more complex sample data
    np.random.seed(42)
    n_records = 200
    
    sample_data = {
        'employee_id': range(1, n_records + 1),
        'name': [f'Employee_{i}' for i in range(1, n_records + 1)],
        'age': np.random.randint(22, 65, n_records),
        'city': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], n_records),
        'department': np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR', 'Finance'], n_records),
        'salary': np.random.randint(50000, 150000, n_records),
        'experience_years': np.random.randint(0, 20, n_records),
        'date': pd.date_range('2023-01-01', periods=n_records, freq='D').strftime('%Y-%m-%d')
    }
    
    # Add some missing values for testing
    sample_df = pd.DataFrame(sample_data)
    sample_df.loc[10:15, 'salary'] = np.nan
    sample_df.loc[20:22, 'city'] = np.nan
    
    # Save sample data to HDFS
    hdfs.mkdir('/exercises/exercise4/')
    sample_csv = sample_df.to_csv(index=False)
    with hdfs.open('/exercises/exercise4/sample_employee_data.csv', 'wt') as f:
        f.write(sample_csv)
    
    # Run the pipeline
    pipeline = HDFSDataPipelineSolution()
    success = pipeline.run_pipeline(
        '/exercises/exercise4/sample_employee_data.csv',
        '/exercises/exercise4/output'
    )
    
    if success:
        print("Advanced data pipeline completed successfully!")
        print("Check /exercises/exercise4/output/ for results")
    else:
        print("Pipeline execution failed - check logs")

if __name__ == "__main__":
    # Run your solution here
    exercise4()
    
    # Uncomment to see the complete solution
    # solution_exercise4()

# Expected Output:
"""
2023-XX-XX XX:XX:XX,XXX - INFO - Data pipeline initialized
2023-XX-XX XX:XX:XX,XXX - INFO - Data loaded: 200 records
2023-XX-XX XX:XX:XX,XXX - INFO - Data validation completed. Valid: True
2023-XX-XX XX:XX:XX,XXX - INFO - Data cleaning completed. 200 -> 200 rows
2023-XX-XX XX:XX:XX,XXX - INFO - Data aggregated by ['city']
2023-XX-XX XX:XX:XX,XXX - INFO - Data saved to /exercises/exercise4/output/city_analysis.csv
2023-XX-XX XX:XX:XX,XXX - INFO - Business insights generated
2023-XX-XX XX:XX:XX,XXX - INFO - Data saved to /exercises/exercise4/output/insights.json
2023-XX-XX XX:XX:XX,XXX - INFO - Data saved to /exercises/exercise4/output/cleaned_data.csv
2023-XX-XX XX:XX:XX,XXX - INFO - Data saved to /exercises/exercise4/output/pipeline_report.txt
2023-XX-XX XX:XX:XX,XXX - INFO - Data pipeline completed successfully
Advanced data pipeline completed successfully!
Check /exercises/exercise4/output/ for results
Exercise 4 completed!
"""
