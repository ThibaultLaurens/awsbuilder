#!/usr/bin/env python

import os
import logging
import yaml

from lib.build_router import Build_Router

if __name__ == '__main__':

    env = os.getenv('PY_ENV', 'development')                        # set 'development' as default value

    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", filename='worker.log',
                        datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    logging.getLogger('pika').setLevel(logging.CRITICAL)
    logging.getLogger('boto').setLevel(logging.CRITICAL)
    if env == 'development':
        logging.getLogger().addHandler(logging.StreamHandler())     # print logging messages to the console
    logging.info('logger configured')

    config = yaml.load(open('config.yaml').read())
    config = config[env]                                            # env = [development | production]

    router = Build_Router(config)
    router.build()


