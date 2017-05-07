# -*- coding: utf-8 -*-

import logging


def get_logger(name, level=logging.INFO, handler=logging.StreamHandler()):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
