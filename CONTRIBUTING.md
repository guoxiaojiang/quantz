## 环境配置
### Redis 数据库
```bash
# Docker 安装 redis 数据库
docker pull redis
## 运行 redis 数据库
docker run -p 6379:6370 --name quant-redis -v /Users/yuz/proj/quant/redis_db:/data -d redis redis-server --appendonly yes
```
```bash
pip install .
```

## Mongodb

```bash
docker pull mongo
pip install mongoengine
docker run -name mongo -v /Volumes/data/proj/mongo/db:/data/db -v /Volumes/data/proj/mongo/etc/:/etc/mongo -p 27017:27017 -d mongo --config /etc/mongo/mongod.conf
# 或
docker run -p 27017:27017 -d -v /Users/yuz/proj/quant/mongo_db:/data/db --name mongo_quant mongo
```



## Run mafilter.py in IPython

```bash
cd QuantZ
```
```python
import os
import sys
sys.path.extend(os.getcwd())
%run quant/mafilter.py

```

## Trouble Shooting
1. 安装TA-Lib 失败
    Python 版本的TA-Lib 是C版本的封装，先手工安装C版本的TA-Lib后再使用 `pip install ta-lib`

2. 运行 `ma_filter` 提示无法找到 talib_lib.so.0

    ```LD_LIBRARY_PATH="/usr/local/lib:$LD_LIARARY_PATH" ma_filter```

3. TODO
