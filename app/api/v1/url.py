from . import UserReportRedFlag, UserReportRedFlagList, version_one
from flask_restful import Api, Resource
from .views import Patch_location, Patch_comment


def routes(api):
    """Add api endpoints"""
    api.add_resource(UserReportRedFlagList, '/records')
    api.add_resource(UserReportRedFlag, '/records/<id>')
    api.add_resource(Patch_location, '/records/<id>/location')
    api.add_resource(Patch_comment, '/records/<id>/comment')

    return None
