#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import multiprocessing as mp
import os

import click
import pandas as pd
import tushare as ts

from quantz.ma_filter import MaFilter
from quantz.on_target_fit_listener import OnTargetFitListener
from quantz.model.target_assets import MaTargetAsset
from quantz.quantz_exception import QuantzException
from quantz.repository.quantz_repository import QuanzRepo
from quantz.utils import market_utils
from quantz.utils import miscutils
from quantz.utils.log import *


class MaOnTargetFitListener(OnTargetFitListener):
    def __init__(self, repo: QuanzRepo, when: datetime):
        self.repo = repo
        self.group_id = str(when)

    def on_target_fit(self, target):
        logi('Got one fit %s' % target)
        self.repo.put_target_asset(self.group_id, target[0], target[1],
                                      'close=%s ma=%s ma_delta=%s' % (target[2], target[3], target[4]))


def ma_filter_func(stocks: pd.DataFrame, ts_token: str, when: datetime, freq='W', time_period=888, threshold=5):
    """
    在新进程中启动功能。
    :param stocks: 待选
    :param ts_token: tushare token
    :param when: 选股开始时间，座位本次选择的group id
    :return: 无
    """
    logv('ma_filter_func %s ts_token=%s freq=%s period=%s threshold=%s' % (
        os.getpid(), ts_token, freq, time_period, threshold))
    ma_filter = MaFilter(miscutils.make_ts_api(ts_token), MaOnTargetFitListener(QuanzRepo(), when), freq=freq,
                         time_period=time_period, threshold=threshold)
    ma_filter.filter_stocks(stocks)


def output_assets(assets: [MaTargetAsset]):
    for asset in assets:
        print('%s %s %s %s' % (asset.group_id, asset.code, asset.name, asset.params))


@click.command()
@click.option('--freq', default='W', type=click.STRING, help='均线周期，默认使用周线选股，1min表示1分钟（支持1/5/15/30/60分钟） D日线，W周线，默认W')
@click.option('--period', default=888, type=click.INT, help='选股周期，默认按照888周均线选股,比如 --period 20 按照20周均线选股')
@click.option('--threshold', default=10, type=click.INT, help='门限，当前股价与均线之间相差百分比在门限之内的股票被选中，默认10，既均线与股价相差百分之五之内的股票被选中')
@click.option('--ts_tokens', default='ts_token.py', type=click.STRING,
              help='tushare token 列表文件，其中要包含 ts_token_list、tmp_ts_token_list两个tuple')
def run(freq, period, threshold, ts_tokens):
    """
    简单的均线选股小程序。
    """
    log_init(0)
    logi('ma filter running(freq=%s,period=%s,threshold=%s,ts_tokens=%s)' % (freq, period, threshold, ts_tokens))
    ts_token_list, tmp_token_list = miscutils.get_ts_token_list(ts_tokens)
    ts.set_token(tmp_token_list[0])
    when = miscutils.today_datetime()
    try:
        worker_count = len(ts_token_list)
        stocks = market_utils.get_stock_list(miscutils.make_ts_api(tmp_token_list[0]))
        logv('%s stocks got' % stocks.shape[0])
        if stocks.shape[0] > 0:
            logd('%s worker process should be created here' % (len(ts_token_list)))
        stocks_df_list = miscutils.spit_df(stocks, worker_count)
        # 多线程
        process_list = []
        for i in range(worker_count):
            logv('Create process %s' % i)
            p = mp.Process(target=ma_filter_func,
                           args=(stocks_df_list[i], ts_token_list[i], when, freq, period, threshold))
            process_list.append(p)
        for i in range(worker_count):
            process_list[i].start()
        for i in range(worker_count):
            process_list[i].join()
        repo = QuanzRepo()
        repo.put_group_id(when, policy='ma', params='freq=%s period=%s threshold=%s' % (freq, period, threshold))
        output_assets(repo.get_target_assets_by_group(group_id=str(when)))
    except QuantzException as e:
        loge('Bad things happened %s' % str(e))
    sys.exit(0)


if __name__ == '__main__':
    run()
