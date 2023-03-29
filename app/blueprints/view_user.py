import datetime

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


bp_view_user = Blueprint("view_user", __name__)


# 人员信息
# http://127.0.0.1:5000/user/info/
# http://127.0.0.1:5000/user/info/?campus_idno=121090568
# http://127.0.0.1:5000/user/info/?name=王鑫豪
# http://127.0.0.1:5000/user/info/?campus_idno=121090568&ame=王鑫豪
@bp_view_user.route("/info/", methods=["GET", "POST"])
@login_required
def info():

    # Verify
    if current_user.role not in [UserRole.staff, UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "user_info.html"

    # Params
    user_info_field_headers       = user_utils.field_headers
    course_info_field_headers     = course_utils.field_headers
    course_record_field_headers   = course_record_utils.field_headers
    activity_info_field_headers   = activity_utils.field_headers
    activity_record_field_headers = activity_record_utils.field_headers
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "search": {
                "campus_idno": {"placeholder": user_info_field_headers["campus_idno"], "default": None},
                "name":        {"placeholder": user_info_field_headers["name"],        "default": None},
            },
            "user_info": {
                "campus_idno":   {"header": user_info_field_headers["campus_idno"]},
                "campus_role":   {"header": user_info_field_headers["campus_role"]},

                "name":          {"header": user_info_field_headers["name"]},
                "campus_type":   {"header": user_info_field_headers["campus_type"]},
                "campus_dept":   {"header": user_info_field_headers["campus_dept"]},
                "campus_addr":   {"header": user_info_field_headers["campus_addr"]},
                "campus_year":   {"header": user_info_field_headers["campus_year"]},
                "campus_grade":  {"header": user_info_field_headers["campus_grade"]},
                "campus_source": {"header": user_info_field_headers["campus_source"]},
                "campus_status": {"header": user_info_field_headers["campus_status"]},
            },
            "course_info": {
                "course_code":    {"header": course_info_field_headers["course_code"],    "width": 10},
                "course_name":    {"header": course_info_field_headers["course_name"],    "width": 20},
                "activity_rules": {"header": course_info_field_headers["activity_rules"], "width": 35},

                # "createtime":     {"header": course_info_field_headers["createtime"],     "width": 10},
                # "modifytime":     {"header": course_info_field_headers["modifytime"],     "width": 10},
                # "modifyuser":     {"header": course_info_field_headers["modifyuser"],     "width": 10},
            },
            "course_record": {
                # "course_code":   {"header": course_record_field_headers["course_code"],   "width": 5},
                # "campus_idno":   {"header": course_record_field_headers["campus_idno"],   "width": 5},

                "status":        {"header": course_record_field_headers["status"],        "width": 5},
                "activity_done": {"header": course_record_field_headers["activity_done"], "width": 35},
                "authen":        {"header": course_record_field_headers["authen"],        "width": 5},

                "note":          {"header": course_record_field_headers["note"],          "width": 5},

                # "createtime":    {"header": course_record_field_headers["createtime"],    "width": 5},
                # "modifytime":    {"header": course_record_field_headers["modifytime"],    "width": 5},
                # "modifyuser":    {"header": course_record_field_headers["modifyuser"],    "width": 5},
            },
            "activity_info": {
                # "course_code":    {"header": activity_info_field_headers["course_code"],    "width": 5},
                "activity_code":  {"header": activity_info_field_headers["activity_code"],    "width": 20},
                "activity_type":  {"header": activity_info_field_headers["activity_type"],    "width": 10},

                # "activity_name":  {"header": activity_info_field_headers["activity_name"],    "width": 5},
                # "activity_note":  {"header": activity_info_field_headers["activity_note"],    "width": 5},
                # "activity_quota": {"header": activity_info_field_headers["activity_quota"],    "width": 5},

                # "activity_year":  {"header": activity_info_field_headers["activity_year"],    "width": 5},
                # "activity_term":  {"header": activity_info_field_headers["activity_term"],    "width": 5},
                "activity_date":  {"header": activity_info_field_headers["activity_date"],    "width": 10},

                # "createtime":     {"header": activity_info_field_headers["createtime"],    "width": 5},
                # "modifytime":     {"header": activity_info_field_headers["modifytime"],    "width": 5},
                # "modifyuser":     {"header": activity_info_field_headers["modifyuser"],    "width": 5},
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
                "note":          {"header": activity_record_field_headers["note"],          "width": 40},

                # "createtime":    {"header": activity_record_field_headers["createtime"],    "width": 5},
                # "modifytime":    {"header": activity_record_field_headers["modifytime"],    "width": 5},
                # "modifyuser":    {"header": activity_record_field_headers["modifyuser"],    "width": 5},
            },
        },
        "user_infos": None,
        "file_infos": None,
    }

    # GET
    if request.method == "GET":
        print("[INFO] %s %s/%s (%s) [%s] => %s" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role,
            request.method, request.endpoint
        ))
        campus_idno = request.args.get("campus_idno", "").strip()
        name        = request.args.get("name", "").strip()
        if campus_idno:
            params["config"]["search"]["campus_idno"]["default"] = campus_idno
            result = user_utils.get_info_by_campus_idno_with_detail(campus_idno=campus_idno)
            params["msgs"].extend(result["msgs"])
            if result["user_info"]:
                params["user_infos"] = [result["user_info"]]
        elif name:
            params["config"]["search"]["name"]["default"] = name
            result = user_utils.get_infos_by_name(name=name)
            params["msgs"].extend(result["msgs"])
            params["user_infos"] = result["user_infos"]
            if params["user_infos"]:
                params["msgs"].append({
                    "type": "success",
                    "text": "\"修读详情\" 请使用 \"校园卡号\" 查询"
                })
        return render_template(template_path, **params)

    # POST
    if request.method == "POST":
        method = request.form["method"]
        print("[INFO] %s %s/%s (%s) [%s] => %s [method=%s]" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role,
            request.method, request.endpoint, method
        ))

        # POST method=search_idno
        if method == "search_idno":
            campus_idno = request.form["campus_idno"].strip()
            if campus_idno:
                params["config"]["search"]["campus_idno"]["default"] = campus_idno
                result_1 = user_utils.get_info_by_campus_idno_with_detail(campus_idno=campus_idno)
                params["msgs"].extend(result_1["msgs"])
                if result_1["user_info"]:
                    params["user_infos"] = [result_1["user_info"]]
                # 保存 - 活动信息
                if params["user_infos"]:
                    course_records = []
                    activity_records = []
                    for __user_info in params["user_infos"]:
                        __course_records = __user_info.get("course_records", [])
                        course_records.extend(__course_records)
                        for __course_record in __course_records:
                            __activity_records = __course_record.get("activity_records", [])
                            activity_records.extend(__activity_records)
                    if course_records:
                        result_2 = course_record_utils.save_records(course_records)
                        params["msgs"].extend(result_2["msgs"])
                        params["file_infos"] = [result_2["file_info"]]
                    if activity_records:
                        result_4 = activity_record_utils.save_records(activity_records)
                        params["msgs"].extend(result_4["msgs"])
                        params["file_infos"].append(result_4["file_info"])
            return render_template(template_path, **params)

        # POST method=search_name
        if method == "search_name":
            name = request.form["name"].strip()
            if name:
                params["config"]["search"]["name"]["default"] = name
                result = user_utils.get_infos_by_name(name=name)
                params["msgs"].extend(result["msgs"])
                params["user_infos"] = result["user_infos"]
                if params["user_infos"]:
                    params["msgs"].append({
                        "type": "success",
                        "text": "\"修读详情\" 请使用 \"校园卡号\" 查询"
                    })
            return render_template(template_path, **params)

    return render_error_template(message="系统错误")


