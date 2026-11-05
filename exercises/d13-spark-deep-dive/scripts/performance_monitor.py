#!/usr/bin/env python3
"""
Spark Performance Monitor Script
This script provides utilities to monitor Spark application performance
"""

from pyspark.sql import SparkSession
import time
import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

class SparkPerformanceMonitor:
    def __init__(self, spark_session):
        self.spark = spark_session
        self.metrics_history = []
    
    def collect_metrics(self):
        """Collect current Spark application metrics"""
        status_tracker = self.spark.sparkContext.statusTracker()
        
        # Get executor information
        executor_infos = status_tracker.getExecutorInfos()
        
        # Get job information
        active_jobs = status_tracker.getActiveJobIds()
        active_stages = status_tracker.getActiveStageIds()
        
        # Get RDD information
        rdd_infos = status_tracker.getRDDInfos()
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'executors': [],
            'active_jobs': len(active_jobs),
            'active_stages': len(active_stages),
            'cached_rdds': len([rdd for rdd in rdd_infos if rdd.numCachedPartitions > 0]),
            'total_memory_mb': 0,
            'used_memory_mb': 0,
            'total_cores': 0
        }
        
        for executor in executor_infos:
            executor_metrics = {
                'executor_id': executor.executorId,
                'host': executor.host,
                'total_cores': executor.totalCores,
                'max_memory_mb': executor.maxMemory / 1024 / 1024,
                'used_memory_mb': executor.memoryUsed / 1024 / 1024,
                'disk_used_mb': executor.diskUsed / 1024 / 1024,
                'active_tasks': executor.activeTasks,
                'total_tasks': executor.totalTasks,
                'failed_tasks': executor.failedTasks
            }
            
            metrics['executors'].append(executor_metrics)
            metrics['total_memory_mb'] += executor_metrics['max_memory_mb']
            metrics['used_memory_mb'] += executor_metrics['used_memory_mb']
            metrics['total_cores'] += executor_metrics['total_cores']
        
        # Calculate utilization percentages
        if metrics['total_memory_mb'] > 0:
            metrics['memory_utilization_pct'] = (metrics['used_memory_mb'] / metrics['total_memory_mb']) * 100
        else:
            metrics['memory_utilization_pct'] = 0
        
        self.metrics_history.append(metrics)
        return metrics
    
    def monitor_job_execution(self, job_function, job_name="Unknown Job"):
        """Monitor a specific job execution"""
        print(f"Starting monitoring for job: {job_name}")
        
        # Collect pre-execution metrics
        pre_metrics = self.collect_metrics()
        
        # Execute the job
        start_time = time.time()
        try:
            result = job_function()
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Collect post-execution metrics
        post_metrics = self.collect_metrics()
        
        job_report = {
            'job_name': job_name,
            'execution_time_seconds': execution_time,
            'success': success,
            'error': error,
            'pre_execution_metrics': pre_metrics,
            'post_execution_metrics': post_metrics,
            'memory_delta_mb': post_metrics['used_memory_mb'] - pre_metrics['used_memory_mb']
        }
        
        print(f"Job completed: {job_name}")
        print(f"Execution time: {execution_time:.3f} seconds")
        print(f"Memory delta: {job_report['memory_delta_mb']:.1f} MB")
        print(f"Success: {success}")
        
        return job_report, result
    
    def generate_performance_report(self):
        """Generate a comprehensive performance report"""
        if not self.metrics_history:
            print("No metrics collected yet")
            return
        
        # Convert to DataFrame for analysis
        df_data = []
        for metrics in self.metrics_history:
            df_data.append({
                'timestamp': metrics['timestamp'],
                'total_memory_mb': metrics['total_memory_mb'],
                'used_memory_mb': metrics['used_memory_mb'],
                'memory_utilization_pct': metrics['memory_utilization_pct'],
                'active_jobs': metrics['active_jobs'],
                'active_stages': metrics['active_stages'],
                'cached_rdds': metrics['cached_rdds'],
                'total_cores': metrics['total_cores']
            })
        
        df = pd.DataFrame(df_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Generate visualizations
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Memory utilization over time
        axes[0, 0].plot(df['timestamp'], df['memory_utilization_pct'], 'b-', linewidth=2)
        axes[0, 0].set_title('Memory Utilization Over Time')
        axes[0, 0].set_ylabel('Memory Utilization (%)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Active jobs and stages
        axes[0, 1].plot(df['timestamp'], df['active_jobs'], 'g-', label='Active Jobs', linewidth=2)
        axes[0, 1].plot(df['timestamp'], df['active_stages'], 'r-', label='Active Stages', linewidth=2)
        axes[0, 1].set_title('Active Jobs and Stages')
        axes[0, 1].set_ylabel('Count')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Memory usage (absolute)
        axes[1, 0].plot(df['timestamp'], df['used_memory_mb'], 'orange', linewidth=2)
        axes[1, 0].set_title('Memory Usage (MB)')
        axes[1, 0].set_ylabel('Memory (MB)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Cached RDDs
        axes[1, 1].plot(df['timestamp'], df['cached_rdds'], 'purple', linewidth=2)
        axes[1, 1].set_title('Cached RDDs')
        axes[1, 1].set_ylabel('Count')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Print summary statistics
        print("Performance Summary:")
        print(f"Average Memory Utilization: {df['memory_utilization_pct'].mean():.1f}%")
        print(f"Peak Memory Utilization: {df['memory_utilization_pct'].max():.1f}%")
        print(f"Average Active Jobs: {df['active_jobs'].mean():.1f}")
        print(f"Max Active Jobs: {df['active_jobs'].max()}")
        print(f"Total Cores Available: {df['total_cores'].iloc[-1] if not df.empty else 0}")
    
    def save_metrics_to_file(self, filename):
        """Save collected metrics to a JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.metrics_history, f, indent=2)
        print(f"Metrics saved to {filename}")
    
    def get_performance_recommendations(self):
        """Provide performance recommendations based on collected metrics"""
        if not self.metrics_history:
            return ["No metrics available for analysis"]
        
        latest_metrics = self.metrics_history[-1]
        recommendations = []
        
        # Memory utilization analysis
        memory_util = latest_metrics['memory_utilization_pct']
        if memory_util > 80:
            recommendations.append("⚠️  High memory utilization detected. Consider increasing executor memory or reducing cache usage.")
        elif memory_util < 20:
            recommendations.append("💡 Low memory utilization. You might be able to reduce executor memory allocation.")
        
        # Core utilization analysis
        total_cores = latest_metrics['total_cores']
        active_jobs = latest_metrics['active_jobs']
        
        if active_jobs == 0 and total_cores > 0:
            recommendations.append("📊 No active jobs. Cluster resources are idle.")
        elif active_jobs > total_cores:
            recommendations.append("⚡ More jobs than cores available. Consider optimizing job parallelism.")
        
        # Cache analysis
        cached_rdds = latest_metrics['cached_rdds']
        if cached_rdds > 10:
            recommendations.append("🗄️  Many cached RDDs detected. Ensure you're unpersisting unused caches.")
        
        # Executor analysis
        failed_tasks_total = sum(executor['failed_tasks'] for executor in latest_metrics['executors'])
        if failed_tasks_total > 0:
            recommendations.append(f"❌ {failed_tasks_total} failed tasks detected. Check for data skew or resource issues.")
        
        return recommendations

def demo_performance_monitoring():
    """Demonstrate the performance monitoring capabilities"""
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import *
    import numpy as np
    
    # Create Spark session
    spark = SparkSession.builder \
        .appName("PerformanceMonitoringDemo") \
        .master("spark://spark-master:7077") \
        .getOrCreate()
    
    # Create performance monitor
    monitor = SparkPerformanceMonitor(spark)
    
    # Collect initial metrics
    print("Collecting initial metrics...")
    monitor.collect_metrics()
    
    # Define some test jobs
    def create_large_dataset_job():
        data = [(i, f"user_{i}", np.random.uniform(1, 1000)) for i in range(50000)]
        df = spark.createDataFrame(data, "id INT, user STRING, value DOUBLE")
        df.cache()
        return df.count()
    
    def aggregation_job():
        data = [(i, np.random.choice(['A', 'B', 'C']), np.random.uniform(1, 100)) for i in range(10000)]
        df = spark.createDataFrame(data, "id INT, category STRING, value DOUBLE")
        return df.groupBy("category").agg(sum("value"), avg("value"), count("*")).collect()
    
    def join_job():
        data1 = [(i, f"user_{i}") for i in range(5000)]
        data2 = [(i, np.random.uniform(1, 500)) for i in range(5000)]
        df1 = spark.createDataFrame(data1, "id INT, name STRING")
        df2 = spark.createDataFrame(data2, "id INT, amount DOUBLE")
        return df1.join(df2, "id").count()
    
    # Monitor job executions
    jobs = [
        (create_large_dataset_job, "Create Large Dataset"),
        (aggregation_job, "Aggregation Job"),
        (join_job, "Join Job")
    ]
    
    job_reports = []
    for job_func, job_name in jobs:
        time.sleep(2)  # Brief pause between jobs
        report, result = monitor.monitor_job_execution(job_func, job_name)
        job_reports.append(report)
    
    # Generate final report
    print("\n" + "="*50)
    print("PERFORMANCE MONITORING REPORT")
    print("="*50)
    
    monitor.generate_performance_report()
    
    # Get recommendations
    recommendations = monitor.get_performance_recommendations()
    print("\nPerformance Recommendations:")
    for rec in recommendations:
        print(f"  {rec}")
    
    # Save metrics
    monitor.save_metrics_to_file("/home/jovyan/data/performance_metrics.json")
    
    spark.stop()

if __name__ == "__main__":
    demo_performance_monitoring()
