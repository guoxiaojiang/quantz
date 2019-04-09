import multiprocessing as mp
from multiprocessing import Lock
from multiprocessing.managers import BaseManager
from unittest import TestCase


class Fits(object):
    def __init__(self):
        self.fits = []

    def add_1(self, one_fit):
        self.fits.append(one_fit)

    def get_fits(self):
        return self.fits


def add_1(fits: Fits, one: str, lock: Lock):
    print('add_1 %s' % one)
    with lock:
        fits.add_1(one)


class TestManager(BaseManager):
    pass


class MultiProcessTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_manager(self):
        """
        按照预期运行，有些麻烦，但是可以实现功能
        :return:
        """
        TestManager.register('Fits', Fits)
        lock = Lock()
        with TestManager() as manager:
            fits = manager.Fits()
            p1 = mp.Process(target=add_1, args=(fits, 'p1', lock))
            p2 = mp.Process(target=add_1, args=(fits, 'p2', lock))
            p3 = mp.Process(target=add_1, args=(fits, 'p3', lock))
            p1.start()
            p2.start()
            p3.start()
            p1.join()
            p2.join()
            p3.join()
            print('R %s' % fits.get_fits())

    def test_manager_with_pool(self):
        """
        未按预期运行，舍弃
        :return:
        """
        TestManager.register('Fits', Fits)
        lock = Lock()
        with TestManager() as manager:
            fits = manager.Fits()
            pool = mp.Pool()
            for i in range(12):
                pool.apply_async(func=add_1, args=(
                    fits, 'this is %s' % i, lock))
            pool.close()
            pool.join()
            print('R %s' % fits.get_fits())

    def test_multi_process(self):
        """
        未按预期运行，舍弃
        :return:
        """
        TestManager.register('Fits', Fits)
        m = TestManager()
        m.start()
        fits = m.Fits()
        lock = Lock()
        ctx = mp.get_context('fork')
        pool = ctx.Pool()
        for i in range(12):
            pool.apply_async(add_1, args=(fits, 'this is ' + str(i), lock))

        pool.close()
        pool.join()
        print('subprocess done %s' % fits.get_fits())

    def tearDown(self) -> None:
        pass