# 人员管理
# http://127.0.0.1:5000/user/info_for_admin/
# http://127.0.0.1:5000/user/info_for_admin/?campus_idno=121090568
# http://127.0.0.1:5000/user/info_for_admin/?name=王鑫豪
# http://127.0.0.1:5000/user/info_for_admin/?campus_idno=121090568&ame=王鑫豪
@bp_view_user.route("/info_for_admin/", methods=["GET", "POST"])
@login_required
def info_for_admin():

    # Verify
    if current_user.role not in [UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "user_info_for_admin.html"

    # Params
    user_info_field_headers    = user_utils.field_headers
    user_info_field_options    = user_utils.field_options
    user_update_by_oracle_info = user_utils.get_updatetime_by_oracle()
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "search": {
                "campus_idno":  {"placeholder": user_info_field_headers["campus_idno"], "default": None},
                "name":         {"placeholder": user_info_field_headers["name"],        "default": None},
            },
            "user_info": {
                "campus_idno":      {"header": user_info_field_headers["campus_idno"],   "fixed": True,  "options": None},
                "campus_role":      {"header": user_info_field_headers["campus_role"],   "fixed": True,  "options": None},

                "name":             {"header": user_info_field_headers["name"],          "fixed": False, "options": None},
                "campus_type":      {"header": user_info_field_headers["campus_type"],   "fixed": False, "options": user_info_field_options["campus_type"]},
                "campus_dept":      {"header": user_info_field_headers["campus_dept"],   "fixed": False, "options": user_info_field_options["campus_dept"]},
                "campus_addr":      {"header": user_info_field_headers["campus_addr"],   "fixed": False, "options": user_info_field_options["campus_addr"]},
                "campus_year":      {"header": user_info_field_headers["campus_year"],   "fixed": False, "options": user_info_field_options["campus_year"]},
                "campus_grade":     {"header": user_info_field_headers["campus_grade"],  "fixed": False, "options": user_info_field_options["campus_grade"]},
                "campus_source":    {"header": user_info_field_headers["campus_source"], "fixed": False, "options": user_info_field_options["campus_source"]},
                "campus_status":    {"header": user_info_field_headers["campus_status"], "fixed": False, "options": user_info_field_options["campus_status"]},

                "idno":             {"header": user_info_field_headers["idno"],          "fixed": False, "options": None},
                "sex":              {"header": user_info_field_headers["sex"],           "fixed": False, "options": user_info_field_options["sex"]},
                "bankacc":          {"header": user_info_field_headers["bankacc"],       "fixed": False, "options": None},
                "phoneno":          {"header": user_info_field_headers["phoneno"],       "fixed": False, "options": None},

                "createtime":       {"header": user_info_field_headers["createtime"],    "fixed": True,  "options": None},
                "modifytime":       {"header": user_info_field_headers["modifytime"],    "fixed": True,  "options": None},
                "modifyuser":       {"header": user_info_field_headers["modifyuser"],    "fixed": True,  "options": None},
            }
        },
        "user_infos": None,
        "file_infos": None,
        "extra_infos": [
            "系统数据定期更新 (不会覆盖锁定字段)\n\n[最近更新] %s\n[预计更新] %s" % (
                user_update_by_oracle_info["updatetime"].strftime("%Y-%m-%d %H:%M:%S"),
                user_update_by_oracle_info["nextruntime"].strftime("%Y-%m-%d %H:%M:%S")
            )
        ]
    }

    # GET
    if request.method == "GET":
        print("[INFO] %s %s/%s (%s) [%s] => %s" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role,
            request.method, request.endpoint
        ))
        campus_idno = request.args.get("campus_idno", "").strip()
        name = request.args.get("name", "").strip()
        if campus_idno:
            print("[INFO] %s %s/%s (%s) [%s] => %s [method=%s, campus_idno=%s]" % (
                datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                current_user.idno, current_user.username, current_user.role,
                request.method, request.endpoint, method,
                campus_idno
            ))
            params["config"]["search"]["campus_idno"]["default"] = campus_idno
            result_1 = user_utils.get_info_by_campus_idno(campus_idno=campus_idno)
            params["msgs"].extend(result_1["msgs"])
            if result_1["user_info"]:
                params["user_infos"] = [result_1["user_info"]]
        elif name:
            print("[INFO] %s %s/%s (%s) [%s] => %s [method=%s, name=%s]" % (
                datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                current_user.idno, current_user.username, current_user.role,
                request.method, request.endpoint, method,
                name
            ))
            params["config"]["search"]["name"]["default"] = name
            result_1 = user_utils.get_infos_by_name(name=name)
            params["msgs"].extend(result_1["msgs"])
            params["user_infos"] = result_1["user_infos"]
        # 保存
        if params["user_infos"]:
            result_2 = user_utils.save_infos(params["user_infos"])
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

        # POST method=search_idno
        if method == "search_idno":
            campus_idno = request.form["campus_idno"].strip()
            print("[INFO] %s %s/%s (%s) [%s] => %s [method=%s, campus_idno=%s]" % (
                datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                current_user.idno, current_user.username, current_user.role,
                request.method, request.endpoint, method,
                campus_idno
            ))
            if campus_idno:
                params["config"]["search"]["campus_idno"]["default"] = campus_idno
                result_1 = user_utils.get_info_by_campus_idno(campus_idno=campus_idno)
                params["msgs"].extend(result_1["msgs"])
                if result_1["user_info"]:
                    params["user_infos"] = [result_1["user_info"]]
            # 保存
            if params["user_infos"]:
                result_2 = user_utils.save_infos(params["user_infos"])
                params["msgs"].extend(result_2["msgs"])
                params["file_infos"] = [result_2["file_info"]]
            return render_template(template_path, **params)

        # POST method=search_name
        if method == "search_name":
            name = request.form["name"].strip()
            print("[INFO] %s %s/%s (%s) [%s] => %s [method=%s, name=%s]" % (
                datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                current_user.idno, current_user.username, current_user.role,
                request.method, request.endpoint, method,
                name
            ))
            if name:
                params["config"]["search"]["name"]["default"] = name
                result = user_utils.get_infos_by_name(name=name)
                params["msgs"].extend(result["msgs"])
                params["user_infos"] = result["user_infos"]
            # 保存
            if params["user_infos"]:
                result_2 = user_utils.save_infos(params["user_infos"])
                params["msgs"].extend(result_2["msgs"])
                params["file_infos"] = [result_2["file_info"]]
            return render_template(template_path, **params)

        # POST method=update
        if method == "update":
            new_user_info = {key: val.strip() for key, val in request.form.items()}
            new_user_info.pop("method")
            old_campus_idno = new_user_info.pop("old_campus_idno")
            old_name        = new_user_info.pop("old_name")
            # 更新
            result_1 = user_utils.update_info(new_user_info=new_user_info, old_campus_idno=old_campus_idno)
            params["msgs"].extend(result_1["msgs"])
            if params["msgs"][-1]["type"] == "success":
                campus_idno = new_user_info["campus_idno"]
                name        = new_user_info["name"]
            else:
                campus_idno = old_campus_idno
                name        = old_name
            params["config"]["search"]["campus_idno"]["default"] = campus_idno
            params["config"]["search"]["name"]["default"]        = name
            # 查询
            result_2 = user_utils.get_info_by_campus_idno(campus_idno=campus_idno)
            params["msgs"].extend(result_2["msgs"])
            if result_2["user_info"]:
                params["user_infos"] = [result_2["user_info"]]
            # 保存
            if params["user_infos"]:
                result_3 = user_utils.save_infos(params["user_infos"])
                params["msgs"].extend(result_3["msgs"])
                params["file_info"] = result_3["file_info"]
            # 更新选项
            user_info_field_options = user_utils.field_options
            for __field in params["config"]["user_info"]:
                if params["config"]["user_info"][__field]["options"] is not None:
                    params["config"]["user_info"][__field]["options"] = user_info_field_options[__field]
            return render_template(template_path, **params)

    return render_error_template(message="系统错误")


