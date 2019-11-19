from unittest import TestCase
import datetime
from datetime import timedelta


class FreeTest(TestCase):
    def test_time_period(self):
        """
        根据当前日期生成最近的报表季时间
        """
        now = datetime.datetime.now()
        month = (now.month - 1) - (now.month - 1) % 3 + 1
        last_quarter_end = datetime.datetime(
            now.year, month, 1) - timedelta(days=1)
        print(last_quarter_end.strftime("%Y%m%d"))
        print(str(last_quarter_end))
