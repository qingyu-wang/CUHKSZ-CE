import datetime

from flask import Blueprint
from flask import render_template, request
from flask_login import login_required, current_user

from ..utils.utils_auth import UserRole
from ..utils.utils_board import board_utils
from ..utils.utils_course_record import course_record_utils
from ..utils.utils_error import render_error_template
from ..utils.utils_index import get_nav
from ..utils.utils_user import user_utils


bp_view_board = Blueprint("view_board", __name__)


# 整体概况
# http://127.0.0.1:5000/board/overview/
@bp_view_board.route("/overview/", methods=["GET"])
@login_required
def overview():

    # Verify
    if current_user.role not in [UserRole.staff, UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "board_overview.html"

    # Params
    course_record_field_options = course_record_utils.field_options
    user_info_field_headers     = user_utils.field_headers
    user_info_field_options     = user_utils.field_options
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "1st_categs": {
                "campus_grade": {"header": user_info_field_headers["campus_grade"], "options": [i for i in user_info_field_options["campus_grade"]      if i != "/"]},
                "campus_year":  {"header": user_info_field_headers["campus_year"],  "options": [i for i in user_info_field_options["campus_year"][::-1] if i != "/"]},
            },
            "2nd_categ_options": course_record_field_options["course_code"],
            "3rd_categ_options": ["总计"] + [i for i in ["已认证", "已完成", "进行中", "未开始"] if i in course_record_field_options["status"]],
        },
        "overview_infos": None,
    }

    # GET
    if request.method == "GET":
        print("[INFO] %s %s/%s (%s) [%s] => %s" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role,
            request.method, request.endpoint
        ))
        # 查询
        result = board_utils.get_overview_infos()
        params["msgs"].extend(result["msgs"])
        if result["overview_infos"]:
            params["overview_infos"] = result["overview_infos"]
        return render_template(template_path, **params)

    return render_error_template(message="系统错误")


# 书院概况
# http://127.0.0.1:5000/board/college/
@bp_view_board.route("/college/", methods=["GET", "POST"])
@login_required
def college():

    # Verify
    if current_user.role not in [UserRole.staff, UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "board_college.html"

    # Params
    course_record_field_options = course_record_utils.field_options
    user_info_field_headers     = user_utils.field_headers
    user_info_field_options     = user_utils.field_options
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "1st_categs": {
                "campus_grade": {"header": user_info_field_headers["campus_grade"], "options": [i for i in user_info_field_options["campus_grade"]      if i != "/"]},
                "campus_year":  {"header": user_info_field_headers["campus_year"],  "options": [i for i in user_info_field_options["campus_year"][::-1] if i != "/"]},
            },
            "2nd_categ_options": [i for i in user_info_field_options["campus_addr"] if i != "/"],
            "3rd_categ_options": ["总计"] + [i for i in ["已认证", "已完成", "进行中", "未开始"] if i in course_record_field_options["status"]],
        },
        "college_infos": None,
    }

    # GET
    if request.method == "GET":
        print("[INFO] %s %s/%s (%s) [%s] => %s" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role,
            request.method, request.endpoint
        ))
        # 查询
        result = board_utils.get_college_infos()
        params["msgs"].extend(result["msgs"])
        if result["activity_types"]:
            params["config"]["3rd_categ_options"] += result["activity_types"]
        if result["college_infos"]:
            params["college_infos"] = result["college_infos"]
        return render_template(template_path, **params)

    return render_error_template(message="系统错误")
