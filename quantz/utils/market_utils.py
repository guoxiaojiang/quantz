# -*- coding: utf-8 -*-


def get_stock_list(tushare_api, fields='ts_code,symbol,name,list_date'):
    return tushare_api.query('stock_basic', list_status='l', fields=fields)
