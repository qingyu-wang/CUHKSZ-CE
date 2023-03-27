import datetime
import os

from flask import Blueprint
from flask import render_template, request
from flask import send_file, send_from_directory
from flask_login import login_required, current_user

from ..utils.utils_auth import UserRole
from ..utils.utils_error import render_error_template
from ..utils.utils_file import file_utils
from ..utils.utils_index import get_nav
from ..utils.utils_tool_dakaji import search_dakaji, preprocess_dakaji
from ..utils.utils_tool_tencent import preprocess_tencent
from ..utils.utils_tool_wenjuanxing_1 import preprocess_wenjuanxing_1
from ..utils.utils_tool_wenjuanxing_2 import preprocess_wenjuanxing_2
from ..utils.utils_tool_zoom import preprocess_zoom


bp_view_tool = Blueprint("view_tool", __name__)


# 文件
# http://127.0.0.1:5000/tool/file/
@bp_view_tool.route("/file/", methods=["GET", "POST"])
def file():

    # GET
    if request.method == "GET":
        method    = request.args["method"]
        file_dir  = request.args["file_dir"]
        file_name = request.args["file_name"]
        save_name = request.args.get("save_name", file_name)

        # GET method=send_from_directory
        if method == "send_from_directory":
            return send_from_directory(directory=file_dir, path=file_name)

        # GET method=send_file
        if method == "send_file":
            file_path = file_utils.get_path(file_dir, file_name)
            if os.path.isfile(file_path):
                return send_file(file_path, download_name=save_name)
            else:
                return render_error_template(message="文件不存在 [ file_dir=%s, file_name=%s ]" % (file_dir, file_name))

    # POST
    if request.method == "POST":
        method    = request.form["method"]
        file_dir  = request.form["file_dir"]
        file_name = request.form["file_name"]
        save_name = request.form.get("save_name", file_name)

        # POST method=send_from_directory
        if method == "send_from_directory":
            return send_from_directory(directory=file_dir, path=file_name)

        # POST method=send_file
        if method == "send_file":
            file_path = file_utils.get_path(file_dir, file_name)
            if os.path.isfile(file_path):
                return send_file(file_path, download_name=save_name)
            else:
                return render_error_template(message="文件不存在 [ file_dir=%s, file_name=%s ]" % (file_dir, file_name))


# 问卷星
# http://127.0.0.1:5000/tool/wenjuanxing/
@bp_view_tool.route("/wenjuanxing/", methods=["GET", "POST"])
@login_required
def wenjuanxing():

    # Verify
    if current_user.role not in [UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "tool_wenjuanxing.html"

    # Params
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "upload": {
                "upload_wenjuanxing_1": {
                    "file_name":   "upload_file_1",
                    "placeholder": "问卷星 报名表 (格式 1).xlsx",
                    "image":       "tool_utils-wenjuanxing-unprocessed-1.png",
                },
                "upload_wenjuanxing_2": {
                    "file_name":   "upload_file_2",
                    "placeholder": "问卷星 报名表 (格式 2).xlsx",
                    "image":       "tool_utils-wenjuanxing-unprocessed-2.png",
                },
            },
        },
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

        # POST method=upload_wenjuanxing_1 or method=upload_wenjuanxing_2
        if method in ["upload_wenjuanxing_1", "upload_wenjuanxing_2"]:
            preprocess_wenjuanxings = {
                "upload_wenjuanxing_1": preprocess_wenjuanxing_1,
                "upload_wenjuanxing_2": preprocess_wenjuanxing_2,
            }
            file_name = params["config"]["upload"][method]["file_name"]
            preprocess_wenjuanxing = preprocess_wenjuanxings[method]
            upload_file = request.files[file_name]
            if upload_file:
                # 保存文件
                date_info = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_dir = "temp_dir"
                file_name = "tool_utils-wenjuanxing-%s.xlsx" % date_info
                save_name = "问卷星-%s.xlsx" % date_info
                upload_path   = "%s/%s" % (file_utils.temp_dir, file_name.replace(".xlsx", "-unprocessed.xlsx"))
                download_path = "%s/%s" % (file_utils.temp_dir, file_name)
                upload_file.save(upload_path)
                # 处理文件
                result = preprocess_wenjuanxing(upload_path, download_path)
                params["msgs"].extend(result["msgs"])
                if params["msgs"][-1]["type"] == "success":
                    params["file_infos"] = [{"file_dir": file_dir, "file_name": file_name, "save_name": save_name}]
            return render_template(template_path, **params)

    return render_error_template(message="系统错误")


# Zoom
# http://127.0.0.1:5000/tool/zoom/
@bp_view_tool.route("/zoom/", methods=["GET", "POST"])
@login_required
def zoom():

    # Verify
    if current_user.role not in [UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "tool_zoom.html"

    # Params
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "upload": {
                "upload_zoom": {
                    "file_name":   "upload_file",
                    "placeholder": "Zoom 签到表.xlsx",
                    "image":       "tool_utils-zoom-unprocessed.png",
                },
            }
        },
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

        # POST method=upload_zoom
        if method == "upload_zoom":
            file_name = params["config"]["upload"][method]["file_name"]
            upload_file = request.files[file_name]
            if upload_file:
                # 保存文件
                date_info = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_dir = "temp_dir"
                file_name = "tool_utils-zoom-%s.xlsx" % date_info
                save_name = "Zoom-%s.xlsx" % date_info
                upload_path   = "%s/%s" % (file_utils.temp_dir, file_name.replace(".xlsx", "-unprocessed.xlsx"))
                download_path = "%s/%s" % (file_utils.temp_dir, file_name)
                upload_file.save(upload_path)
                # 处理文件
                result = preprocess_zoom(upload_path, download_path)
                params["msgs"].extend(result["msgs"])
                if params["msgs"][-1]["type"] == "success":
                    params["file_infos"] = [{"file_dir": file_dir, "file_name": file_name, "save_name": save_name}]
            return render_template(template_path, **params)

    return render_error_template(message="系统错误")


