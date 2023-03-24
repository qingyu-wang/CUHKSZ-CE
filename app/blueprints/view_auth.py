import datetime

from flask import Blueprint
from flask import redirect, url_for
from flask import render_template, request
from flask_login import login_required, current_user
from flask_login import login_user, logout_user

from ..utils.utils_auth import FlaskUser, UserRole, auth_utils
from ..utils.utils_error import render_error_template
from ..utils.utils_index import get_nav


bp_view_auth = Blueprint("view_auth", __name__)


# 登录
# http://127.0.0.1:5000/auth/login/
@bp_view_auth.route("/login/", methods=["GET", "POST"])
def login():

    # Template
    template_path = "auth_login.html"

    # Params
    params = {
        "nav":  get_nav(),
        "msgs": []
    }

    # GET
    if request.method == "GET":
        return render_template(template_path, **params)

    # POST
    if request.method == "POST":
        method = request.form["method"]

        # POST method=login
        if method == "login":
            auth_username = request.form.get("username").strip()
            auth_password = request.form.get("password").strip()

            result = auth_utils.login_account(
                auth_username=auth_username,
                auth_password=auth_password
            )
            params["msgs"].extend(result["msgs"])
            if result["msgs"][0]["type"] == "success":
                flask_user = FlaskUser(auth_user=result["auth_user"])
                login_user(flask_user)
                return redirect(url_for("view_index.index"))

            return render_template(template_path, **params)

    return render_error_template(message="系统错误")


# 注册
# http://127.0.0.1:5000/auth/signup/
@bp_view_auth.route("/signup/", methods=["GET", "POST"])
def signup():

    # Template
    template_path = "auth_signup.html"

    # Params
    params = {
        "nav":  get_nav(),
        "msgs": []
    }

    # GET /signup/
    if request.method == "GET":
        return render_template(template_path, **params)

    # POST
    if request.method == "POST":
        method = request.form["method"]

        # POST method=signup
        if method == "signup":
            auth_username   = request.form.get("username").strip()
            auth_password_1 = request.form.get("password_1").strip()
            auth_password_2 = request.form.get("password_2").strip()

            result = auth_utils.signup_account(
                auth_username=auth_username,
                auth_password_1=auth_password_1,
                auth_password_2=auth_password_2
            )
            params["msgs"].extend(result["msgs"])
            if result["msgs"][0]["type"] == "success":
                flask_user = FlaskUser(auth_user=result["auth_user"])
                login_user(flask_user)
                return redirect(url_for("view_index.index"))

            return render_template(template_path, **params)

    return render_error_template(message="系统错误")


# 账户
# http://127.0.0.1:5000/auth/account/
@bp_view_auth.route("/account/", methods=["GET", "POST"])
@login_required
def account():

    # Verify
    if current_user.role not in auth_utils.field_role_options:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "auth_account.html"

    # Params
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "auth_headers": auth_utils.field_headers
        }
    }

    # GET
    if request.method == "GET":
        return render_template(template_path, **params)

    # POST
    if request.method == "POST":
        method = request.form["method"]

        # POST method=update
        if method == "update":
            auth_idno           = request.form["idno"]
            auth_username_new   = request.form["username_new"]
            auth_password_new_1 = request.form["password_new_1"]
            auth_password_new_2 = request.form["password_new_2"]

            if auth_username_new or auth_password_new_1 or auth_password_new_2:
                result = auth_utils.update_account(
                    auth_idno=auth_idno,
                    auth_username_new=auth_username_new,
                    auth_password_new_1=auth_password_new_1,
                    auth_password_new_2=auth_password_new_2
                )
                params["msgs"].extend(result["msgs"])
                logout_user()
                flask_user = FlaskUser(auth_user=result["auth_user"])
                login_user(flask_user)

            return render_template(template_path, **params)

    return render_error_template(message="系统错误")


# 登出
# http://127.0.0.1:5000/auth/logout/
@bp_view_auth.route("/logout/", methods=["GET"])
@login_required
def logout():

    # Verify
    if current_user.role not in auth_utils.field_role_options:
        return render_error_template(message="您没有权限访问")

    # GET
    if request.method == "GET":
        logout_user()
        return redirect(url_for("view_index.index"))

    return render_error_template(message="系统错误")


# 管理权限
# http://127.0.0.1:5000/auth/role/
@bp_view_auth.route("/role/", methods=["GET", "POST"])
@login_required
def role():

    # Verify
    if current_user.role not in [UserRole.admin]:
        return render_error_template(message="您没有权限访问")

    # Template
    template_path = "auth_role.html"

    # Params
    params = {
        "nav": get_nav(),
        "msgs": [],
        "config": {
            "auth_role_options": auth_utils.field_role_options,
            "auth_role_headers": auth_utils.field_role_headers
        },
        "auth_role_infos": {},
    }

    # GET
    if request.method == "GET":
        params["auth_role_infos"] = auth_utils.get_role_infos()
        return render_template(template_path, **params)

    # POST
    if request.method == "POST":
        method = request.form["method"]

        # POST method=update
        if method == "update":
            auth_idno     = request.form["auth_idno"]
            auth_role_new = request.form["auth_role_new"]

            if auth_idno or auth_role_new:
                result = auth_utils.update_role(
                    auth_idno=auth_idno, 
                    auth_role_new=auth_role_new
                )
                params["msgs"].extend(result["msgs"])

            params["auth_role_infos"] = auth_utils.get_role_infos()
            return render_template(template_path, **params)

    return render_error_template(message="系统错误")
