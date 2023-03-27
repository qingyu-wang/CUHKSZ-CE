from flask import Blueprint
from flask import render_template, request
from flask_login import login_required, current_user

from ..utils.utils_activity import activity_utils
from ..utils.utils_activity_record import activity_record_utils
from ..utils.utils_auth import UserRole
from ..utils.utils_course import course_utils
from ..utils.utils_course_record import course_record_utils
from ..utils.utils_error import render_error_template
from ..utils.utils_index import get_nav
from ..utils.utils_user import user_utils


bp_view_course = Blueprint("view_course", __name__)


# 课程信息
# http://127.0.0.1:5000/course/info/
# http://127.0.0.1:5000/course/info/?course_code=CEC1010
@bp_view_course.route("/info/", methods=["GET", "POST"])
@login_required
def info():

    # Verify
    if current_user.role not in [UserRole.guest, UserRole.staff, UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "course_info.html"

    # Params
    course_info_field_headers   = course_utils.field_headers
    activity_info_field_headers = activity_utils.field_headers
    activity_info_field_options = activity_utils.field_options
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "search": {
                "course_code":   {"placeholder": course_info_field_headers["course_code"],     "default": None, "options": activity_info_field_options["course_code"]},
                "activity_type": {"placeholder": activity_info_field_headers["activity_type"], "default": None, "options": activity_info_field_options["activity_type"]},
                "activity_year": {"placeholder": activity_info_field_headers["activity_year"], "default": None, "options": activity_info_field_options["activity_year"]},
                "activity_term": {"placeholder": activity_info_field_headers["activity_term"], "default": None, "options": activity_info_field_options["activity_term"]},
                "activity_date": {"placeholder": activity_info_field_headers["activity_date"], "default": None, "options": activity_info_field_options["activity_date"]},
            },
            "course_info": {
                "course_code":    {"header": course_info_field_headers["course_code"]},
                "course_name":    {"header": course_info_field_headers["course_name"]},
                "activity_rules": {"header": course_info_field_headers["activity_rules"]},

                "createtime":     {"header": course_info_field_headers["createtime"]},
                "modifytime":     {"header": course_info_field_headers["modifytime"]},
                "modifyuser":     {"header": course_info_field_headers["modifyuser"]}
            },
            "activity_info": {
                "activity_code":  {"header": activity_utils.field_headers["activity_code"],  "width": 15},
                "activity_type":  {"header": activity_utils.field_headers["activity_type"],  "width": 10},

                "activity_name":  {"header": activity_utils.field_headers["activity_name"],  "width": 40},
                "activity_note":  {"header": activity_utils.field_headers["activity_note"],  "width": 40},
                "activity_quota": {"header": activity_utils.field_headers["activity_quota"], "width": 10},

                "activity_year":  {"header": activity_utils.field_headers["activity_year"],  "width": 10},
                "activity_term":  {"header": activity_utils.field_headers["activity_term"],  "width": 10},
                "activity_date":  {"header": activity_utils.field_headers["activity_date"],  "width": 10},
            }
        },
        "course_infos": None,
        "file_infos": None,
    }

    # GET
    if request.method == "GET":
        print("[INFO] %s/%s (%s) [%s] => %s" % (
            current_user.idno, current_user.username, current_user.role,
            request.method, request.endpoint
        ))
        course_code = request.args.get("course_code", "").strip()
        field_filters = {
            "activity_type":    request.args.get("activity_type", "").strip(),
            "activity_year":    request.args.get("activity_year", "").strip(),
            "activity_term":    request.args.get("activity_term", "").strip(),
            "activity_date":    request.args.get("activity_date", "").strip(),
        }
        field_filters = {key: val for key, val in field_filters.items() if val}
        for __field, __value in field_filters.items():
            params["config"]["search"][__field]["default"] = __value
        params["config"]["search"]["course_code"]["default"] = course_code
        if course_code:
            # 查询 - 课程信息
            result_1 = course_utils.get_info(course_code=course_code, field_filters=field_filters)
            params["msgs"].extend(result_1["msgs"])
            if result_1["course_info"]:
                params["course_infos"] = [result_1["course_info"]]
            # 保存 - 课程信息
            if params["course_infos"]:
                result_2 = course_utils.save_infos(params["course_infos"])
                params["msgs"].extend(result_2["msgs"])
                params["file_infos"] = [result_2["file_info"]]
                # 保存 - 活动信息
                activity_infos = []
                for course_info in params["course_infos"]:
                    activity_infos.extend(course_info["activity_infos"])
                if activity_infos:
                    result_3 = activity_utils.save_infos(activity_infos)
                    params["msgs"].extend(result_3["msgs"])
                    params["file_infos"].append(result_3["file_info"])
        return render_template(template_path, **params)

    # POST
    if request.method == "POST":
        method = request.form["method"]
        print("[INFO] %s/%s (%s) [%s] => %s [method=%s]" % (
            current_user.idno, current_user.username, current_user.role, 
            request.method, request.endpoint, method
        ))

        # POST method=search
        if method == "search":
            course_code   = request.form["course_code"].strip()
            field_filters = {
                "activity_type":    request.form["activity_type"].strip(),
                "activity_year":    request.form["activity_year"].strip(),
                "activity_term":    request.form["activity_term"].strip(),
                "activity_date":    request.form["activity_date"].strip(),
            }
            field_filters = {key: val for key, val in field_filters.items() if val}
            for __field, __value in field_filters.items():
                params["config"]["search"][__field]["default"] = __value
            params["config"]["search"]["course_code"]["default"] = course_code
            if course_code:
                # 查询 - 课程信息
                result_1 = course_utils.get_info(course_code=course_code, field_filters=field_filters)
                params["msgs"].extend(result_1["msgs"])
                if result_1["course_info"]:
                    params["course_infos"] = [result_1["course_info"]]
                # 保存 - 课程信息
                if params["course_infos"]:
                    result_2 = course_utils.save_infos(params["course_infos"])
                    params["msgs"].extend(result_2["msgs"])
                    params["file_infos"] = [result_2["file_info"]]
                    # 保存 - 活动信息
                    activity_infos = []
                    for course_info in params["course_infos"]:
                        activity_infos.extend(course_info["activity_infos"])
                    if activity_infos:
                        result_3 = activity_utils.save_infos(activity_infos)
                        params["msgs"].extend(result_3["msgs"])
                        params["file_infos"].append(result_3["file_info"])
            return render_template(template_path, **params)

    return render_error_template(message="系统错误")


