import datetime

def date_2_str(when):
    """
    date 对象转换为字符串"YYYYMMDD"形式
    :param when: 需要转换的时间，必须是 date,datetime 或 time 类型的参数
    :return:
    """
    if isinstance(when, (datetime.datetime, datetime.date, datetime.time)):
        return when.strftime('%Y%m%d')
    else:
        raise Exception('when must be one of date,datetime or time')

def today():
    return date_2_str(datetime.datetime.today())