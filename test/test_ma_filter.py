from unittest import TestCase

from tushare.pro import client

from quantz.ma_filter import MaFilter, OnTargetFitListener
from quantz.utils.log import *


class TestOnTargetFitListener(OnTargetFitListener):

    def on_target_fit(self, target):
        return logi('%s fits' % target)


class TestMa888(TestCase):
    def setUp(self):
        log_init()
        sys.path.extend(['/Users/yuz/data'])
        import ts_token
        ts_api = client.DataApi(
            token=ts_token.ts_token_list[0], timeout=30)
        self.on_target_fit_listener = TestOnTargetFitListener()
        self.ma_filter = MaFilter(
            ts_api, self.on_target_fit_listener, freq='W', time_period=20, threshold=10)

    def test_ma(self):
        close = self.ma_filter._MaFilter__get_close(
            '000001.SZ', '20180101', '20190404')
        ma20 = self.ma_filter._MaFilter__ma(close=close)
        print(ma20)
        self.assertEqual(11.1215, ma20, 'Incorrect ma20')

    def test_get_weekly_close(self):
        pass

    def tearDown(self) -> None:
        pass
