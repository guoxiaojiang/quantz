from unittest import TestCase

from quantz import utils


class TestLog(TestCase):
    def test_log(self):
        utils.log_init()
        utils.logd('DEBUG %s %s' % ('this', 'is debug'))
        utils.logw('WARNING %s' % 'this is warning')
        utils.logi('INFO')
        utils.loge('ERROR %s' % 'ERROR NOW')
