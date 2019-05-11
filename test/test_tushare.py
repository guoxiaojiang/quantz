from unittest import TestCase

from tushare.pro import client

from quantz.utils import miscutils


class TushareTest(TestCase):
    def setUp(self) -> None:
        ts_token = miscutils.get_ts_token_from_env()
        if ts_token is not None:
            self.ts_api = client.DataApi(token=ts_token, timeout=10)
        else:
            self.fail('TS_TOKEN not specified')

    def test_fina_indicator(self):
        ts_code = '300122.SZ'
        start_date = '20180101'
        end_date = '20181231'
        period = '20181231'
        fina = self.ts_api.query('fina_indicator', ts_code=ts_code,  # start_date=start_date, end_date=end_date,
                                 period=period,
                                 fields='ts_code, end_date, or_yoy, roe_dt, grossprofit_margin, saleexp_to_gr,adminexp_of_gr,finaexp_of_gr,rd_exp')
        for row in fina.itertuples():
            print(row)

        income = self.ts_api.query('income', ts_code=ts_code,  # start_date=start_date, end_date=end_date,
                                   period=period,
                                   fields='ts_code, end_date, total_revenue, revenue')
        for row in income.itertuples():
            print(row)

        result = fina.set_index('end_date').merge(income, how='left', left_index=True, right_index=True)
        for row in result.itertuples():
            print(row)

    def tearDown(self) -> None:
        pass