# 课程记录
# http://127.0.0.1:5000/course/record/
# http://127.0.0.1:5000/course/record/?course_code=CEC1010&campus_idno=121090568
@bp_view_course.route("/record/", methods=["GET", "POST"])
@login_required
def record():

    # Verify
    if current_user.role not in [UserRole.staff, UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "course_record.html"

    # Params
    user_info_field_headers       = user_utils.field_headers
    course_info_field_headers     = course_utils.field_headers
    course_record_field_headers   = course_record_utils.field_headers
    course_record_field_options   = course_record_utils.field_options
    activity_info_field_headers   = activity_utils.field_headers
    activity_record_field_headers = activity_record_utils.field_headers
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "search": {
                "course_code": {"placeholder": course_record_field_headers["course_code"], "default": None, "options": course_record_field_options["course_code"]},
                "campus_idno": {"placeholder": course_record_field_headers["campus_idno"], "default": None, "options": None}
            },
            "user_info": {
                "campus_idno": {"header": user_info_field_headers["campus_idno"]},
                "name":        {"header": user_info_field_headers["name"]},
            },
            "course_info": {
                "course_code":    {"header": course_info_field_headers["course_code"]},
                "course_name":    {"header": course_info_field_headers["course_name"]},
                "activity_rules": {"header": course_info_field_headers["activity_rules"]},
            },
            "course_record": {
                "course_code":   {"header": course_record_field_headers["course_code"]},
                "campus_idno":   {"header": course_record_field_headers["campus_idno"]},

                "status":        {"header": course_record_field_headers["status"]},
                "activity_done": {"header": course_record_field_headers["activity_done"]},
                "authen":        {"header": course_record_field_headers["authen"]},

                "note":          {"header": course_record_field_headers["note"]},

                "createtime":    {"header": course_record_field_headers["createtime"]},
                "modifytime":    {"header": course_record_field_headers["modifytime"]},
                "modifyuser":    {"header": course_record_field_headers["modifyuser"]},
            },
            "activity_info": {
                "activity_code": {"header": activity_info_field_headers["activity_code"],  "width": 10},
                "activity_name": {"header": activity_info_field_headers["activity_name"],  "width": 20},
                "activity_type": {"header": activity_info_field_headers["activity_type"],  "width": 5},

                # "activity_name": {"header": activity_info_field_headers["activity_name"],  "width": 5},
                # "activity_note": {"header": activity_info_field_headers["activity_note"],  "width": 5},
                # "activity_quota":{"header": activity_info_field_headers["activity_quota"], "width": 5},

                # "activity_year": {"header": activity_info_field_headers["activity_year"],  "width": 5},
                # "activity_term": {"header": activity_info_field_headers["activity_term"],  "width": 5},
                # "activity_date": {"header": activity_info_field_headers["activity_date"],  "width": 5},

                # "createtime":    {"header": activity_info_field_headers["createtime"],     "width": 5},
                # "modifytime":    {"header": activity_info_field_headers["modifytime"],     "width": 5},
                # "modifyuser":    {"header": activity_info_field_headers["modifyuser"],     "width": 5},
            },
            "activity_record": {
                "activity_code": {"header": activity_record_field_headers["activity_code"], "width": 10},
                # "campus_idno":   {"header": activity_record_field_headers["campus_idno"],   "width": 15},
                "count":         {"header": activity_record_field_headers["count"],         "width": 5},

                "signup":        {"header": activity_record_field_headers["signup"],        "width": 5},
                # "signin_record": {"header": activity_record_field_headers["signin_record"], "width": 15},
                "takeoff":       {"header": activity_record_field_headers["takeoff"],       "width": 5},
                "score":         {"header": activity_record_field_headers["score"],         "width": 5},
                "grade":         {"header": activity_record_field_headers["grade"],         "width": 5},
                "note":          {"header": activity_record_field_headers["note"],          "width": 20},

                # "createtime":    {"header": activity_record_field_headers["createtime"],    "width": 5},
                # "modifytime":    {"header": activity_record_field_headers["modifytime"],    "width": 5},
                # "modifyuser":    {"header": activity_record_field_headers["modifyuser"],    "width": 5},
            }
        },
        "course_records": None,
        "file_infos": None,
    }

    # GET
    if request.method == "GET":
        print("[INFO] %s/%s (%s) [%s] => %s" % (
            current_user.idno, current_user.username, current_user.role,
            request.method, request.endpoint
        ))
        course_code = request.args.get("course_code", "").strip()
        campus_idno = request.args.get("campus_idno", "").strip()
        params["config"]["search"]["course_code"]["default"] = course_code
        params["config"]["search"]["campus_idno"]["default"] = campus_idno
        # 查询
        if course_code and campus_idno:
            result_1 = course_record_utils.get_record(course_code=course_code, campus_idno=campus_idno)
            params["msgs"].extend(result_1["msgs"])
            if result_1["course_record"]:
                params["course_records"] = [result_1["course_record"]]
        # 保存 - 课程记录
        if params["course_records"]:
            result_2 = course_record_utils.save_records(params["course_records"])
            params["msgs"].extend(result_2["msgs"])
            params["file_infos"] = [result_2["file_info"]]
            # 保存 - 活动记录
            activity_records = []
            for course_record in params["course_records"]:
                activity_records.extend(course_record["activity_records"])
            if activity_records:
                result_3 = activity_record_utils.save_records(activity_records)
                params["msgs"].extend(result_3["msgs"])
                params["file_infos"].append(result_3["file_info"])
        return render_template(template_path, **params)

    # POST
    if request.method == "POST":
        method = request.form["method"]
        print("[INFO] %s/%s (%s) [%s] => %s [method=%s]" % (
            current_user.idno, current_user.username, current_user.role, 
            request.method, request.endpoint, method
        ))

        # POST method=search
        if method == "search":
            course_code = request.form["course_code"].strip()
            campus_idno = request.form["campus_idno"].strip()
            params["config"]["search"]["course_code"]["default"] = course_code
            params["config"]["search"]["campus_idno"]["default"] = campus_idno
            # 查询
            if course_code and campus_idno:
                result_1 = course_record_utils.get_record(course_code=course_code, campus_idno=campus_idno)
                params["msgs"].extend(result_1["msgs"])
                if result_1["course_record"]:
                    params["course_records"] = [result_1["course_record"]]
            # 保存 - 课程记录
            if params["course_records"]:
                result_2 = course_record_utils.save_records(params["course_records"])
                params["msgs"].extend(result_2["msgs"])
                params["file_infos"] = [result_2["file_info"]]
                # 保存 - 活动记录
                activity_records = []
                for course_record in params["course_records"]:
                    activity_records.extend(course_record["activity_records"])
                if activity_records:
                    result_3 = activity_record_utils.save_records(activity_records)
                    params["msgs"].extend(result_3["msgs"])
                    params["file_infos"].append(result_3["file_info"])
            return render_template(template_path, **params)

    return render_error_template(message="系统错误")


