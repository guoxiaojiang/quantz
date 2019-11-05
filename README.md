[![Build Status](https://travis-ci.com/zhangyuz/quantz.svg?token=Dy7SZxVytRKD6vwS4HXe&branch=master)](https://travis-ci.com/zhangyuz/quantz)     [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)     [![Codacy Badge](https://api.codacy.com/project/badge/Grade/c8a2783a237949db9865259119e0fe56)](https://www.codacy.com/manual/leran0222/quantz?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=zhangyuz/quantz&amp;utm_campaign=Badge_Grade)

## 安装

本程序依赖 Anaconda Python 环境，请预先安装好 Anaconda 或 Miniconda。

```bash
# Requires mongodb for data storage
docker pull mongo
# Python driver for mongodb
pip install mongoengine
# Run mongodb
docker run -p 27017:27017 -d -v /Volumes/data/mongo_db:/data/db --name mongo_quant mongo
# Install quantz
pip install .
```

## 运行

由于本程序依赖 tushare 获取股票数据，在使用之前，请先注册你自己的 tushare 账号且积分达到600以上，并保存你的 token 到一个 Python 文件，供运行使用，可以点击这里注册 tushare 账号。

``` Python
ts_token_list = ('aaaaaaa',
                 'bbbbbbb')
'''积分超过600的token，用于有积分要求的接口调用'''

tmp_ts_token_list = ('ccccccc',
                  'eeeeeee',
                  'ddddddd')
'''积分少于600的token，用于没有积分要求的接口调用'''
```

```bash
ma_filter --help
growing_value_filter --help
```

