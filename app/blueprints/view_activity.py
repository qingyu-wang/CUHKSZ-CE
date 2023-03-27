import datetime

from flask import Blueprint
from flask import render_template, request
from flask_login import login_required, current_user

from ..utils.utils_activity import activity_utils
from ..utils.utils_activity_record import activity_record_utils
from ..utils.utils_auth import UserRole
from ..utils.utils_course import course_utils
from ..utils.utils_error import render_error_template
from ..utils.utils_index import get_nav
from ..utils.utils_user import user_utils


bp_view_activity = Blueprint("view_activity", __name__)


# 活动信息
# http://127.0.0.1:5000/activity/info/
# http://127.0.0.1:5000/activity/info/?activity_code=CEC1010-LECTURE-A001
@bp_view_activity.route("/info/", methods=["GET", "POST"])
@login_required
def info():

    # Verify
    if current_user.role not in [UserRole.guest, UserRole.staff, UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "activity_info.html"

    # Params
    course_info_field_headers   = course_utils.field_headers
    activity_info_field_headers = activity_utils.field_headers
    activity_info_field_options = activity_utils.field_options
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "search": {
                "course_code":      {"placeholder": activity_info_field_headers["course_code"],   "default": None, "options": activity_info_field_options["course_code"]},
                "activity_type":    {"placeholder": activity_info_field_headers["activity_type"], "default": None, "options": activity_info_field_options["activity_type"]},
                "activity_year":    {"placeholder": activity_info_field_headers["activity_year"], "default": None, "options": activity_info_field_options["activity_year"]},
                "activity_term":    {"placeholder": activity_info_field_headers["activity_term"], "default": None, "options": activity_info_field_options["activity_term"]},
                "activity_date":    {"placeholder": activity_info_field_headers["activity_date"], "default": None, "options": activity_info_field_options["activity_date"]},
                "activity_code":    {"placeholder": activity_info_field_headers["activity_code"], "default": None, "options": activity_info_field_options["activity_code"]},
            },
            "course_info": {
                "course_code":      {"header": course_info_field_headers["course_code"]},
                "course_name":      {"header": course_info_field_headers["course_name"]},
            },
            "activity_info": {
                "course_code":      {"header": activity_info_field_headers["course_code"]},
                "activity_code":    {"header": activity_info_field_headers["activity_code"]},
                "activity_type":    {"header": activity_info_field_headers["activity_type"]},

                "activity_name":    {"header": activity_info_field_headers["activity_name"]},
                "activity_note":    {"header": activity_info_field_headers["activity_note"]},
                "activity_quota":   {"header": activity_info_field_headers["activity_quota"]},

                "activity_year":    {"header": activity_info_field_headers["activity_year"]},
                "activity_term":    {"header": activity_info_field_headers["activity_term"]},
                "activity_date":    {"header": activity_info_field_headers["activity_date"]},

                "createtime":       {"header": activity_info_field_headers["createtime"]},
                "modifytime":       {"header": activity_info_field_headers["modifytime"]},
                "modifyuser":       {"header": activity_info_field_headers["modifyuser"]}
            }
        },
        "activity_infos": None,
        "file_infos": None,
    }

    # GET
    if request.method == "GET":
        print("[INFO] %s %s/%s (%s) [%s] => %s" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role,
            request.method, request.endpoint
        ))
        activity_code = request.args.get("activity_code", "").strip()
        params["config"]["search"]["activity_code"]["default"] = activity_code
        if activity_code:
            # 查询
            result_1 = activity_utils.get_info(activity_code=activity_code)
            params["msgs"].extend(result_1["msgs"])
            if result_1["activity_info"]:
                params["activity_infos"] = [result_1["activity_info"]]
            # 保存
            if params["activity_infos"]:
                result_2 = activity_utils.save_infos(params["activity_infos"])
                params["msgs"].extend(result_2["msgs"])
                params["file_infos"] = [result_2["file_info"]]
        return render_template(template_path, **params)

    # POST
    if request.method == "POST":
        method = request.form["method"]
        print("[INFO] %s %s/%s (%s) [%s] => %s [method=%s]" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role, 
            request.method, request.endpoint, method
        ))

        # POST method=filter
        if method == "filter":
            activity_code = request.form["activity_code"].strip()
            field_filters = {
                "course_code":      request.form["course_code"].strip(),
                "activity_type":    request.form["activity_type"].strip(),
                "activity_year":    request.form["activity_year"].strip(),
                "activity_term":    request.form["activity_term"].strip(),
                "activity_date":    request.form["activity_date"].strip(),
            }
            field_filters = {key: val for key, val in field_filters.items() if val}
            for __field, __value in field_filters.items():
                params["config"]["search"][__field]["default"] = __value
            params["config"]["search"]["activity_code"]["default"] = activity_code
            params["config"]["search"]["activity_code"]["options"] = activity_utils.get_activity_code_options(field_filters)
            return render_template(template_path, **params)

        # POST method=search
        if method == "search":
            activity_code = request.form["activity_code"].strip()
            field_filters = {
                "course_code":      request.form["course_code"].strip(),
                "activity_type":    request.form["activity_type"].strip(),
                "activity_year":    request.form["activity_year"].strip(),
                "activity_term":    request.form["activity_term"].strip(),
                "activity_date":    request.form["activity_date"].strip(),
            }
            field_filters = {key: val for key, val in field_filters.items() if val}
            for __field, __value in field_filters.items():
                params["config"]["search"][__field]["default"] = __value
            params["config"]["search"]["activity_code"]["default"] = activity_code
            params["config"]["search"]["activity_code"]["options"] = activity_utils.get_activity_code_options(field_filters)
            if activity_code:
                result_1 = activity_utils.get_info(activity_code=activity_code)
                params["msgs"].extend(result_1["msgs"])
                if result_1["activity_info"]:
                    params["activity_infos"] = [result_1["activity_info"]]
                # 保存
                if params["activity_infos"]:
                    result_2 = activity_utils.save_infos(params["activity_infos"])
                    params["msgs"].extend(result_2["msgs"])
                    params["file_infos"] = [result_2["file_info"]]
            return render_template(template_path, **params)

    return render_error_template(message="系统错误")


