# -*- coding: utf-8 -*-

from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool
import asyncio
import itertools
import fire
import logging
# import random
import time


from aio_pool import AsyncIOPool
from benchmark import Benchmark
from logger import get_logger


class Test:
    def __init__(self, sleep, workers, log_level):
        self.sleep = sleep
        self.workers = workers
        self.logger = get_logger(__name__, log_level)

    async def async_sleep(self, x):
        await asyncio.sleep(self.sleep)
        # await asyncio.sleep(random.randint(1, 10))
        return x * 2

    @staticmethod
    def time_sleep(x, sleep):
        time.sleep(sleep)
        return x * 2

    def async_map(self, loop, sample):
        with Benchmark('coroutine map benchmark', self.logger):
            results = []
            _pool = AsyncIOPool(loop=loop, workers=self.workers, timeout=self.sleep + 0.1)
            for item in _pool.map(self.async_sleep, sample):
                results.append(item)
        self.logger.debug(sorted(results, key=lambda x: x[0]))

    def thread_map(self, sample):
        with Benchmark('thread map benchmark', self.logger):
            thread_pool = ThreadPool(self.workers)
            results = thread_pool.starmap(self.time_sleep, zip(sample, itertools.repeat(self.sleep, len(sample))))
            thread_pool.close()
            thread_pool.join()
        self.logger.debug(results)

    def process_map(self, sample):
        with Benchmark('process map benchmark', self.logger):
            process_pool = ProcessPool(self.workers)
            results = process_pool.starmap(self.time_sleep, zip(sample, itertools.repeat(self.sleep, len(sample))))
            process_pool.close()
            process_pool.join()
        self.logger.debug(results)


def main(sleep, sample, workers, log_level=logging.INFO):
    _loop = asyncio.get_event_loop()

    print('{0}    sleep: {1}, sample: {2}, works: {3}    {0}'.format('-' * 30, sleep, sample, workers))

    _sample = range(sample)

    test = Test(sleep=sleep, workers=workers, log_level=log_level)

    test.async_map(_loop, _sample)
    test.thread_map(_sample)
    test.process_map(_sample)

    _loop.close()

if __name__ == '__main__':
    # env/bin/python test_aio_pool.py --sleep SLEEP --sample SAMPLE --workers WORKERS [--log-level LOG_LEVEL]
    # env/bin/python test_aio_pool.py --sleep 0.1 --sample 100 --workers 10
    # env/bin/python test_aio_pool.py --sleep 1 --sample 1000 --workers 100
    # env/bin/python test_aio_pool.py --sleep 10 --sample 10000 --workers 1000
    fire.Fire(main)
