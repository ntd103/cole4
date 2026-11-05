## Step 1: Setup

Cài `GNU make`

```bash
sudo apt update
sudo apt install make
make --version
```
    
Chạy
```bash
make up
```

Lỗi vì file Makefile đang dùng `docker-compose` (v1), thay bằng `docker compose` (v2 - bỏ gạch nối)

Lỗi 
```
 => ERROR [jupyter 3/7] RUN pip install --no-cache-dir     duckdb==0.9.2     pandas==2.1.4     pyarrow==14.0.1     plotly==5.17.0     seaborn==0.13.0  8.4s

...

 => CANCELED [data-generator 3/5] RUN pip install --no-cache-dir     pandas==2.1.4     faker==20.1.0     numpy==1.24.3     pyarrow==14.0.1     tqdm==  6.6s

 ...

 7.302 Requirement already satisfied: tqdm==4.66.1 in /opt/conda/lib/python3.11/site-packages (4.66.1)
7.664 ERROR: Could not find a version that satisfies the requirement jupyter-lab==4.0.9 (from versions: none)
7.665 ERROR: No matching distribution found for jupyter-lab==4.0.9

...

target jupyter: failed to solve: process "/bin/bash -o pipefail -c pip install --no-cache-dir     duckdb==0.9.2     pandas==2.1.4     pyarrow==14.0.1     plotly==5.17.0     seaborn==0.13.0     faker==20.1.0     memory-profiler==0.61.0     psutil==5.9.6     tqdm==4.66.1     jupyter-lab==4.0.9     ipywidgets==8.1.1     nbconvert==7.12.0" did not complete successfully: exit code: 1

make: *** [Makefile:23: build] Error 1
```

**Check Dockerfile**

Lỗi `ERROR: Could not find a version that satisfies the requirement jupyter-lab==4.0.9 (from versions: none)` 
=> Trên PyPI không có pakage `jupyter-lab` mà thay vào đó là `jupyterlab` (không có dấu gạch nối).

Check phiên bản, có tồn tại trên PyPI

Check phiên bản cài sẵn trong `jupyter/scipy-notebook:latest`

Tạo container vào bash, thêm `--rm` để tự xoá sau khi xong
```bash
docker run -it --rm jupyter/scipy-notebook:latest bash
```

```bash
pip show jupyterlab pandas
```

=> Trong image đã có sẵn pandas 2.1.1 và jupyterlab 4.0.7. Ghi đè. 