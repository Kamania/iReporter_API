from app.api.v1.view.record_view import UserReportRedFlagList, UserReportRedFlag
from app.api.v1.view.user_view import Register
from flask import Blueprint

version_one = Blueprint('v1', __name__, url_prefix="/api/v1")

