from mongoengine import *


class Transaction(Document):
    """ 交割记录 """
    # 成交时间
    time = DateTimeField(required=True)
    # 股票名称
    name = StringField(required=False)
    # 买卖方向,(1 卖出，-1 买入)
    direction = IntField(required=True)
    # 成交数量
    volume = IntField(required=True)
    # 成交单价
    price = FloatField(required=True)
    # 成交金额
    turnover = FloatField(required=True)
    # 股票代码
    code = StringField(required=True)
    # 手续费
    service_charge = FloatField(required=True)
    # 印花税
    stamp_tax = FloatField(default=0)
    # 其他费用
    misc_charge = FloatField(default=0)
    # 发生金额
    actual_amount = FloatField(required=True)
