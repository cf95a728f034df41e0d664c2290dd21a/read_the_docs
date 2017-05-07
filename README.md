# 1. Requirements
```bash
git clone <repository>
cd <repository_directory>
python3 -m venv env  # Python >= 3.5.0
env/bin/pip install -r requirements.txt
```

# 2. AsyncIOPool
Coroutine pool, it's more lightweight and faster than thread and process

### 2.1. Usage:
```python
pool = AsyncIOPool(loop, workers, timeout, default)
for arg, ret in pool.map(coroutine, sequence):
    pass
```

### 2.2. Benchmark:
```bash
# usage
test_aio_pool.py --sleep SLEEP --sample SAMPLE --workers WORKERS [--log-level LOG_LEVEL]

# examples
env/bin/python test_aio_pool.py --sleep 0.1 --sample 100 --workers 10
env/bin/python test_aio_pool.py --sleep 1 --sample 1000 --workers 100
env/bin/python test_aio_pool.py --sleep 10 --sample 10000 --workers 1000

# output
------------------------------    sleep: 0.1, sample: 100, works: 10    ------------------------------
coroutine map benchmark: 1.006 seconds
thread map benchmark: 1.354 seconds
process map benchmark: 1.274 seconds
------------------------------    sleep: 1, sample: 1000, works: 100    ------------------------------
coroutine map benchmark: 10.023 seconds
thread map benchmark: 12.135 seconds
process map benchmark: 12.393 seconds
------------------------------    sleep: 10, sample: 10000, works: 1000    ------------------------------
coroutine map benchmark: 100.160 seconds
thread map benchmark: 129.090 seconds
process map benchmark: BlockingIOError: [Errno 35] Resource temporarily unavailable
```

# 3. Downloader
### 3.1. Usage:
```python
downloader = Downloader(url, path, name, timeout, bytes_per_time, max_connections)
downloader.start()
```
### 3.2. Command line:
```bash
downloader.py --url URL [--path PATH] [--name NAME] [--timeout TIMEOUT] [--bytes-per-time BYTES_PER_TIME] [--max-connections MAX_CONNECTIONS]

# example
env/bin/python downloader.py --url http://mirrors.hust.edu.cn/apache/hadoop/common/hadoop-2.8.0/hadoop-2.8.0.tar.gz --bytes-per-time 1048576

# output
4% (18 of 411) |#                                                                                | Elapsed Time: 0:00:08 ETA: 0:03:21
```

# 4. ReadTheDocsDownloader
### 4.1. Usage:
```python
read_the_docs = ReadTheDocsDownloader(project, version, path, timeout, bytes_per_time, max_connections)
read_the_docs.start()
```
### 4.2. Command line:
```bash
read_the_docs.py --project PROJECT [--version VERSION] [--path PATH] [--timeout TIMEOUT] [--bytes-per-time BYTES_PER_TIME] [--max-connections MAX_CONNECTIONS]

# example
env/bin/python read_the_docs.py --project aiohttp --bytes-per-time 102400

# output
49% (82 of 166) |#######################################                                          | Elapsed Time: 0:00:06 ETA: 0:00:08
```
