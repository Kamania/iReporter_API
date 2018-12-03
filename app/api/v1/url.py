from . import Register,UserReportRedFlag,UserReportRedFlagList,version_one
from flask_restful import Api, Resource

def routes(api):
    """Add api endpoints"""
    api.add_resource(UserReportRedFlagList, '/red_flag_records')
    api.add_resource(UserReportRedFlag, '/red_flag_record/<int:id>')
    api.add_resource(Register, '/user')

    return None