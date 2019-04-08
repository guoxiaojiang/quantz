import sys
from datetime import datetime

def log_init():
    pass

def logd(*msg):
    print(datetime.now().strftime('%Y%m%d-%H%M%S.%f') + 'D:%s' % msg)


def logi(*msg):
    print(datetime.now().strftime('%Y%m%d-%H%M%S.%f') + 'I:%s' % msg)


def logw(*msg):
    print(datetime.now().strftime('%Y%m%d-%H%M%S.%f') + 'W:%s' % msg)


def loge(*msg):
    print(datetime.now().strftime('%Y%m%d-%H%M%S.%f') + 'E:%s' % msg, file=sys.stderr)
