# -*- coding: utf-8 -*-

import time


class Benchmark:
    def __init__(self, name, logger):
        self.name = name
        self.logger = logger

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, ty, val, tb):
        self.logger.info('{}: {:.3f} seconds'.format(self.name, time.time() - self.start))
        return False