# 人员数据
# http://127.0.0.1:5000/user/data/
# http://127.0.0.1:5000/user/data?campus_type=1%20本科生&campus_year=2021
@bp_view_user.route("/data", methods=["GET", "POST"])
@login_required
def data():

    # Verify
    if current_user.role not in [UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "user_data.html"

    # Params
    user_info_field_headers = user_utils.field_headers
    user_info_field_options = user_utils.field_options
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "search": {
                "campus_role":   {"placeholder": user_info_field_headers["campus_role"],   "default": None, "options": user_info_field_options["campus_role"]},
                "campus_type":   {"placeholder": user_info_field_headers["campus_type"],   "default": None, "options": user_info_field_options["campus_type"]},
                "campus_dept":   {"placeholder": user_info_field_headers["campus_dept"],   "default": None, "options": user_info_field_options["campus_dept"]},
                "campus_addr":   {"placeholder": user_info_field_headers["campus_addr"],   "default": None, "options": user_info_field_options["campus_addr"]},
                "campus_year":   {"placeholder": user_info_field_headers["campus_year"],   "default": None, "options": user_info_field_options["campus_year"]},
                "campus_grade":  {"placeholder": user_info_field_headers["campus_grade"],  "default": None, "options": user_info_field_options["campus_grade"]},
                "campus_source": {"placeholder": user_info_field_headers["campus_source"], "default": None, "options": user_info_field_options["campus_source"]},
                "campus_status": {"placeholder": user_info_field_headers["campus_status"], "default": None, "options": user_info_field_options["campus_status"]},
            },
            "update": {
                "update_user_info": {
                    "file_name":   "update_user_info_file",
                    "placeholder": "人员信息.xlsx"
                },
            },
            "display_limit": 200
        },
        "user_infos": None,
        "file_infos": None,
    }

    # GET
    if request.method == "GET":
        print("[INFO] %s %s/%s (%s) [%s] => %s" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role,
            request.method, request.endpoint
        ))
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
            field_filters = {
                "campus_role":    request.form["campus_role"].strip(),
                "campus_type":    request.form["campus_type"].strip(),
                "campus_dept":    request.form["campus_dept"].strip(),
                "campus_addr":    request.form["campus_addr"].strip(),
                "campus_year":    request.form["campus_year"].strip(),
                "campus_grade":   request.form["campus_grade"].strip(),
                "campus_source":  request.form["campus_source"].strip(),
                "campus_status":  request.form["campus_status"].strip()
            }
            field_filters = {key: val for key, val in field_filters.items() if val}
            if request.form.get("method") == "search":
                result_1 = user_utils.get_infos(field_filters=field_filters)
                for __field, __value in field_filters.items():
                    params["config"]["search"][__field]["default"] = __value
                params["msgs"].extend(result_1["msgs"])
                params["user_infos"] = result_1["user_infos"]
                # 保存
                if params["user_infos"]:
                    result_2 = user_utils.save_infos(params["user_infos"])
                    params["msgs"].extend(result_2["msgs"])
                    params["file_infos"] = [result_2["file_info"]]
                return render_template(template_path, **params)

        # POST method=update_user_info
        if method == "update_user_info":
            file_name = params["config"]["update"][method]["file_name"]
            update_file = request.files[file_name]
            if update_file:
                result = user_utils.update_info_by_file(update_file)
                params["msgs"].extend(result["msgs"])
            return render_template(template_path, **params)

    return render_error_template(message="系统错误")