# 活动记录
# http://127.0.0.1:5000/activity/record/
# http://127.0.0.1:5000/activity/record/?activity_code=CEC1010-LECTURE-A001&campus_idno=121090568
@bp_view_activity.route("/record/", methods=["GET", "POST"])
@login_required
def record():

    # Verify
    if current_user.role not in [UserRole.staff, UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "activity_record.html"

    # Params
    user_info_field_headers       = user_utils.field_headers
    course_info_field_headers     = course_utils.field_headers
    activity_info_field_headers   = activity_utils.field_headers
    activity_record_field_headers = activity_record_utils.field_headers
    activity_record_field_options = activity_record_utils.field_options
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "search": {
                "activity_code":    {"placeholder": activity_record_field_headers["activity_code"], "default": None, "options": activity_record_field_options["activity_code"]},
                "campus_idno":      {"placeholder": activity_record_field_headers["campus_idno"],   "default": None, "options": None}
            },
            "user_info": {
                "campus_idno":      {"header": user_info_field_headers["campus_idno"]},
                "name":             {"header": user_info_field_headers["name"]},
            },
            "course_info": {
                "course_code":          {"header": course_info_field_headers["course_code"]},
                "course_name":          {"header": course_info_field_headers["course_name"]},
                "activity_rules_html":   {"header": course_info_field_headers["activity_rules"]},
            },
            "activity_info": {
                "activity_code":    {"header": activity_info_field_headers["activity_code"]},
                "activity_name":    {"header": activity_info_field_headers["activity_name"]},
                "activity_type":    {"header": activity_info_field_headers["activity_type"]},
            },
            "activity_record": {
                "activity_code":    {"header": activity_record_field_headers["activity_code"]},
                "campus_idno":      {"header": activity_record_field_headers["campus_idno"]},
                "count":            {"header": activity_record_field_headers["count"]},

                "signup":           {"header": activity_record_field_headers["signup"]},
                "signin_record":    {"header": activity_record_field_headers["signin_record"]},
                "takeoff":          {"header": activity_record_field_headers["takeoff"]},
                "score":            {"header": activity_record_field_headers["score"]},
                "grade":            {"header": activity_record_field_headers["grade"]},
                "note":             {"header": activity_record_field_headers["note"]},

                "createtime":       {"header": activity_record_field_headers["createtime"]},
                "modifytime":       {"header": activity_record_field_headers["modifytime"]},
                "modifyuser":       {"header": activity_record_field_headers["modifyuser"]},
            },
        },
        "activity_records": None,
        "file_infos": None,
    }

    # GET
    if request.method == "GET":
        print("[INFO] %s %s/%s (%s) [%s] => %s" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role,
            request.method, request.endpoint
        ))
        activity_code = request.args.get("activity_code", "").strip()
        campus_idno   = request.args.get("campus_idno", "").strip()
        params["config"]["search"]["activity_code"]["default"] = activity_code
        params["config"]["search"]["campus_idno"]["default"]   = campus_idno
        # 查询
        if activity_code and campus_idno:
            result_1 = activity_record_utils.get_record(activity_code=activity_code, campus_idno=campus_idno)
            params["msgs"].extend(result_1["msgs"])
            if result_1["activity_record"]:
                params["activity_records"] = [result_1["activity_record"]]
        # 保存
        if params["activity_records"]:
            result_2 = activity_record_utils.save_records(params["activity_records"])
            params["msgs"].extend(result_2["msgs"])
            params["file_infos"] = [result_2["file_info"]]
        return render_template(template_path, **params)

    # POST
    if request.method == "POST":
        method = request.form["method"]
        print("[INFO] %s %s/%s (%s) [%s] => %s [method=%s]" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role, 
            request.method, request.endpoint, method
        ))

        # POST method=search
        if method == "search":
            activity_code = request.form["activity_code"].strip()
            campus_idno   = request.form["campus_idno"].strip()
            params["config"]["search"]["activity_code"]["default"] = activity_code
            params["config"]["search"]["campus_idno"]["default"]   = campus_idno
            # 查询
            if activity_code and campus_idno:
                result_1 = activity_record_utils.get_record(activity_code=activity_code, campus_idno=campus_idno)
                params["msgs"].extend(result_1["msgs"])
                if result_1["activity_record"]:
                    params["activity_records"] = [result_1["activity_record"]]
            # 保存
            if params["activity_records"]:
                result_2 = activity_record_utils.save_records(params["activity_records"])
                params["msgs"].extend(result_2["msgs"])
                params["file_infos"] = [result_2["file_info"]]
            return render_template(template_path, **params)

    return render_error_template(message="系统错误")


