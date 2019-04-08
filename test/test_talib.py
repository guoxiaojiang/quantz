from unittest import TestCase

import tushare as ts
from tushare.pro import client
import talib as ta
import numpy as np
from datetime import datetime


class TalibTest(TestCase):
    """
    确定talib的SMA函数等于A股的MA
    """
    def setUp(self):
        ts.set_token('4f34944e3ca4c1e2c10ab9c43a9f6a9d76b24479617330c95f9edaad')
        # 自定义连接超时时间
        self.pro = client.DataApi(token='4f34944e3ca4c1e2c10ab9c43a9f6a9d76b24479617330c95f9edaad', timeout=30)

    def test_ma(self):
        pingan_daily = self.pro.query('daily', ts_code='000001.SZ', start_date='20190101',
                                      end_date='' ,fields='ts_code, trade_date, close')
        print('平安银行日线数据:%s' % pingan_daily['close'].values)
        sma20 = ta.SMA(pingan_daily['close'].values, timeperiod=20)
        print('shape:%s' % sma20.shape)
        sma20 = sma20[19:]
        sma20 = np.round(sma20, 3)
        print(sma20)

    def test_date(self):
        print(datetime.today().strftime('%Y%m%d'))

    def tearDown(self):
        pass
