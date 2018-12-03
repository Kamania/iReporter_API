from flask import Flask, Blueprint
from flask_restful import Api, Resource
from instance.config import app_config
from .api.v1 import version_one as v1
from app.api.v1.url import routes

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])

    from app.api.v1 import version_one
    api = Api(version_one)
    app.register_blueprint(v1)

    routes(api)
    return app