# 活动管理
# http://127.0.0.1:5000/activity/info_for_admin/
# http://127.0.0.1:5000/activity/info_for_admin/?activity_code=CEC1010-LECTURE-A001
@bp_view_activity.route("/info_for_admin/", methods=["GET", "POST"])
@login_required
def info_for_admin():

    # Verify
    if current_user.role not in [UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "activity_info_for_admin.html"

    # Params
    course_info_field_headers   = course_utils.field_headers
    activity_info_field_headers = activity_utils.field_headers
    activity_info_field_options = activity_utils.field_options
    activity_info_default_doc   = activity_utils.new_doc
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "search": {
                "course_code":      {"placeholder": activity_info_field_headers["course_code"],   "default": None, "options": activity_info_field_options["course_code"]},
                "activity_type":    {"placeholder": activity_info_field_headers["activity_type"], "default": None, "options": activity_info_field_options["activity_type"]},
                "activity_year":    {"placeholder": activity_info_field_headers["activity_year"], "default": None, "options": activity_info_field_options["activity_year"]},
                "activity_term":    {"placeholder": activity_info_field_headers["activity_term"], "default": None, "options": activity_info_field_options["activity_term"]},
                "activity_date":    {"placeholder": activity_info_field_headers["activity_date"], "default": None, "options": activity_info_field_options["activity_date"]},
                "activity_code":    {"placeholder": activity_info_field_headers["activity_code"], "default": None, "options": activity_info_field_options["activity_code"]},
            },
            "course_info": {
                "course_code":      {"header": course_info_field_headers["course_code"]},
                "course_name":      {"header": course_info_field_headers["course_name"]},
            },
            "activity_info": {
                "course_code":      {"header": activity_info_field_headers["course_code"],    "fixed": False, "default": activity_info_default_doc["course_code"],    "options": activity_info_field_options["course_code"]},
                "activity_code":    {"header": activity_info_field_headers["activity_code"],  "fixed": False, "default": activity_info_default_doc["activity_code"],  "options": activity_info_field_options["activity_code"]},
                "activity_type":    {"header": activity_info_field_headers["activity_type"],  "fixed": False, "default": activity_info_default_doc["activity_type"],  "options": activity_info_field_options["activity_type"]},

                "activity_name":    {"header": activity_info_field_headers["activity_name"],  "fixed": False, "default": activity_info_default_doc["activity_name"],  "options": None},
                "activity_note":    {"header": activity_info_field_headers["activity_note"],  "fixed": False, "default": activity_info_default_doc["activity_note"],  "options": None},
                "activity_quota":   {"header": activity_info_field_headers["activity_quota"], "fixed": False, "default": activity_info_default_doc["activity_quota"], "options": None},

                "activity_year":    {"header": activity_info_field_headers["activity_year"],  "fixed": False, "default": activity_info_default_doc["activity_year"],  "options": activity_info_field_options["activity_year"]},
                "activity_term":    {"header": activity_info_field_headers["activity_term"],  "fixed": False, "default": activity_info_default_doc["activity_term"],  "options": activity_info_field_options["activity_term"]},
                "activity_date":    {"header": activity_info_field_headers["activity_date"],  "fixed": False, "default": activity_info_default_doc["activity_date"],  "options": activity_info_field_options["activity_date"]},

                "createtime":       {"header": activity_info_field_headers["createtime"],     "fixed": True,  "default": activity_info_default_doc["createtime"],     "options": None},
                "modifytime":       {"header": activity_info_field_headers["modifytime"],     "fixed": True,  "default": activity_info_default_doc["modifytime"],     "options": None},
                "modifyuser":       {"header": activity_info_field_headers["modifyuser"],     "fixed": True,  "default": activity_info_default_doc["modifyuser"],     "options": None}
            }
        },
        "activity_infos": None,
        "file_infos": None,
    }

    # GET
    if request.method == "GET":
        print("[INFO] %s %s/%s (%s) [%s] => %s" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role,
            request.method, request.endpoint
        ))
        activity_code = request.args.get("activity_code", "").strip()
        params["config"]["search"]["activity_code"]["default"] = activity_code
        if activity_code:
            # 查询
            result_1 = activity_utils.get_info(activity_code=activity_code)
            params["msgs"].extend(result_1["msgs"])
            if result_1["activity_info"]:
                params["activity_infos"] = [result_1["activity_info"]]
            # 保存
            if params["activity_infos"]:
                result_2 = activity_utils.save_infos(params["activity_infos"])
                params["msgs"].extend(result_2["msgs"])
                params["file_infos"] = [result_2["file_info"]]
        return render_template(template_path, **params)

    # POST
    if request.method == "POST":
        method = request.form["method"]
        print("[INFO] %s %s/%s (%s) [%s] => %s [method=%s]" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role, 
            request.method, request.endpoint, method
        ))

        # POST method=filter
        if method == "filter":
            activity_code = request.form["activity_code"].strip()
            field_filters = {
                "course_code":      request.form["course_code"].strip(),
                "activity_type":    request.form["activity_type"].strip(),
                "activity_year":    request.form["activity_year"].strip(),
                "activity_term":    request.form["activity_term"].strip(),
                "activity_date":    request.form["activity_date"].strip(),
            }
            field_filters = {key: val for key, val in field_filters.items() if val}
            # 筛选
            for __field, __value in field_filters.items():
                params["config"]["search"][__field]["default"] = __value
            params["config"]["search"]["activity_code"]["default"] = activity_code
            params["config"]["search"]["activity_code"]["options"] = activity_utils.get_activity_code_options(field_filters)
            return render_template(template_path, **params)

        # POST method=search
        if method == "search":
            activity_code = request.form["activity_code"].strip()
            field_filters = {
                "course_code":      request.form["course_code"].strip(),
                "activity_type":    request.form["activity_type"].strip(),
                "activity_year":    request.form["activity_year"].strip(),
                "activity_term":    request.form["activity_term"].strip(),
                "activity_date":    request.form["activity_date"].strip(),
            }
            field_filters = {key: val for key, val in field_filters.items() if val}
            # 筛选
            for __field, __value in field_filters.items():
                params["config"]["search"][__field]["default"] = __value
            params["config"]["search"]["activity_code"]["default"] = activity_code
            params["config"]["search"]["activity_code"]["options"] = activity_utils.get_activity_code_options(field_filters)
            if activity_code:
                # 查询
                result_1 = activity_utils.get_info(activity_code=activity_code)
                params["msgs"].extend(result_1["msgs"])
                if result_1["activity_info"]:
                    params["activity_infos"] = [result_1["activity_info"]]
                # 保存
                if params["activity_infos"]:
                    result_2 = activity_utils.save_infos(params["activity_infos"])
                    params["msgs"].extend(result_2["msgs"])
                    params["file_infos"] = [result_2["file_info"]]
            return render_template(template_path, **params)

        # POST method=update
        if method == "update":
            new_activity_info = {key: val.strip() for key, val in request.form.items()}
            new_activity_info.pop("method")
            old_activity_code = new_activity_info.pop("old_activity_code")
            # 更新
            result_1 = activity_utils.update_info(new_activity_info=new_activity_info, old_activity_code=old_activity_code)
            params["msgs"].extend(result_1["msgs"])
            if params["msgs"][-1]["type"] == "success":
                activity_code = new_activity_info["activity_code"]
            else:
                activity_code = old_activity_code
            params["config"]["search"]["activity_code"]["default"] = activity_code
            # 查询
            result_2 = activity_utils.get_info(activity_code=activity_code)
            params["msgs"].extend(result_2["msgs"])
            if result_2["activity_info"]:
                params["activity_infos"] = [result_2["activity_info"]]
            # 保存
            if params["activity_infos"]:
                result_3 = activity_utils.save_infos(params["activity_infos"])
                params["msgs"].extend(result_3["msgs"])
                params["file_infos"] = [result_3["file_info"]]
            # 更新选项
            activity_info_field_options = activity_utils.field_options
            for __field in params["config"]["search"]:
                if params["config"]["search"][__field]["options"] is not None:
                    params["config"]["search"][__field]["options"] = activity_info_field_options[__field]
            for __field in params["config"]["activity_info"]:
                if params["config"]["activity_info"][__field]["options"] is not None:
                    params["config"]["activity_info"][__field]["options"] = activity_info_field_options[__field]
            return render_template(template_path, **params)

        # POST method=create
        if method == "create":
            new_activity_info = {key: val.strip() for key, val in request.form.items()}
            new_activity_info.pop("method")
            # 新增
            result_1 = activity_utils.create_info(new_activity_info=new_activity_info)
            params["msgs"].extend(result_1["msgs"])
            if params["msgs"][-1]["type"] == "success":
                activity_code = new_activity_info["activity_code"]
                params["config"]["search"]["activity_code"]["default"] = activity_code
                # 查询
                result_2 = activity_utils.get_info(activity_code=activity_code)
                params["msgs"].extend(result_2["msgs"])
                if result_2["activity_info"]:
                    params["activity_infos"] = [result_2["activity_info"]]
                 # 保存
                if params["activity_infos"]:
                    result_3 = activity_utils.save_infos(params["activity_infos"])
                    params["msgs"].extend(result_3["msgs"])
                    params["file_infos"] = [result_3["file_info"]]
                # 更新选项
                activity_info_field_options = activity_utils.field_options
                for __field in params["config"]["search"]:
                    if params["config"]["search"][__field]["options"] is not None:
                        params["config"]["search"][__field]["options"] = activity_info_field_options[__field]
                for __field in params["config"]["activity_info"]:
                    if params["config"]["activity_info"][__field]["options"] is not None:
                        params["config"]["activity_info"][__field]["options"] = activity_info_field_options[__field]
            return render_template(template_path, **params)

    return render_error_template(message="系统错误")


