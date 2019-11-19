import datetime
from datetime import timedelta
import math
import os
import re
import sys

import pandas as pd
from tushare.pro import client

from quantz.quantz_exception import QuantzException
from quantz.utils.log import *


def date_2_str(when):
    """
    date 对象转换为字符串"YYYYMMDD"形式
    :param when: 需要转换的时间，必须是 date,datetime 或 time 类型的参数
    :return:
    """
    if isinstance(when, (datetime, datetime.date, datetime.time)):
        return when.strftime('%Y%m%d')
    else:
        raise Exception('when must be one of date, datetime or time')


def today_yyyymmdd_str():
    """
    获取今天YYYYMMDD格式的日期。
    :return:
    """
    return date_2_str(datetime.today())


def today_datetime():
    return datetime.today()


def get_ts_token_from_env():
    return os.getenv('TS_TOKEN')


def get_ts_token_list(config_file):
    """
    从配置python文件中获取tushare token
    :param config_file: 配置Python 文件
    :return: 两个 tushare token tuple
    """
    config_dir = os.path.dirname(os.path.abspath(config_file))
    sys.path.extend([config_dir])
    import ts_token
    return ts_token.ts_token_list, ts_token.tmp_ts_token_list


def spit_df(df: pd.DataFrame, count: int):
    """
    将一个大的DataFrame平均分成count个小的DataFrame
    :param df: 需要分割的DataFrame
    :param count: 分割的个数
    :return: [DataFrame] 列表
    """
    size = df.shape[0]
    if size >= count:
        piece_count = math.floor(size / count)
        df_list = []
        i = 1
        while i < count:
            df_list.append(df[(i - 1) * piece_count:i * piece_count])
            logv('%s %s' % (((i - 1) * piece_count), (i * piece_count)))
            i = i + 1
        df_list.append(df[piece_count * (count - 1):])
        return df_list
    else:
        raise QuantzException('Failed to split to %s pieces' % count)


def make_ts_api(token):
    # 自定义连接超时时间
    return client.DataApi(token=token, timeout=30)


def generate_latest_report_period():
    """
    根据当前日期生成最近的报表季时间
    """
    now = datetime.now()
    month = (now.month - 1) - (now.month - 1) % 3 + 1
    last_quarter_end = datetime(now.year, month, 1) - timedelta(days=1)
    return (last_quarter_end.strftime("%Y%m%d"))


def is_valid_report_end_date(end_date: str = None):
    if end_date is None:
        return False
    elif re.match('[0-9]{6}3[01]', end_date) is not None:
        if not end_date[4:] in ('0331', '0630', '0930', '1231'):
            return False
        else:
            if int(end_date[0:4]) <= int(today_yyyymmdd_str()[0:4]):
                return True
            return False
    else:
        return False
