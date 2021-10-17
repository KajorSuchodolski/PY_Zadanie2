import logging


def xd():
    print('dupa')


def umu():
    log = logging.getLogger(__name__)
    log.setLevel(level='DEBUG')
    log.warning('test')
    xd()
    return 0


def log_config(level):
    with open('chase.log') as f_log:
        log = logging.getLogger(__name__)
        log.add

umu()

