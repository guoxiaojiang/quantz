## 环境配置
### Redis 数据库
```bash
# Docker 安装 redis 数据库
docker pull redis
## 运行 redis 数据库
docker run --name quant-redis -v /Users/yuz/proj/quant/redis_db:/data -d redis redis-server --appendonly yes
```
```bash
pip install .
```


## Run ma888.py in IPython
```bash
cd QuantZ
```
```python
import os
import sys
sys.path.extend(os.getcwd())
%run QuantZ/quant/ma888.py

```

## Trouble Shooting
1. 安装TA-Lib 失败
    Python 版本的TA-Lib 是C版本的封装，先手工安装C版本的TA-Lib后再使用 `pip install ta-lib`
2. TODO
