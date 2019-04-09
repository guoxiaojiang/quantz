from unittest import TestCase

from quantz import utils


class TestLog(TestCase):
    def test_log(self):
        utils.log_init(level=utils.LEVEL_V)
        utils.logv('VERBOSE MSG')
        utils.logd('DEBUG %s %s' % ('this', 'is debug'))
        utils.logi('INFO')
        utils.logw('WARNING %s' % 'this is warning')
        utils.loge('ERROR %s' % 'ERROR NOW')
