from flask import Blueprint
from flask import render_template, request

from ..utils.utils_error import render_error_template
from ..utils.utils_index import get_nav


bp_view_index = Blueprint("view_index", __name__)


# 首页
# http://127.0.0.1:5000/
@bp_view_index.route("/", methods=["GET"])
def index():

    # Template
    template_path = "index.html"

    # Params
    params = {
        "nav": get_nav()
    }

    # GET
    if request.method == "GET":
        return render_template(template_path, **params)

    return render_error_template(message="系统错误")
