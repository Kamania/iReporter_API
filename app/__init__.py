from flask import Flask, Blueprint
# from flask_restful import Api, Resource
# from .db_config import create_tables
from instance.config import app_config
# To include local variables #
# from .api.v1.view import UserReportRedFlagList, UserReportRedFlag
from .api.v1 import version_one as v1

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # api = Api(app)
    app.config.from_object(app_config['development'])
    # create_tables()
    app.register_blueprint(v1)
    # api.add_resource(UserReportRedFlagList, '/report')
    # api.add_resource(UserReportRedFlag, '/report/<int:id>')
    return app