import logging
import yaml


def getLogger():
    '''로거 생성'''
    with open('log.yaml', 'r') as f:
        config = yaml.safe_load(f)

    logging.config.dictConfig(config)
    log = logging.getLogger('simple')

    return log
