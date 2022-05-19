import logging
import yaml

with open('log.yaml', 'r') as f:
    config = yaml.safe_load(f)

logging.config.dictConfig(config)
log = logging.getLogger('simple')
