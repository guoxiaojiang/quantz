from unittest import TestCase

from quantz.ma_filter_main import get_ts_token_list

class MaFilterMainTest(TestCase):
    def test_get_ts_token_list(self):
        for l in get_ts_token_list('/Users/yuz/data/ts_token.py'):
            print(l)
