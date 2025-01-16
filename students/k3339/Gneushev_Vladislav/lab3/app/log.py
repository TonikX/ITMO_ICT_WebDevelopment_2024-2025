import logging
import sys


def setup_logging():
    logging.basicConfig(
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{",
        format=("{asctime} [{levelname:.1}] [{name:^16}] {message}"),
    )
