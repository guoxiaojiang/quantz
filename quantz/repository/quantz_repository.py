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
    def put_group_id(when: date, policy='undefined', params='undefined'):
        """
        将股票的group id存入数据库
        :param when:
        :return:
        """
        MaTargetAssetGroup(group_id=str(when), when=when,
                           policy=policy, params=params).save()

    @staticmethod
    def put_target_asset(group_id: str = 'undefined', code: str = 'undefined',
                         name: str = 'undefined', params: str = 'undefined'):
        """
        保存选中的股票到数据库。
        :param group_id: 组id
        :param code: 选中的股票代码+.SH/SZ
        :param name: 选中的股票名字
        :param params: 选股的参数值
        :return: None
        """
        MaTargetAsset(group_id=group_id, code=code,
                      name=name, params=params).save()

    @staticmethod
    def get_target_assets_by_group(group_id: str):
        return MaTargetAsset.objects(group_id=group_id)
