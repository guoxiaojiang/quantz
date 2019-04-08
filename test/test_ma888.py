from unittest import TestCase

import tushare as ts
from tushare.pro import client
import talib as ta
import numpy as np

from quantz.ma888 import Ma888
from quantz.utils.log import *

class TestMa888(TestCase):
    def setUp(self):
        log_init()
        self.ma888 = Ma888()

    def test_ma(self):
        close = self.ma888.get_weekly_close('000001.SZ', '20180101', '20190404')
        ma20 = self.ma888.ma(close=close, time_period=20)
        print(ma20)
        self.assertEqual(11.1215, ma20, 'Incorrect ma20')

    def test_get_weekly_close(self):
        pass

    def tearDown(self) -> None:
        pass
