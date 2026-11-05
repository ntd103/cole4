## Step1: Đọc docker-compose.yml

Chuyển images `pyspark-notebok:spark-3.4.1` sang `pyspark-notebook:latest` đã cài ở D2 đỡ phải cài thêm image

(trên dockerhub đã dừng update, mới nhất dùng image `quay.io/jupyter/pyspark-notebook`)

check the docs: https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html

```
services:
  jupyter:
    image: jupyter/pyspark-notebook:latest
    container_name: jupyter
    ports:
      - 8888:8888
      - 4050:4040 
    volumes:
      - ./notebooks:/home/jovyan/work
      - ./data:/home/jovyan/data
    environment:
      - SPARK_OPTS="--packages org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.3.1"
      - JUPYTER_ENABLE_LAB=yes
    command: >
      start-notebook.sh
      --NotebookApp.token=''
      --NotebookApp.password=''
      --NotebookApp.log_level='DEBUG'
```

Cấu hình trong docker-compose.yaml:
- services gồm 1 container tên jupyter dùng image `jupyter/pyspark-notebook:latest`

Trong image này, exposed port gồm:
- 8888:8888 là jupyter notebook
- 4040:4040 là spark ui

Các volume mount:
- ./notebooks:/home/jovyan/work: mount thư mục notebooks trên host vào thư mục work trong container
- ./data:/home/jovyan/data: mount thư mục data trên host vào thư mục data trong container
