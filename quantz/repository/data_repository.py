from quantz import Transaction

class TransactionRepo(object):
    """
    交易数据仓库，保存每笔交易的数据。
    """
    def get_last_transaction_of(self, code):
        """
        获取指定股票的最近一笔交易。
        :param code: 股票代码
        :return: 最后一笔交易
        """
        pass
