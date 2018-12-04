from .views import UserReportRedFlagList, UserReportRedFlag
from .views import Register
from flask import Blueprint

version_one = Blueprint('v1', __name__, url_prefix="/api/v1")
