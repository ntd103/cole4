#!/bin/bash

# Exercise runner script
echo "Hadoop/HDFS Python Integration - Exercise Runner"
echo "================================================"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <exercise_number>"
    echo "Available exercises:"
    echo "  1 - Basic HDFS Operations"
    echo "  2 - Data Processing"
    echo "  3 - Text Processing and Word Count"
    echo "  4 - Advanced Data Pipeline"
    echo "  demo - Run the complete demo"
    exit 1
fi

EXERCISE_NUM=$1

case $EXERCISE_NUM in
    1)
        echo "Running Exercise 1: Basic HDFS Operations"
        docker exec -it hadoop-python-client python /exercises/exercise1_basic_operations.py
        ;;
    2)
        echo "Running Exercise 2: Data Processing"
        docker exec -it hadoop-python-client python /exercises/exercise2_data_processing.py
        ;;
    3)
        echo "Running Exercise 3: Text Processing"
        docker exec -it hadoop-python-client python /exercises/exercise3_text_processing.py
        ;;
    4)
        echo "Running Exercise 4: Advanced Pipeline"
        docker exec -it hadoop-python-client python /exercises/exercise4_advanced_pipeline.py
        ;;
    demo)
        echo "Running Complete Demo"
        docker exec -it hadoop-python-client python /app/hdfs_demo.py
        ;;
    *)
        echo "Invalid exercise number. Use 1-4 or 'demo'"
        exit 1
        ;;
esac
