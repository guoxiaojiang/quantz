import sys
from datetime import datetime
from unittest import TestCase

import numpy as np
import talib as ta
import tushare as ts
from tushare.pro import client


class TalibTest(TestCase):
    """
    确定talib的SMA函数等于A股的MA
    """

    def setUp(self):
        sys.path.extend(['/Users/yuz/data'])
        import ts_token
        token = ts_token.ts_token_list[0]
        ts.set_token(token)
        # 自定义连接超时时间
        self.pro = client.DataApi(token=token, timeout=30)

    def test_ma(self):
        pingan_daily = self.pro.query('daily', ts_code='000001.SZ', start_date='20190101',
                                      end_date='', fields='ts_code, trade_date, close')
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
