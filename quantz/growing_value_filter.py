#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time

import pandas as pd
from pandas import DataFrame
from tushare.pro import client

from quantz.quantz_exception import QuantzException
from quantz.utils.log import *
from quantz.utils import miscutils
from quantz.on_target_fit_listener import OnTargetFitListener

METHOD_INTERVAL = 0.74


class GrowingValueFilter(object):
    """
    价值成长。
    营业收入增长率：30-50, fina_indicator - >or_yoy
    研发投入比例：15-25，但不能低于10，不能高于30  fina_indicator->rd_exp / income->revenue
    扣除研发费用的三费（销售费用、管理费用、财务费用）费用比例控制在20%以内 fina_indicator->saleexp_to_gr adminexp_of_gr finaexp_of_gr
    毛利率：40以上 fina_indicator->grossprofit_margin
    毛利率>研发投入比例+扣除研发费的三费比例
    处于信息技术、物联网、芯片、5G、智能硬件、车载、医疗领域
    """

    def __init__(self, ts_api: client.DataApi, on_target_fit_listener:OnTargetFitListener,
                 or_yoy: float = 30, rd_exp_min: float = 10, rd_exp_max: float = 30,
                 o_exp: float = 20, gpr: float = 40, end_date: str = None):
        """
        :param or_yoy Operating Revenue Year over Year，营业收入增长率(非营业总收入)
        :param rd_exp R & D 研发投入比例最低值
        :param o_exp 三费总额比例
        :param gpr Gross Profit Rate, 毛利率
        """
        self.ts_api = ts_api
        if on_target_fit_listener is None:
            raise QuantzException('OnTargetFitListener must be specified')
        self.on_target_fit_listener = on_target_fit_listener
        self.or_yoy = or_yoy
        self.rd_exp_min = rd_exp_min
        self.rd_exp_max = rd_exp_max
        self.o_exp = o_exp
        self.gpr = gpr
        if miscutils.is_valid_report_end_date(end_date):
            self.end_date = end_date
        else:
            loge('Invalid report period,using last report period')
            self.end_date = miscutils.generate_latest_report_period()

    def __get_annual_report_at(self, ts_code):
        """
        Get data for filtering
        :param ts_code: stock number
        :param year: Year of Annual Report
        :return: DataFrame
        """
        count = 10
        # period = '%s1231' % year
        period = self.end_date
        fina = None
        income = None
        while count > 0 and fina is None:
            try:
                count = count - 1
                fina = self.ts_api.query('fina_indicator', ts_code=ts_code,
                                         period=period,
                                         fields='ts_code, end_date, or_yoy,'
                                                'roe_dt, grossprofit_margin, profit_to_gr, saleexp_to_gr,adminexp_of_gr,finaexp_of_gr,rd_exp')
            except Exception as e:
                loge('%s' % str(e))
                loge('Failing getting fina indicators for %s, retrying' % ts_code)
            if fina is None:
                time.sleep(METHOD_INTERVAL)
            else:
                # 有时年报财务数据会拿到两条一样的数据，只保留第一条既可
                fina = fina[0:1]
        count = 10
        while count > 0 and income is None:
            count = count - 1
            try:
                income = self.ts_api.query('income', ts_code=ts_code,
                                           period=period,
                                           fields='ts_code, total_revenue, revenue')
            except Exception as e:
                loge('%s' % str(e))
                loge('Failing getting incomes for %s, retrying' % ts_code)
            if income is None:
                time.sleep(METHOD_INTERVAL)
            else:
                # 有时年报收入数据会拿到两条一样的数据，只保留第一条既可
                income = income[0:1]
        if fina is None or income is None or fina.empty:
            raise QuantzException('Failed to get annual report for %s @%s' % (ts_code, period))
        if fina.shape[0] == 1 and income.shape[0] == 1:
            report = fina.merge(income)
            logi('Got report for %s' % ts_code)
            return report.iloc[0]
        else:
            loge('Got Invalid report data')
            raise QuantzException('Invalid report got for %s @%s' % (ts_code, period))

    def __is_stock_data_valid(self, annual_report):
        if annual_report is None or annual_report.empty:
            return False
        if annual_report['saleexp_to_gr'] is not None \
                and annual_report['adminexp_of_gr'] is not None \
                and annual_report['finaexp_of_gr'] is not None \
                and annual_report['rd_exp'] is not None \
                and annual_report['total_revenue'] is not None \
                and annual_report['or_yoy'] is not None:
            return True
        return False

    def __filter_stock(self, stock):
        """
        :param stock: named tuple of stock
        :return:
        """
        try:
            report = self.__get_annual_report_at(stock.ts_code)
            name = pd.Series(index=['name'], data=[stock.name])
            end_date = pd.Series(index=['end_date'], data=[self.end_date])
            report = report.append(name)
            report = report.append(end_date)
            # logv('Annual Report:\n%s\n' % report)
            if not self.__is_stock_data_valid(report):
                logi('Invalid annual report data of %s' % stock.name)
                return
            o_exp_of_gr = report['saleexp_to_gr'] + report['adminexp_of_gr'] + report['finaexp_of_gr']
            rd_exp_of_gr = 100 * report['rd_exp'] / report['total_revenue']
            logv('or_yoy=%s rd_exp_of_gr=%s o_exp_of_gr=%s grossprofit=%s' % \
                 (report['or_yoy'], rd_exp_of_gr, o_exp_of_gr, report['grossprofit_margin']))
            if report['or_yoy'] < self.or_yoy:
                logi('%s not qualified, or_yoy(营业收入增速) %s < %s' % (report['ts_code'], report['or_yoy'], self.or_yoy))
                return
            if rd_exp_of_gr < self.rd_exp_min or rd_exp_of_gr > self.rd_exp_max:
                logi('%s not qualified, rd_exp(研发投入) %s not between(%s %s)' % (report['ts_code'], rd_exp_of_gr, self.rd_exp_min, self.rd_exp_max))
                return
            if o_exp_of_gr > self.o_exp:
                logi('%s not qualified, o_exp(三费总和) %s > %s' % (report['ts_code'], o_exp_of_gr, self.o_exp))
                return
            if report['grossprofit_margin'] < self.gpr:
                logi('%s not qualified, grossprofit(毛利率) %s < %s' % (report['ts_code'], report['grossprofit_margin'], self.gpr))
                return
            if o_exp_of_gr + rd_exp_of_gr > report['grossprofit_margin']:
                logi('%s not qualified, 三费+研发投入(%s) > 毛利率(%s)' % (report['ts_code'], (o_exp_of_gr+rd_exp_of_gr), report['grossprofit_margin']))
                return
            # if report['or_yoy'] >= self.or_yoy \
            #         and rd_exp_of_gr >= self.rd_exp_min and rd_exp_of_gr <= self.rd_exp_max \
            #         and o_exp_of_gr <= self.o_exp \
            #         and report['grossprofit_margin'] >= self.gpr \
            #         and o_exp_of_gr + rd_exp_of_gr <= report['grossprofit_margin']:
            logi('###########################################')
            logi('Got one %s' % report)
            logi('###########################################')
            self.on_target_fit_listener.on_target_fit(report)
        except QuantzException as e:
            loge('Error getting annual for %s:%s' % (stock.name, e))

    def filter_stocks(self, stocks: DataFrame):
        if stocks is not None and stocks.shape[0] > 0:
            for stock in stocks.itertuples():
                self.__filter_stock(stock)
                # 每分钟最多调用接口80次 6/8 = 0.75
                time.sleep(METHOD_INTERVAL)
            logi('Filter %d done' % os.getpid())
