from unittest import TestCase

from quantz.utils import *


class TestMiscUtils(TestCase):
    def test_date_2_str(self):
        today = datetime.datetime.today()
        print(date_2_str(today))
