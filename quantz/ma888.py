"""
周线888级别选股
"""

import time

import numpy as np
import talib as ta
import tushare as ts
from tushare.pro import client

from quantz.quantz_exception import QuantzException
from quantz.utils import miscutils
from quantz.utils.log import *


class Ma888(object):
    def __init__(self, tushare_api):
        if not isinstance(tushare_api, (client.DataApi)):
            raise QuantzException('Wrong type of tushare_api, tushare.client.DataApi expected!!!')
        self.tushare_api = tushare_api
        self.result_list = []

    def get_weekly_close(self, ts_code, start_date, end_date):
        """
        获取日线级别收盘数据，最多重试10次。
        :param ts_code:股票代码，+.SZ/.SH
        :param start_date:
        :return: 收盘价的ndarray，如果获取失败，抛出异常
        """
        done = False
        count = 10
        daily_close = None
        while not done and count > 0:
            count = count - 1
            try:
                daily_close = ts.pro_bar(pro_api=self.tushare_api, ts_code=ts_code, start_date=start_date,
                                         end_date=end_date,
                                         asset='E', freq='W', adj='qfq')
                done = True
            except Exception as e:
                loge(str(e))
                done = False
                time.sleep(0.31)
                logi('Retrying get close price for ' + ts_code)
            finally:
                pass
        if daily_close is None:
            raise QuantzException('Failed to get bars for ' + ts_code)
        else:
            return daily_close['close'].values
            # return daily_close['close'].values[::-1] 倒序输出

    def ma(self, close, time_period):
        """
        获取N天移动均线，最简单的移动算术平均，取小数点后三位
        :param close: 收盘价ndarray
        :param time_period: 多久的均值
        :return: ma的ndarray
        """
        if close.shape[0] < time_period:
            raise QuantzException(
                'Ma' + str(time_period) + ' requires at least ' + str(time_period) + ' datas, but got ' + str(
                    close.shape[
                        0]))
        # 我们只需要最后一个交易日的ma数值用于对比，因此只计算这一个
        # talib 的 SMA 就是通达信的 MA，简单的算术平均值
        maN = ta.SMA(close[0:time_period], timeperiod=time_period)
        # 计算出的MA值是数组的最后一个，所以只返回最后一个值即可
        maN = maN[time_period - 1:]
        return np.round(maN, 4)

    def get_stock_list(self):
        return self.tushare_api.query('stock_basic', list_status='l', fields='ts_code,symbol,name,list_date')

    def add_stock(self, ts_code, name, close, ma888_val, ma888_delta):
        self.result_list.append((ts_code, name, close, ma888_val, ma888_delta))


def init_tushare():
    ts.set_token('4f34944e3ca4c1e2c10ab9c43a9f6a9d76b24479617330c95f9edaad')
    # 自定义连接超时时间
    return client.DataApi(token='4f34944e3ca4c1e2c10ab9c43a9f6a9d76b24479617330c95f9edaad', timeout=30)


def run():
    log_init()
    ma888 = Ma888(init_tushare())
    stocks = ma888.get_stock_list()
    logi(stocks.shape[0])
    if (stocks.shape[0] > 0):
        for row in stocks.itertuples():
            try:
                logi('Handling ' + row.ts_code + ' ' + row.name)
                daily_close = ma888.get_weekly_close(ts_code=row.ts_code, start_date=row.list_date,
                                                     end_date=miscutils.today())

                ma888_val = ma888.ma(close=daily_close, time_period=888)[0]
                # print('%s %s (Close:%s ma888:%s)' % (row.ts_code, row.name, daily_close[0], ma888_val))
                ma888_delta = (daily_close[0] - ma888_val) / daily_close[0]
                logi(row.name + ':' + str(ma888_delta))
                if abs(ma888_delta) <= 0.1:
                    logi('Add ' + row.name + ':' + str(ma888_delta))
                    ma888.add_stock(row.ts_code, row.name, daily_close[0], ma888_val, ma888_delta)
                # 由于获取日线数据的函数每分钟最多调用200次，所以，每次sleep 0.31秒，保证每分钟调用此函数不会超过200次
                time.sleep(0.301)
            except QuantzException as e:
                logi('Failed get ma888 for ' + row.name + ' cause:' + str(e))
    logi('Final Result:')
    logi(str(ma888.result_list))
    return 0


if __name__ == '__main__':
    sys.exit(run())
