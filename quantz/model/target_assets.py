from mongoengine import *

"""
Assets chosen by ma
"""


class MaTargetAsset(Document):
    """
    MA888 周线选股结果。
    """
    group_id = StringField(required=True)
    '''组ID'''
    code = StringField(required=True)
    '''股票代码'''
    name = StringField(required=True)
    '''股票名称'''
    close = FloatField(required=True)
    '''收盘价'''
    ma = FloatField(required=True)
    '''均线值'''
    ma_delta = FloatField(required=True)
    '''股价与均线之间差值的百分比'''


class MaTargetAssetGroup(Document):
    group_id = StringField(required=True)
    '''股票组'''
    when = DateTimeField(required=True)
    '''选股时间'''
    freq = StringField(required=True)
    '''频率'''
    period = IntField(required=True)
    '''周期'''
    threshold = IntField(required=True)
    '''选中的门限值'''
