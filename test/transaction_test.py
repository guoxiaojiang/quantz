import datetime
import unittest

import rom

from quantz import Transaction


class TransactionTest(unittest.TestCase):
    def setUp(self):
        rom.util.set_connection_settings(host='localhost')

    def testCrud(self):
        t = Transaction(time=datetime.datetime.now(), name='中科创达', direction=1,
                        volume=200, price=34.83, turnover=6966, code='000001', service_charge=10.95,
                        stamp_tax=10, misc_charge=20, actual_amount=7000)
        t.save(full=True, force=True)
        print('Transaction saved')
        ret = Transaction.query.all()
        print('All transactions got')
        for x in ret:
            print('%s %s %f' % (x.code, x.name, x.price))
        Transaction.query.filter().delete()

    def tearDown(self):
        pass
