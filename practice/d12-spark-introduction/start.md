image bitnami đã thương mại hoá không pull được, thay bằng bitnamilegacy/spark:3.5

Danh sách các port:
- http://localhost:8080/: Spark Web UI
- http://localhost:7077/: Spark Master Port
- http://localhost:8888/: Jupyter Notebook
- http://localhost:8889/: Jupyter Lab

Step1: Chạy `docker compose up -d`
Step2: Đã có sẵn data, k cần gen. Chạy `docker exec --user spark spark-master python3 /home/spark/scripts/spark_demo_basic.py`

(Thêm `--user spark`)

Bug1: Thêm user: "root" trong docker-compose.yml để tránh lỗi permission denied khi chạy spark-submit
Bug2: Lỗi trong spark_demo_basic.py

```sql
  SELECT 
        category,
        date,
        total_amount,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY total_amount DESC) as rank,
        SUM(total_amount) OVER (PARTITION BY category) as category_total
    FROM sales
    QUALIFY rank <= 3
```
1. QUALIFY dùng để lọc kết quả của WIndow Function ngay trong 1 query mà không cần bọc Subquery/CTE. Tuy nhiên chỉ hỗ trợ trên Databricks SQL, Snowflake SQL, BigQuery SQL. Spark SQL không hỗ trợ QUALIFY nên cần bọc Subquery/CTE để lọc kết quả của Window Function.
=> Viết CTE

```sql
    WITH ranked_sales AS (
        SELECT
            category,
            date,
            total_amount,
            ROW_NUMBER() OVER (PARTITION BY category ORDER BY total_amount DESC) as rank,
            SUM(total_amount) OVER (PARTITION BY category) as category_total
        FROM sales
    )
    SELECT * FROM ranked_sales WHERE rank <= 3
```

