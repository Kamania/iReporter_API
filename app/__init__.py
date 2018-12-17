from flask import Flask, Blueprint
from flask_restful import Api, Resource
from instance.config import app_config, DevelopmentConfig
from .api.v1 import version_one as v1
from .api.v2 import version_two as v2
from app.api.v1.url import routes
from app.db_config import create_tables
from flask_jwt_extended import JWTManager

jwt = JWTManager()


def not_found(error):
    return "URL not found", 404


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.register_error_handler(404, not_found)
    app.url_map.strict_slashes = False
    app.config.from_object(DevelopmentConfig)
    jwt.init_app(app) 
    '''register'''
    app.register_blueprint(v1)
    app.register_blueprint(v2)
    create_tables()
    return app