# 课程管理
# http://127.0.0.1:5000/course/info_for_admin/
# http://127.0.0.1:5000/course/info_for_admin/?course_code=CEC1010
@bp_view_course.route("/info_for_admin/", methods=["GET", "POST"])
@login_required
def info_for_admin():

    # Verify
    if current_user.role not in [UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "course_info_for_admin.html"

    # Params
    course_info_field_headers = course_utils.field_headers
    course_info_field_options = course_utils.field_options
    course_info_default_doc   = course_utils.new_doc
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "search": {
                "course_code": {"placeholder": course_info_field_headers["course_code"],   "default": None, "options": course_info_field_options["course_code"]},
            },
            "course_info": {
                "course_code":    {"header": course_info_field_headers["course_code"],    "fixed": False, "default": course_info_default_doc["course_code"],    "options": course_info_field_options["course_code"]},
                "activity_rules": {"header": course_info_field_headers["activity_rules"], "fixed": False, "default": course_info_default_doc["activity_rules"], "options": None},

                "course_name":    {"header": course_info_field_headers["course_name"],    "fixed": False, "default": course_info_default_doc["course_name"],    "options": None},

                "createtime":     {"header": course_info_field_headers["createtime"],     "fixed": True,  "default": course_info_default_doc["createtime"],     "options": None},
                "modifytime":     {"header": course_info_field_headers["modifytime"],     "fixed": True,  "default": course_info_default_doc["modifytime"],     "options": None},
                "modifyuser":     {"header": course_info_field_headers["modifyuser"],     "fixed": True,  "default": course_info_default_doc["modifyuser"],     "options": None},
            }
        },
        "course_infos": None,
        "file_infos": None,
    }

    # GET
    if request.method == "GET":
        print("[INFO] %s/%s (%s) [%s] => %s" % (
            current_user.idno, current_user.username, current_user.role,
            request.method, request.endpoint
        ))
        course_code = request.args.get("course_code", "").strip()
        params["config"]["search"]["course_code"]["default"] = course_code
        if course_code:
            # 查询
            result_1 = course_utils.get_info(course_code=course_code)
            params["msgs"].extend(result_1["msgs"])
            if result_1["course_info"]:
                params["course_infos"] = [result_1["course_info"]]
            # 保存
            if params["course_infos"]:
                result_2 = course_utils.save_infos(params["course_infos"])
                params["msgs"].extend(result_2["msgs"])
                params["file_infos"] = [result_2["file_info"]]
        return render_template(template_path, **params)

    # POST
    if request.method == "POST":
        method = request.form["method"]
        print("[INFO] %s/%s (%s) [%s] => %s [method=%s]" % (
            current_user.idno, current_user.username, current_user.role, 
            request.method, request.endpoint, method
        ))

        # POST method=search
        if method == "search":
            course_code = request.form["course_code"].strip()
            params["config"]["search"]["course_code"]["default"] = course_code
            if course_code:
                # 查询
                result_1 = course_utils.get_info(course_code=course_code)
                params["msgs"].extend(result_1["msgs"])
                if result_1["course_info"]:
                    params["course_infos"] = [result_1["course_info"]]
                # 保存
                if params["course_infos"]:
                    result_2 = course_utils.save_infos(params["course_infos"])
                    params["msgs"].extend(result_2["msgs"])
                    params["file_infos"] = [result_2["file_info"]]
            return render_template(template_path, **params)

        # POST method=update
        if method == "update":
            new_course_info = {key: val.strip() for key, val in request.form.items()}
            new_course_info.pop("method")
            old_course_code = new_course_info.pop("old_course_code")
            # 更新
            result_1 = course_utils.update_info(new_course_info=new_course_info, old_course_code=old_course_code)
            params["msgs"].extend(result_1["msgs"])
            if params["msgs"][-1]["type"] == "success":
                course_code = new_course_info["course_code"]
            else:
                course_code = old_course_code
            params["config"]["search"]["course_code"]["default"] = course_code
            # 查询
            result_2 = course_utils.get_info(course_code=course_code)
            params["msgs"].extend(result_2["msgs"])
            if result_2["course_info"]:
                params["course_infos"] = [result_2["course_info"]]
            # 保存
            if params["course_infos"]:
                result_3 = course_utils.save_infos(params["course_infos"])
                params["msgs"].extend(result_3["msgs"])
                params["file_infos"] = [result_3["file_info"]]
            # 更新选项
            course_info_field_options = course_utils.field_options
            for __field in params["config"]["search"]:
                if params["config"]["search"][__field]["options"] is not None:
                    params["config"]["search"][__field]["options"] = course_info_field_options[__field]
            for __field in params["config"]["course_info"]:
                if params["config"]["course_info"][__field]["options"] is not None:
                    params["config"]["course_info"][__field]["options"] = course_info_field_options[__field]
            return render_template(template_path, **params)

        # POST method=create
        if method == "create":
            new_course_info = {key: val.strip() for key, val in request.form.items()}
            new_course_info.pop("method")
            # 新增
            result_1 = course_utils.create_info(new_course_info=new_course_info)
            params["msgs"].extend(result_1["msgs"])
            if params["msgs"][-1]["type"] == "success":
                course_code = new_course_info["course_code"]
                params["config"]["search"]["course_code"]["default"] = course_code
                # 查询
                result_2 = course_utils.get_info(course_code=course_code)
                params["msgs"].extend(result_2["msgs"])
                if result_2["course_info"]:
                    params["course_infos"] = [result_2["course_info"]]
                 # 保存
                if params["course_infos"]:
                    result_3 = course_utils.save_infos(params["course_infos"])
                    params["msgs"].extend(result_3["msgs"])
                    params["file_infos"] = [result_3["file_info"]]
                # 更新选项
                course_info_field_options = course_utils.field_options
                for __field in params["config"]["search"]:
                    if params["config"]["search"][__field]["options"] is not None:
                        params["config"]["search"][__field]["options"] = course_info_field_options[__field]
                for __field in params["config"]["course_info"]:
                    if params["config"]["course_info"][__field]["options"] is not None:
                        params["config"]["course_info"][__field]["options"] = course_info_field_options[__field]
            return render_template(template_path, **params)

    return render_error_template(message="系统错误")


