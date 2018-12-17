from .views import UserReportRedFlagList, UserReportRedFlag, Patch_location
from .views import Patch_comment
from flask import Blueprint
from flask_restful import Api

version_one = Blueprint('v1', __name__, url_prefix="/api/v1")
api = Api(version_one)
api.add_resource(UserReportRedFlagList, '/records')
api.add_resource(UserReportRedFlag, '/records/<id>')
api.add_resource(Patch_location, '/records/<id>/location')
api.add_resource(Patch_comment, '/records/<id>/comment')