from .views.record_views import UserReportRedFlag, UserReportRedFlagList
from .views.record_views import Patch_comment, Patch_location, Patch_status
from flask import Blueprint
from flask_restful import Api
from .views.user_views import Register, UserLogin


version_two = Blueprint('v2', __name__, url_prefix='/api/v2')
api = Api(version_two)
api.add_resource(UserReportRedFlagList, '/records')
api.add_resource(UserReportRedFlag, '/records/<id>')
api.add_resource(Patch_location, '/records/<id>/location')
api.add_resource(Patch_comment, '/records/<id>/comment')

api.add_resource(Register, '/auth/signup')
api.add_resource(UserLogin, '/auth/login')

api.add_resource(Patch_status, '/records/<id>/status')
