#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import multiprocessing as mp
import os
import sys

import click
import pandas as pd
import tushare as ts

from quantz.growing_value_filter import GrowingValueFilter
from quantz.on_target_fit_listener import OnTargetFitListener
from quantz.quantz_exception import QuantzException
from quantz.repository.quantz_repository import QuanzRepo
from quantz.utils import miscutils, market_utils
from quantz.utils.log import *


class OnGrowingValueFitListener(OnTargetFitListener):

    def on_target_fit(self, target):
        logv('#############################')
        logv('On Fit\n%s' % (target))
        self.repo.put_target_asset(group_id=self.group_id, code=target['ts_code'], name=target['name'],
                                   params='or_yoy=%s grossprofit_margin=%s end_date=%s' %
                                   (target['or_yoy'], target['grossprofit_margin'], target['end_date']))

    def __init__(self, repo: QuanzRepo, when: datetime):
        if repo is None:
            raise QuantzException('Quant data repository must be specified')
        self.repo = repo
        self.group_id = str(when)


def growing_value_filter_func(stocks: pd.DataFrame, ts_token, when, or_yoy, rd_exp_min, rd_exp_max,
                              o_exp, gpr, end_date):
    logv('growing value filter or_yoy=%s rd_exp_min=%s rd_exp_max=%s o_exp=%s grp=%s end_date=%s'
         % (or_yoy, rd_exp_min, rd_exp_max, o_exp, gpr, end_date))
    growing_value_filter = GrowingValueFilter(miscutils.make_ts_api(ts_token),
                                              OnGrowingValueFitListener(
                                                  QuanzRepo(), when),
                                              or_yoy, rd_exp_min=rd_exp_min, rd_exp_max=rd_exp_max,
                                              o_exp=o_exp, gpr=gpr, end_date=end_date)
    growing_value_filter.filter_stocks(stocks)


@click.command()
@click.option('--ts_tokens', default='ts_token.py', type=click.STRING, help='Tushare token 配置文件')
@click.option('--or_yoy', default=30, type=click.FLOAT, help='营收增长率')
@click.option('--rd_exp_min', default=10, type=click.FLOAT, help='最低研发投入')
@click.option('--rd_exp_max', default=30, type=click.FLOAT, help='最高研发投入')
@click.option('--o_exp', default=20, type=click.FLOAT, help='研发外的三费比例')
@click.option('--gross_profit_rate', default=40, type=click.FLOAT, help='毛利率')
@click.option('--end_date', default=None, type=click.STRING, help='报告期')
def run(ts_tokens, rd_exp_min, rd_exp_max, or_yoy, o_exp, gross_profit_rate, end_date):
    log_init(0)
    logi('Growing Value picker running\nor_yoy=%d,rd_exp_min=%s rd_exp_max=%s o_exp=%s,gross_profit=%s end_date=%s\n'
         % (or_yoy, rd_exp_min, rd_exp_max, o_exp, gross_profit_rate, end_date))
    ts_token_list, tmp_token_list = miscutils.get_ts_token_list(ts_tokens)
    ts.set_token(ts_token_list[0])
    when = miscutils.today_datetime()
    try:
        worker_count = len(ts_token_list)
        stocks = market_utils.get_stock_list(
            miscutils.make_ts_api(tmp_token_list[0]))
        logi('%s stocks got' % stocks.shape[0])
        if stocks.shape[0] > 0:
            logd('%s worker process should be created here' %
                 (len(ts_token_list)))
        stocks_df_list = miscutils.spit_df(stocks, worker_count)
        process_list = []
        for i in range(worker_count):
            logv('Creating process %s' % i)
            p = mp.Process(target=growing_value_filter_func, args=(stocks_df_list[i], ts_token_list[i],
                                                                   when, or_yoy, rd_exp_min, rd_exp_max, o_exp,
                                                                   gross_profit_rate, end_date))
            process_list.append(p)
        for i in range(worker_count):
            process_list[i].start()
        for i in range(worker_count):
            process_list[i].join()
        repo = QuanzRepo()
        repo.put_group_id(when=when, policy='growing_value',
                          params='or_yoy=%s rd_exp_min=%s rd_exp_max=%s o_exp=%s gross_profit_rate=%s end_date=%s' % (
                              or_yoy, rd_exp_min, rd_exp_max, o_exp, gross_profit_rate, end_date))
        logi('JOB DONE!!!!!!')
    except QuantzException as e:
        loge('Something bad happened %s' % str(e))
    sys.exit(0)


if __name__ == '__main__':
    run()
