from app.api.v1.view import UserReportRedFlagList, UserReportRedFlag
from flask_restful import Api, Resource
from flask import Blueprint

version_one = Blueprint('v1', __name__, url_prefix="/api/v1")

api = Api(version_one)
api.add_resource(UserReportRedFlagList, '/red_flag_records')
api.add_resource(UserReportRedFlag, '/red_flag_record/<int:id>')