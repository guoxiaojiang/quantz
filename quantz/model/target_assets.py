from mongoengine import *

"""
Assets chosen by ma
"""


class GrowingValueTargetAsset(Document):
    """
    高成长选股目标
    """
    group_id = StringField(required=True)
    '''组 id'''
    code = StringField(required=True)
    '''股票代码'''
    name = StringField(required=False)
    '''股票名字'''
    period = StringField(required=True)
    '''报告期，20181231表示2018年的年报'''
    or_yoy = FloatField(required=True)
    '''营业收入增长率'''
    grossprofit_margin = FloatField(required=True)
    '''毛利率'''
    profit_to_gr = FloatField(required=False)
    '''净利润率'''
    saleexp_to_gr = FloatField(required=False)
    '''销售费用比例'''
    adminexp_of_gr = FloatField(required=False)
    '''管理费用比例'''
    finaexp_of_gr = FloatField(required=False)
    '''财务费用比例'''
    rd_exp = FloatField(required=False)
    '''研发费用'''
    total_revenue = FloatField(required=True)
    '''总营业收入'''
    revenue = FloatField(required=True)
    '''营业收入'''


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
    params = StringField(required=True)


class MaTargetAssetGroup(Document):
    group_id = StringField(required=True)
    '''股票组'''
    when = DateTimeField(required=True)
    '''选股时间'''
    policy = StringField(required=False)
    '''选股策略，ma：均线选股，growing_value：成长价值'''
    params = StringField(required=False)
    '''选股的参数'''
