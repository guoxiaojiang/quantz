import rom


class Transaction(rom.Model):
    """ 交割记录 """
    # 成交时间
    time = rom.DateTime(required = True)
    # 股票名称
    name = rom.Text(required=False)
    # 买卖方向,(1 卖出，-1 买入)
    direction = rom.Integer(required=True)
    # 成交数量
    volume = rom.Integer(required=True)
    # 成交单价
    price = rom.Float(required=True)
    # 成交金额
    turnover = rom.Float(required=True)
    # 股票代码
    code = rom.Text(required=True)
    # 手续费
    service_charge = rom.Float(required=True)
    # 印花税
    stamp_tax = rom.Float(default=0)
    # 其他费用
    misc_charge = rom.Float(default=0)
    # 发生金额
    actual_amount = rom.Float(required=True)