# 腾讯会议
# http://127.0.0.1:5000/tool/tencent/
@bp_view_tool.route("/tencent/", methods=["GET", "POST"])
@login_required
def tencent():

    # Verify
    if current_user.role not in [UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "tool_tencent.html"

    # Params
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "upload": {
                "upload_tencent": {
                    "file_name":   "upload_file",
                    "placeholder": "腾讯会议 签到表.xlsx",
                    "image":       "tool_utils-tencent-unprocessed.png",
                },
            }
        },
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

        # POST method=upload_tencent
        if method == "upload_tencent":
            file_name = params["config"]["upload"][method]["file_name"]
            upload_file = request.files[file_name]
            if upload_file:
                # 保存文件
                date_info = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_dir = "temp_dir"
                file_name = "tool_utils-tencent-%s.xlsx" % date_info
                save_name = "腾讯会议-%s.xlsx" % date_info
                upload_path   = "%s/%s" % (file_utils.temp_dir, file_name.replace(".xlsx", "-unprocessed.xlsx"))
                download_path = "%s/%s" % (file_utils.temp_dir, file_name)
                upload_file.save(upload_path)
                # 处理文件
                result = preprocess_tencent(upload_path, download_path)
                params["msgs"].extend(result["msgs"])
                if params["msgs"][-1]["type"] == "success":
                    params["file_infos"] = [{"file_dir": file_dir, "file_name": file_name, "save_name": save_name}]
            return render_template(template_path, **params)

    return render_error_template(message="系统错误")


# 打卡机
# http://127.0.0.1:5000/tool/dakaji/
@bp_view_tool.route("/dakaji/", methods=["GET", "POST"])
@login_required
def dakaji():

    # Verify
    if current_user.role not in [UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "tool_dakaji.html"

    # Params
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "search": {
                "search_info": {
                    "title": "查询会议",
                    "default": None,
                    "placeholder": "输入关键词即可",
                    "name": "search_word"
                },
                "search_data": {
                    "title": "查询数据",
                    "default": None,
                    "placeholder": "输入完整会议名",
                    "name": "search_name"
                },
            }
        },
        "meeting_infos": None,
        "file_infos": None,
    }

    # GET
    if request.method == "GET":
        print("[INFO] %s %s/%s (%s) [%s] => %s" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role,
            request.method, request.endpoint
        ))

        # GET method=search_data
        if request.args.get("method") == "search_data":
            search_name = request.args["search_name"]
            if search_name:
                params["config"]["search"]["search_data"]["default"] = search_name
                date_info = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_dir = "temp_dir"
                file_name = "tool_utils-dakaji-%s.xlsx" % date_info
                save_name = "打卡机-%s.xlsx" % date_info
                download_path = "%s/%s" % (file_utils.temp_dir, file_name)
                # 处理文件
                result = preprocess_dakaji(search_text=search_name, save_path=download_path)
                params["msgs"].extend(result["msgs"])
                if params["msgs"][-1]["type"] == "success":
                    params["file_infos"] = [{"file_dir": file_dir, "file_name": file_name, "save_name": save_name}]

        return render_template(template_path, **params)

    # POST
    if request.method == "POST":
        method = request.form["method"]
        print("[INFO] %s %s/%s (%s) [%s] => %s [method=%s]" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role, 
            request.method, request.endpoint, method
        ))

        # POST method=search_info
        if method == "search_info":
            search_word = request.form["search_word"]
            if search_word:
                params["config"]["search"]["search_info"]["default"] = search_word
                params["meeting_infos"] = search_dakaji(search_text=search_word)
            return render_template(template_path, **params)

        # POST method=search_data
        if method == "search_data":
            search_name = request.form["search_name"]
            if search_name:
                params["config"]["search"]["search_data"]["default"] = search_name
                date_info = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_dir = "temp_dir"
                file_name = "tool_utils-dakaji-%s.xlsx" % date_info
                save_name = "打卡机-%s.xlsx" % date_info
                download_path = "%s/%s" % (file_utils.temp_dir, file_name)
                # 处理文件
                result = preprocess_dakaji(search_text=search_name, save_path=download_path)
                params["msgs"].extend(result["msgs"])
                if params["msgs"][-1]["type"] == "success":
                    params["file_infos"] = [{"file_dir": file_dir, "file_name": file_name, "save_name": save_name}]
            return render_template(template_path, **params)

    return render_error_template(message="系统错误")


# 数据结构
# http://127.0.0.1:5000/tool/data_structure/
@bp_view_tool.route("/data_structure/", methods=["GET"])
@login_required
def data_structure():

    # Verify
    if current_user.role not in [UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "tool_data_structure.html"

    # Params
    params = {
        "nav": get_nav(),
        "msgs": [],
        "image_infos": [
            {
                "name": "数据库关系",
                "path": "data structure 1 database link.png",
                "width": 564 # width 1125
            },
            {
                "name": "更新 活动进度 (课程记录)",
                "path": "data structure 2 auto update course_record-activity_done.png",
                "width": 622 # width 1243
            },
            {
                "name": "更新 状态 (课程记录)",
                "path": "data structure 3 auto update course_record-status.png",
                "width": 712 # width 1425
            },
        ],
    }

    # GET
    if request.method == "GET":
        print("[INFO] %s %s/%s (%s) [%s] => %s" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            current_user.idno, current_user.username, current_user.role,
            request.method, request.endpoint
        ))
        return render_template(template_path, **params)

    return render_error_template(message="系统错误")