# 活动数据
# http://127.0.0.1:5000/activity/data/
# http://127.0.0.1:5000/activity/data/?activity_code=CEC1010-LECTURE-A001
@bp_view_activity.route("/data/", methods=["GET", "POST"])
@login_required
def data():

    # Verify
    if current_user.role not in [UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "activity_data.html"

    # Params
    user_info_field_headers       = user_utils.field_headers
    course_info_field_headers     = course_utils.field_headers
    activity_info_field_headers   = activity_utils.field_headers
    activity_info_field_options   = activity_utils.field_options
    activity_record_field_headers = activity_record_utils.field_headers
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "search": {
                "course_code":      {"placeholder": activity_info_field_headers["course_code"],   "default": None, "options": activity_info_field_options["course_code"]},
                "activity_type":    {"placeholder": activity_info_field_headers["activity_type"], "default": None, "options": activity_info_field_options["activity_type"]},
                "activity_year":    {"placeholder": activity_info_field_headers["activity_year"], "default": None, "options": activity_info_field_options["activity_year"]},
                "activity_term":    {"placeholder": activity_info_field_headers["activity_term"], "default": None, "options": activity_info_field_options["activity_term"]},
                "activity_date":    {"placeholder": activity_info_field_headers["activity_date"], "default": None, "options": activity_info_field_options["activity_date"]},
                "activity_code":    {"placeholder": activity_info_field_headers["activity_code"], "default": None, "options": activity_info_field_options["activity_code"]},
            },
            "update": {
                "update_activity_info": {
                    "file_name":   "update_activity_info_file",
                    "placeholder": "活动信息.xlsx"
                },
                "update_activity_record": {
                    "file_name":   "update_activity_record_file",
                    "placeholder": "活动记录.xlsx"
                },
            },
            "course_info": {
                "course_code": {"header": course_info_field_headers["course_code"]},
                "course_name": {"header": course_info_field_headers["course_name"]},
            },
            "activity_info": {
                "course_code":    {"header": activity_info_field_headers["course_code"]},
                "activity_code":  {"header": activity_info_field_headers["activity_code"]},
                "activity_type":  {"header": activity_info_field_headers["activity_type"]},

                "activity_name":  {"header": activity_info_field_headers["activity_name"]},
                "activity_note":  {"header": activity_info_field_headers["activity_note"]},
                "activity_quota": {"header": activity_info_field_headers["activity_quota"]},

                "activity_year":  {"header": activity_info_field_headers["activity_year"]},
                "activity_term":  {"header": activity_info_field_headers["activity_term"]},
                "activity_date":  {"header": activity_info_field_headers["activity_date"]},

                "createtime":     {"header": activity_info_field_headers["createtime"]},
                "modifytime":     {"header": activity_info_field_headers["modifytime"]},
                "modifyuser":     {"header": activity_info_field_headers["modifyuser"]}
            },
            "activity_overview": {
                "num_total":   {"header": "总人数"},
                "num_done":    {"header": "完成数"},
                "num_signup":  {"header": "报名数"},
                "num_takeoff": {"header": "请假数"},
            },
            "user_info": {
                "campus_idno": {"header": user_info_field_headers["campus_idno"]},
                "name":        {"header": user_info_field_headers["name"]},
            },
            "activity_record": {
                # "activity_code": {"header": activity_record_field_headers["activity_code"], "width": 5},
                # "campus_idno":   {"header": activity_record_field_headers["campus_idno"],   "width": 5},
                "count":         {"header": activity_record_field_headers["count"],         "width": 5},

                "signup":        {"header": activity_record_field_headers["signup"],        "width": 5},
                # "signin_record": {"header": activity_record_field_headers["signin_record"], "width": 5},
                "takeoff":       {"header": activity_record_field_headers["takeoff"],       "width": 5},
                "score":         {"header": activity_record_field_headers["score"],         "width": 5},
                "grade":         {"header": activity_record_field_headers["grade"],         "width": 5},
                "note":          {"header": activity_record_field_headers["note"],          "width": 20},

                # "createtime":    {"header": activity_record_field_headers["createtime"],    "width": 5},
                # "modifytime":    {"header": activity_record_field_headers["modifytime"],    "width": 5},
                # "modifyuser":    {"header": activity_record_field_headers["modifyuser"],    "width": 5},
            },
            "display_limit": 200
        },
        "activity_infos": None,
        "file_infos": None,
    }

    # GET
    if request.method == "GET":
        print("[INFO] %s %s/%s (%s) [%s] => %s" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role,
            request.method, request.endpoint
        ))
        activity_code = request.args.get("activity_code", "").strip()
        params["config"]["search"]["activity_code"]["default"] = activity_code
        if activity_code:
            # 查询
            result_1 = activity_utils.get_info_with_detail(activity_code=activity_code)
            params["msgs"].extend(result_1["msgs"])
            if result_1["activity_info"]:
                params["activity_infos"] = [result_1["activity_info"]]
            # 保存 - 活动信息
            if params["activity_infos"]:
                result_2 = activity_utils.save_infos(params["activity_infos"])
                params["msgs"].extend(result_2["msgs"])
                params["file_infos"] = [result_2["file_info"]]
                # 保存 - 活动记录
                activity_records = []
                for activity_info in params["activity_infos"]:
                    activity_records.extend(activity_info["activity_records"])
                if activity_records:
                    result_3 = activity_record_utils.save_records(activity_records)
                    params["msgs"].extend(result_3["msgs"])
                    params["file_infos"].append(result_3["file_info"])
                    result_4 = activity_record_utils.save_records_with_detail(activity_records)
                    params["msgs"].extend(result_4["msgs"])
                    params["file_infos"].append(result_4["file_info"])
        return render_template(template_path, **params)

    # POST
    if request.method == "POST":
        method = request.form["method"]
        print("[INFO] %s %s/%s (%s) [%s] => %s [method=%s]" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role, 
            request.method, request.endpoint, method
        ))

        # POST method=filter
        if method == "filter":
            activity_code = request.form["activity_code"].strip()
            field_filters = {
                "course_code":      request.form["course_code"].strip(),
                "activity_type":    request.form["activity_type"].strip(),
                "activity_year":    request.form["activity_year"].strip(),
                "activity_term":    request.form["activity_term"].strip(),
                "activity_date":    request.form["activity_date"].strip(),
            }
            field_filters = {key: val for key, val in field_filters.items() if val}
            for __field, __value in field_filters.items():
                params["config"]["search"][__field]["default"] = __value
            params["config"]["search"]["activity_code"]["default"] = activity_code
            params["config"]["search"]["activity_code"]["options"] = activity_utils.get_activity_code_options(field_filters)
            return render_template(template_path, **params)

        # POST method=search
        if method == "search":
            activity_code = request.form["activity_code"].strip()
            field_filters = {
                "course_code":      request.form["course_code"].strip(),
                "activity_type":    request.form["activity_type"].strip(),
                "activity_year":    request.form["activity_year"].strip(),
                "activity_term":    request.form["activity_term"].strip(),
                "activity_date":    request.form["activity_date"].strip(),
            }
            field_filters = {key: val for key, val in field_filters.items() if val}
            for __field, __value in field_filters.items():
                params["config"]["search"][__field]["default"] = __value
            params["config"]["search"]["activity_code"]["default"] = activity_code
            params["config"]["search"]["activity_code"]["options"] = activity_utils.get_activity_code_options(field_filters)
            if activity_code:
                result_1 = activity_utils.get_info_with_detail(activity_code=activity_code)
                params["msgs"].extend(result_1["msgs"])
                if result_1["activity_info"]:
                    params["activity_infos"] = [result_1["activity_info"]]
                # 保存 - 活动信息
                if params["activity_infos"]:
                    result_2 = activity_utils.save_infos(params["activity_infos"])
                    params["msgs"].extend(result_2["msgs"])
                    params["file_infos"] = [result_2["file_info"]]
                    # 保存 - 活动记录
                    activity_records = []
                    for activity_info in params["activity_infos"]:
                        activity_records.extend(activity_info["activity_records"])
                    if activity_records:
                        result_3 = activity_record_utils.save_records(activity_records)
                        params["msgs"].extend(result_3["msgs"])
                        params["file_infos"].append(result_3["file_info"])
                        result_4 = activity_record_utils.save_records_with_detail(activity_records)
                        params["msgs"].extend(result_4["msgs"])
                        params["file_infos"].append(result_4["file_info"])
            return render_template(template_path, **params)

        # POST method=update_activity_info
        if method == "update_activity_info":
            file_name = params["config"]["update"][method]["file_name"]
            update_file = request.files[file_name]
            if update_file:
                result = activity_utils.update_info_by_file(update_file)
                params["msgs"].extend(result["msgs"])
            return render_template(template_path, **params)

        # POST method=update_activity_record
        if method == "update_activity_record":
            file_name = params["config"]["update"][method]["file_name"]
            update_file = request.files[file_name]
            if update_file:
                result = activity_record_utils.update_record_by_file(update_file)
                params["msgs"].extend(result["msgs"])
            return render_template(template_path, **params)

    return render_error_template(message="系统错误")
