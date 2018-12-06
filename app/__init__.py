from flask import Flask, Blueprint
from flask_restful import Api, Resource
from instance.config import app_config
from .api.v1 import version_one as v1
from app.api.v1.url import routes


def not_found(error):
    return "URL not found", 404


def create_app():
    app = Flask(__name__, instance_relative_config=True)
ch-update-files-162490007
    app.register_error_handler(404, not_found)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config['development'])
    api = Api(v1)
    '''register'''
    app.register_blueprint(v1)
    routes(api)
    return app
