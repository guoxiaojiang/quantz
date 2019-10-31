from unittest import TestCase

from quantz.utils import *


class TestMiscUtils(TestCase):
    def test_date_2_str(self):
        today = datetime.datetime.today()
        print(date_2_str(today))

    def test_today_date(self):
        print(today_datetime())

    def test_generate_last_season(self):
        print(generate_latest_report_period())

    def test_is_valid_report_end_date(self):
        print(is_valid_report_end_date('20200331'))
        print(is_valid_report_end_date('20000330'))
        print(is_valid_report_end_date('20000731'))
        print(is_valid_report_end_date('20000330'))
        print(is_valid_report_end_date('20000330'))
        print(is_valid_report_end_date('19990331'))
        print(is_valid_report_end_date('20190630'))
        print(is_valid_report_end_date('20190930'))
        print(is_valid_report_end_date('19981231'))
