# -*- encoding: utf-8 -*-

"""
Web app module.
"""

import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from flask.ext.restful import Api

from cwr_validator.config import DevConfig
from data_validator.accessor import CWRValidatorConfiguration
from cwr_validator.resources import UploadFileResource
from cwr_validator.service.cwr_parser import ThreadingCWRParserService
from cwr_validator.service.identifier import UUIDIdentifierService
from cwr_validator.service.data import MemoryDataStoreService

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


def _register_resources(api):
    api.add_resource(UploadFileResource, '/upload')


def _load_services(app, config):
    app.config['DATA_SERVICE'] = MemoryDataStoreService()
    app.config['ID_SERVICE'] = UUIDIdentifierService()
    app.config['FILE_SERVICE'] = ThreadingCWRParserService(
        config['upload.folder'],
        app.config['DATA_SERVICE'],
        app.config['ID_SERVICE'])


def create_app(config_object=DevConfig):
    config = CWRValidatorConfiguration().get_config()

    app = Flask(__name__)
    api = Api(app)

    app.config.from_object(config_object)

    _register_resources(api)
    _load_services(app, config)

    app.wsgi_app = ProxyFix(app.wsgi_app)

    if app.config['DEBUG']:
        log = config['log.folder']
        if len(log) == 0:
            log = 'mera_ws.log'

        handler = RotatingFileHandler(log, maxBytes=10000, backupCount=1)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(
            Formatter('[%(levelname)s][%(asctime)s] %(message)s'))

        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger('').addHandler(handler)

        app.logger.addHandler(handler)

    return app
