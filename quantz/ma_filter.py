"""
Filter stock by ma
"""

import time

import numpy as np
import pandas as pd
import talib as ta
import tushare as ts
from tushare.pro import client

from quantz.on_target_fit_listener import OnTargetFitListener
from quantz.quantz_exception import QuantzException
from quantz.utils import miscutils
from quantz.utils.log import *


class MaFilter(object):
    def __init__(self, tushare_api: client.DataApi, on_target_fit_listener: OnTargetFitListener,
                 freq='D', time_period=60, threshold=10):
        """
        :param tushare_api:
        :param on_target_fit_listener:
        :param freq: 股票周期,支持1/5/15/30/60分钟,周/月/季/年
        :param time_period: 使用多久的均线
        :param threshold: 选股门限
        """
        if not isinstance(tushare_api, client.DataApi):
            raise QuantzException(
                'Wrong type of tushare_api, tushare.client.DataApi expected!!!')
        self.tushare_api = tushare_api
        self.on_target_fit_listener = on_target_fit_listener
        self.freq = freq
        self.time_period = time_period
        self.threshold = threshold / 100

    def __get_close(self, ts_code, start_date, end_date):
        """
        获取日线级别收盘数据，最多重试10次。
        :param ts_code:股票代码，+.SZ/.SH
        :param start_date:开始日期，如'20190101'
        :param end_date:开始日期，如'20190201'
        :return: 收盘价的ndarray，如果获取失败，抛出异常
        """
        done = False
        count = 10
        daily_close = None
        while not done and count > 0:
            count = count - 1
            try:
                daily_close = ts.pro_bar(api=self.tushare_api, ts_code=ts_code, start_date=start_date,
                                         end_date=end_date,
                                         asset='E', freq=self.freq, adj='qfq')
                done = True
            except Exception as e:
                loge(str(e))
                done = False
                time.sleep(0.501)
                logi('Retrying get close price for ' + ts_code)
                logi('try %d' % (10 - count))
            finally:
                pass
        if daily_close is None:
            raise QuantzException('Failed to get bars for ' + ts_code)
        else:
            return daily_close['close'].values
            # return daily_close['close'].values[::-1] 倒序输出

    def __ma(self, close):
        """
        获取N天移动均线，最简单的移动算术平均，取小数点后三位
        :param close: 收盘价ndarray
        :return: ma的ndarray
        """
        time_period = self.time_period
        if close.shape[0] < time_period:
            raise QuantzException(
                'Ma' + str(time_period) + ' requires at least ' + str(time_period) + ' datas, but got ' + str(
                    close.shape[
                        0]))
        # 我们只需要最后一个交易日的ma数值用于对比，因此只计算这一个
        # talib 的 SMA 就是通达信的 MA，简单的算术平均值
        ma_n = ta.SMA(close[0:time_period], timeperiod=time_period)
        # 计算出的MA值是数组的最后一个，所以只返回最后一个值即可
        ma_n = ma_n[time_period - 1:]
        return np.round(ma_n, 4)

    def __on_target_fit(self, ts_code, name, close, ma_val, ma_delta):
        logi('%s fit(%f) ' % (name, ma_delta))
        self.on_target_fit_listener.on_target_fit(
            [ts_code, name, close, ma_val, ma_delta])

    def filter_stocks(self, stocks: pd.DataFrame):
        """
        过滤符合条件的股票
        :param stocks: 需要过滤的股票
        :return: None
        """
        if stocks.shape[0] > 0:
            for row in stocks.itertuples():
                try:
                    logi('Handling ' + row.ts_code + ' ' + row.name)
                    daily_close = self.__get_close(ts_code=row.ts_code, start_date=row.list_date,
                                                   end_date=miscutils.today_yyyymmdd_str())

                    ma_val = self.__ma(close=daily_close)[0]
                    logv('%s %s (Close:%s ma%s:%s)' % (
                        row.ts_code, row.name, daily_close[0], self.time_period, ma_val))
                    ma_delta = (daily_close[0] - ma_val) / daily_close[0]
                    logi(row.name + ':' + str(ma_delta))
                    if abs(ma_delta) <= self.threshold:
                        self.__on_target_fit(
                            row.ts_code, row.name, daily_close[0], ma_val, ma_delta)
                    # 由于获取日线数据的函数每分钟最多调用120次，所以，每次sleep 0.31秒，保证每分钟调用此函数不会超过200次
                    time.sleep(0.501)
                except QuantzException as e:
                    logw(str(e))
        else:
            logw('Empty stock list')
