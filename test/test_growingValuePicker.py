from unittest import TestCase
from quantz.growing_value_filter import GrowingValueFilter
from quantz.on_target_fit_listener import OnTargetFitListener
from quantz.repository.quantz_repository import QuanzRepo
from quantz.utils.log import *

from quantz.utils import miscutils, market_utils
from tushare.pro import client


class OnGrowingValueFitListener(OnTargetFitListener):

    def on_target_fit(self, target):
        logv('on fit\n%s' % target)
        self.repo.put_target_asset(group_id=self.group_id,
                                   code=target['ts_code'])

    def __init__(self, repo: QuanzRepo, when: datetime):
        self.repo = repo
        self.group_id = str(when)


class GrowingValuePickerTest(TestCase):

    def setUp(self) -> None:
        log_init(0)
        self.ts_api = client.DataApi(miscutils.get_ts_token_from_env())
        self.picker = GrowingValueFilter(self.ts_api, OnGrowingValueFitListener(QuanzRepo(), datetime.now()),
                                         or_yoy=10, rd_exp_min=1, rd_exp_max=30, o_exp=80, gpr=10)

    def test_get_annual_report_at(self):
        report = self.picker._GrowingValuePicker__get_annual_report_at(
            '300122.SZ', 2018)
        logi(report)

    def test_filter_stock(self):
        self.picker._GrowingValueFilter__filter_stock('300122.SZ')
        pass

    def test_filter_stocks(self):
        self.picker.filter_stocks(market_utils.get_stock_list(self.ts_api))
        pass

    def tearDown(self) -> None:
        pass
