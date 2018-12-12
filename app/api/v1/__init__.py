from .views import UserReportRedFlagList, UserReportRedFlag, Patch_location
from .views import Patch_comment
from flask import Blueprint

version_one = Blueprint('v1', __name__, url_prefix="/api/v1")