# 课程数据
# http://127.0.0.1:5000/course/data/
# http://127.0.0.1:5000/course/data/?course_code=CEC1010
@bp_view_course.route("/data/", methods=["GET", "POST"])
@login_required
def data():

    # Verify
    if current_user.role not in [UserRole.staff, UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "course_data.html"

    # Params
    user_info_field_headers     = user_utils.field_headers
    user_info_field_options     = user_utils.field_options
    course_info_field_headers   = course_utils.field_headers
    course_record_field_headers = course_record_utils.field_headers
    course_record_field_options = course_record_utils.field_options
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "search": {
                "course_code":   {"placeholder": course_record_field_headers["course_code"], "default": None, "options": course_record_field_options["course_code"]},
                "status":        {"placeholder": course_record_field_headers["status"],      "default": None, "options": course_record_field_options["status"]},

                "campus_role":   {"placeholder": user_info_field_headers["campus_role"],          "default": None, "options": user_info_field_options["campus_role"]},
                "campus_type":   {"placeholder": user_info_field_headers["campus_type"],          "default": None, "options": user_info_field_options["campus_type"]},
                "campus_dept":   {"placeholder": user_info_field_headers["campus_dept"],          "default": None, "options": user_info_field_options["campus_dept"]},
                "campus_addr":   {"placeholder": user_info_field_headers["campus_addr"],          "default": None, "options": user_info_field_options["campus_addr"]},
                "campus_year":   {"placeholder": user_info_field_headers["campus_year"],          "default": None, "options": user_info_field_options["campus_year"]},
                "campus_grade":  {"placeholder": user_info_field_headers["campus_grade"],         "default": None, "options": user_info_field_options["campus_grade"]},
                "campus_source": {"placeholder": user_info_field_headers["campus_source"],        "default": None, "options": user_info_field_options["campus_source"]},
                "campus_status": {"placeholder": user_info_field_headers["campus_status"],        "default": None, "options": user_info_field_options["campus_status"]},
            },
            "update": {
                "update_course_info": {
                    "file_name":   "update_course_info_file", 
                    "placeholder": "课程信息.xlsx"
                },
                "update_course_record": {
                    "file_name":   "update_course_record_file", 
                    "placeholder": "课程记录.xlsx"
                },
            },
            "course_info": {
                "course_code":    {"header": course_info_field_headers["course_code"]},
                "course_name":    {"header": course_info_field_headers["course_name"]},
                "activity_rules": {"header": course_info_field_headers["activity_rules"]},
            },
            "course_overview": {
                "num_total":  {"header": "总人数"},
                "num_auth":   {"header": "已认证"},
                "num_done":   {"header": "已完成"},
                "num_doing":  {"header": "进行中"},
                "num_undone": {"header": "未开始"},
            },
            "user_info": {
                "campus_idno":   {"header": user_info_field_headers["campus_idno"],   "width": 5},
                "name":          {"header": user_info_field_headers["name"],          "width": 5},

                "campus_role":   {"header": user_info_field_headers["campus_role"],   "width": 5},
                "campus_type":   {"header": user_info_field_headers["campus_type"],   "width": 5},
                "campus_dept":   {"header": user_info_field_headers["campus_dept"],   "width": 5},
                "campus_addr":   {"header": user_info_field_headers["campus_addr"],   "width": 5},
                "campus_year":   {"header": user_info_field_headers["campus_year"],   "width": 5},
                "campus_grade":  {"header": user_info_field_headers["campus_grade"],  "width": 5},
                "campus_source": {"header": user_info_field_headers["campus_source"], "width": 5},
                "campus_status": {"header": user_info_field_headers["campus_status"], "width": 5},
            },
            "course_record": {
                # "course_code":   {"header": course_record_field_headers["course_code"],   "width": 5},
                # "campus_idno":   {"header": course_record_field_headers["campus_idno"],   "width": 5},

                "status":        {"header": course_record_field_headers["status"],        "width": 5},
                "activity_done": {"header": course_record_field_headers["activity_done"], "width": 5},
                "authen":        {"header": course_record_field_headers["authen"],        "width": 5},

                "note":          {"header": course_record_field_headers["note"],          "width": 5},

                # "createtime":    {"header": course_record_field_headers["createtime"],    "width": 5},
                # "modifytime":    {"header": course_record_field_headers["modifytime"],    "width": 5},
                # "modifyuser":    {"header": course_record_field_headers["modifyuser"],    "width": 5},
            },
            "display_limit": 200
        },
        "course_infos": None,
        "file_infos": None,
    }

    # GET
    if request.method == "GET":
        print("[INFO] %s/%s (%s) [%s] => %s" % (
            current_user.idno, current_user.username, current_user.role,
            request.method, request.endpoint
        ))
        course_code = request.args.get("course_code", "").strip()
        params["config"]["search"]["course_code"]["default"] = course_code
        if course_code:
            # 查询
            result_1 = course_utils.get_info_with_detail(course_code=course_code)
            params["msgs"].extend(result_1["msgs"])
            if result_1["course_info"]:
                params["course_infos"] = [result_1["course_info"]]
            # 保存 - 课程信息
            if params["course_infos"]:
                result_2 = course_utils.save_infos(params["course_infos"])
                params["msgs"].extend(result_2["msgs"])
                params["file_infos"] = [result_2["file_info"]]
                # 保存 - 课程记录
                course_records = []
                for course_info in params["course_infos"]:
                    course_records.extend(course_info["course_records"])
                if course_records:
                    result_3 = course_record_utils.save_records(course_records)
                    params["msgs"].extend(result_3["msgs"])
                    params["file_infos"].append(result_3["file_info"])
                    result_4 = course_record_utils.save_records_with_detail(course_records)
                    params["msgs"].extend(result_4["msgs"])
                    params["file_infos"].append(result_4["file_info"])
        return render_template(template_path, **params)

    # POST
    if request.method == "POST":
        method = request.form["method"]
        print("[INFO] %s/%s (%s) [%s] => %s [method=%s]" % (
            current_user.idno, current_user.username, current_user.role, 
            request.method, request.endpoint, method
        ))

        # POST method=search
        if method == "search":
            course_code = request.form["course_code"].strip()
            field_filters = {
                "course_record": {
                    "status": request.form["status"].strip(),
                },
                "user_info": {
                    "campus_role":   request.form["campus_role"].strip(),
                    "campus_type":   request.form["campus_type"].strip(),
                    "campus_dept":   request.form["campus_dept"].strip(),
                    "campus_addr":   request.form["campus_addr"].strip(),
                    "campus_year":   request.form["campus_year"].strip(),
                    "campus_grade":  request.form["campus_grade"].strip(),
                    "campus_source": request.form["campus_source"].strip(),
                    "campus_status": request.form["campus_status"].strip(),
                }               
            }
            field_filters["course_record"] = {key: val for key, val in field_filters["course_record"].items() if val}
            field_filters["user_info"]     = {key: val for key, val in field_filters["user_info"].items()     if val}
            for __field, __value in field_filters["course_record"].items():
                params["config"]["search"][__field]["default"] = __value
            for __field, __value in field_filters["user_info"].items():
                params["config"]["search"][__field]["default"] = __value
            params["config"]["search"]["course_code"]["default"] = course_code
            if course_code:
                # 查询
                result_1 = course_utils.get_info_with_detail(course_code=course_code, field_filters=field_filters)
                params["msgs"].extend(result_1["msgs"])
                if result_1["course_info"]:
                    params["course_infos"] = [result_1["course_info"]]
                # 保存 - 课程信息
                if params["course_infos"]:
                    result_2 = course_utils.save_infos(params["course_infos"])
                    params["msgs"].extend(result_2["msgs"])
                    params["file_infos"] = [result_2["file_info"]]
                    # 保存 - 课程记录
                    course_records = []
                    for course_info in params["course_infos"]:
                        course_records.extend(course_info["course_records"])
                    if course_records:
                        result_3 = course_record_utils.save_records(course_records)
                        params["msgs"].extend(result_3["msgs"])
                        params["file_infos"].append(result_3["file_info"])
                        result_4 = course_record_utils.save_records_with_detail(course_records)
                        params["msgs"].extend(result_4["msgs"])
                        params["file_infos"].append(result_4["file_info"])
            return render_template(template_path, **params)

        # POST method=update_course_info
        if method == "update_course_info":
            file_name = params["config"]["update"][method]["file_name"]
            update_file = request.files[file_name]
            if update_file:
                result = course_utils.update_info_by_file(update_file)
                params["msgs"].extend(result["msgs"])
            return render_template(template_path, **params)

        # POST method=update_course_record
        if method == "update_course_record":
            file_name = params["config"]["update"][method]["file_name"]
            update_file = request.files[file_name]
            if update_file:
                result = course_record_utils.update_record_by_file(update_file)
                params["msgs"].extend(result["msgs"])
            return render_template(template_path, **params)

    return render_error_template(message="系统错误")
