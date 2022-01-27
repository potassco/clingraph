#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Custom Logger."""

import sys
import logging


class SingleLevelFilter(logging.Filter):
    """Filter levels"""

    def __init__(self, passlevel, reject):
        # pylint: disable=super-init-not-called
        self.passlevel = passlevel
        self.reject = reject

    def filter(self, record):
        if self.reject:
            return record.levelno != self.passlevel

        return record.levelno == self.passlevel


GREY = '\033[90m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
NORMAL = '\033[0m'


def setup_logger(level=logging.INFO):
    """Logger setup."""

    logger = logging.getLogger('custom')
    logger.propagate = False
    logger.setLevel(level)
    # log_message_str = "{}%(levelname)s:{} %(filename)s:%(funcName)s:%(lineno)d - %(message)s{}"
    log_message_str = "{}%(levelname)s:{}  - %(message)s{}"
    # INFO stream handler
    info_sh = logging.StreamHandler(sys.stderr)
    info_sh.addFilter(SingleLevelFilter(logging.INFO, False))
    info_sh.setLevel(logging.INFO)
    formatter = logging.Formatter(
        log_message_str.format(GREEN, GREY, NORMAL))
    info_sh.setFormatter(formatter)
    logger.addHandler(info_sh)

    # WARNING stream handleer
    warn_sh = logging.StreamHandler(sys.stderr)
    warn_sh.addFilter(SingleLevelFilter(logging.WARNING, False))
    warn_sh.setLevel(logging.WARN)
    formatter = logging.Formatter(
        log_message_str.format(YELLOW, GREY, NORMAL))
    warn_sh.setFormatter(formatter)
    logger.addHandler(warn_sh)

    # DEBUG stream handler
    debug_sh = logging.StreamHandler(sys.stderr)
    debug_sh.addFilter(SingleLevelFilter(logging.DEBUG, False))
    debug_sh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        log_message_str.format(BLUE, GREY, NORMAL))
    debug_sh.setFormatter(formatter)
    logger.addHandler(debug_sh)

    # ERROR stream handler
    error_sh = logging.StreamHandler(sys.stderr)
    error_sh.addFilter(SingleLevelFilter(logging.ERROR, False))
    error_sh.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        log_message_str.format(RED, GREY, NORMAL))
    error_sh.setFormatter(formatter)
    logger.addHandler(error_sh)
