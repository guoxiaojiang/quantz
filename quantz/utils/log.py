import sys
from datetime import datetime

LEVEL_V: int = 0
LEVEL_D: int = 1
LEVEL_I: int = 2
LEVEL_W: int = 3
LEVEL_E: int = 4
" 无任何log输出 "
LEVEL_N: int = 5

__log_level__ = LEVEL_I


def log_init(level=LEVEL_I):
    # 函数内修改外部变量，生命这是一个外部的全局变量，否则，Python 会声明一个同名的本地变量，对其做的修改不会影响外部的变量值
    global __log_level__
    __log_level__ = level


def logv(*msg):
    if __log_level__ <= LEVEL_V:
        print(datetime.now().strftime('%Y%m%d-%H%M%S.%f') + 'V:%s' % msg)


def logd(*msg):
    if __log_level__ <= LEVEL_D:
        print(datetime.now().strftime('%Y%m%d-%H%M%S.%f') + 'D:%s' % msg)


def logi(*msg):
    if __log_level__ <= LEVEL_I:
        print(datetime.now().strftime('%Y%m%d-%H%M%S.%f') + 'I:%s' % msg)


def logw(*msg):
    if __log_level__ <= LEVEL_W:
        print(datetime.now().strftime('%Y%m%d-%H%M%S.%f') + 'W:%s' % msg)


def loge(*msg):
    if __log_level__ <= LEVEL_E:
        print(datetime.now().strftime('%Y%m%d-%H%M%S.%f') + 'E:%s' %
              msg, file=sys.stderr)
