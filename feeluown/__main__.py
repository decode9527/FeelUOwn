#! /usr/bin/env python3

import asyncio
import logging
import os
import traceback
import sys

sys.path.append(os.path.dirname(sys.path[0]))

from PyQt5.QtWidgets import QApplication
from quamash import QEventLoop

from feeluown import logger_config
from feeluown.app import App
from feeluown.rcfile import load_rcfile
from feeluown.consts import (HOME_DIR, USER_PLUGINS_DIR, PLUGINS_DIR, DATA_DIR,
                             CACHE_DIR, USER_THEMES_DIR, SONG_DIR)
from feeluown.config import config

logger = logging.getLogger(__name__)


def parse_args(args):
    if '-d' in args:
        config.debug = True
    logger_config()


def ensure_dir():
    if not os.path.exists(HOME_DIR):
        os.mkdir(HOME_DIR)
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    if not os.path.exists(USER_PLUGINS_DIR):
        os.mkdir(USER_PLUGINS_DIR)
    if not os.path.exists(CACHE_DIR):
        os.mkdir(CACHE_DIR)
    if not os.path.exists(USER_THEMES_DIR):
        os.mkdir(USER_THEMES_DIR)
    if not os.path.exists(SONG_DIR):
        os.mkdir(SONG_DIR)


def excepthook(exc_type, exc_value, tb):
    """Exception hook"""
    src_tb = tb
    while src_tb.tb_next:
        src_tb = src_tb.tb_next
    logger.error('Exception occured: print locals varibales')
    logger.error(src_tb.tb_frame.f_locals)
    traceback.print_exception(exc_type, exc_value, tb)


ensure_dir()
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.append(PLUGINS_DIR)
sys.path.append(USER_PLUGINS_DIR)


def main():
    sys.excepthook = excepthook
    parse_args(sys.argv)

    q_app = QApplication(sys.argv)
    q_app.setQuitOnLastWindowClosed(True)
    q_app.setApplicationName('FeelUOwn')

    app_event_loop = QEventLoop(q_app)
    asyncio.set_event_loop(app_event_loop)
    app = App()
    app.show()

    load_rcfile(app)

    app_event_loop.run_forever()
    sys.exit(0)


if __name__ == '__main__':
    main()
