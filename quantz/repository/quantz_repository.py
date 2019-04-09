from datetime import date

import mongoengine as mongo

from quantz.model.target_assets import MaTargetAsset, MaTargetAssetGroup


class QuanzRepo(object):
    """
    数据仓库，保存所有数据。
    """

    def __init__(self, db='quantz', host='localhost', port=27017):
        mongo.connect(db=db, host=host, port=port, connect=False)

    def get_last_transaction_of(self, code):
        """
        获取指定股票的最近一笔交易。
        :param code: 股票代码
        :return: 最后一笔交易
        """
        pass

    @staticmethod
    def put_group_id(when: date, freq, period, threshold):
        """
        将股票的group id存入数据库
        :param when:
        :return:
        """
        MaTargetAssetGroup(group_id=str(when), when=when, freq=freq, period=period, threshold=threshold).save()

    @staticmethod
    def put_ma_target_asset(group_id: str, code: str,
                            name: str, close: float, ma: float, ma_delta: float):
        """
        保存选中的股票到数据库。
        :param group_id: 组id
        :param code: 选中的股票代码+.SH/SZ
        :param name: 选中的股票名字
        :param close: 收盘价
        :param ma: 均线位置
        :param ma_delta: 收盘价与均线差值的百分比
        :return: None
        """
        MaTargetAsset(group_id=group_id, code=code, name=name, close=close, ma=ma, ma_delta=ma_delta).save()

    @staticmethod
    def get_target_assets_by_group(group_id: str):
        return MaTargetAsset.objects(group_id=group_id)
