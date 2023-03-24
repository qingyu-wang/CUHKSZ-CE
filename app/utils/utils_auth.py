"""
Utils Auth

# MongoDB 索引
mongo.coll_auth_info.create_index(
    name="index", unique=True, keys=[("idno", 1)] 
)

# Flask Login
current_user attribute              (from flask_login import current_user)
    no login => AnonymousUserMixin  (from flask_login import AnonymousUserMixin)
        is_active => False
        is_authenticated => False
        is_anonymous => True
        get_id => None
    login => FlaskUser              (from utils.utils_auth import FlaskUser)
        is_active = True
        is_authenticated = True
        is_anonymous = False
        get_id => idno
        idno
        role
        username
"""

import datetime

from flask_login import UserMixin, current_user

from .utils_mongo import mongo


class UserRole(object):

    guest = "guest"
    staff = "staff"
    admin = "admin"


class FlaskUser(UserMixin):

    def __init__(self, auth_user):
        self.idno = auth_user["idno"]
        self.role = auth_user["role"]
        self.username = auth_user["username"]
        self.password = auth_user["password"]
        self.createtime = auth_user["createtime"]
        self.modifytime = auth_user["modifytime"]
        self.modifyuser = auth_user["modifyuser"]

    def get_id(self):
        return self.idno


class AuthUtils(object):

    # ---
    # property
    # ---

    @property
    def new_doc(self):
        __new_doc = {
            "idno":       "/",
            "role":       "/",
            "username":   "/",
            "password":   "/",
            "createtime": datetime.datetime.now(),
            "modifytime": None,
            "modifyuser": None
        }
        return __new_doc

    @property
    def field_headers(self):
        __field_headers = {
            "idno":       "ID",
            "role":       "权限",
            "username":   "账号",
            "password":   "密码",
            "createtime": "创建时间",
            "modifytime": "修改时间",
            "modifyuser": "修改用户"
        }
        return __field_headers

    @property
    def field_role_options(self):
        __field_role_options = [i for i in vars(UserRole) if "__" not in i][::-1]
        return __field_role_options

    @property
    def field_role_headers(self):
        __field_role_headers = {
            "guest": "访客",
            "staff": "教工",
            "admin": "管理员"
        }
        return __field_role_headers

    # ---
    # blueprints.view_auth.login
    # ---

    def login_account(
        self,
        auth_username,
        auth_password
    ):
        result = {
            "auth_user": None,
            "msgs": []
        }
        if not auth_username:
            result["msgs"].append({"type": "warn", "text": "请输入账号"})
            return result

        if mongo.coll_auth_info.count_documents({"username": auth_username}) == 0:
            result["msgs"].append({"type": "warn", "text": "账号不存在"})
            return result

        if not auth_password:
            result["msgs"].append({"type": "warn", "text": "请输入密码"})
            return result

        if mongo.coll_auth_info.count_documents({"username": auth_username, "password": auth_password}) == 0:
            result["msgs"].append({"type": "error", "text": "密码错误"})
            return result

        auth_user = mongo.coll_auth_info.find_one({"username": auth_username, "password": auth_password})

        result["msgs"].append({"type": "success", "text": "登录成功"})
        result["auth_user"] = auth_user
        return result

    # ---
    # blueprints.view_auth.signup
    # ---

    def signup_account(
        self,
        auth_username,
        auth_password_1,
        auth_password_2
    ):
        result = {
            "auth_user": None,
            "msgs": []
        }

        if not auth_username:
            result["msgs"].append({"type": "warn", "text": "请输入账号"})
            return result

        if mongo.coll_auth_info.count_documents({"username": auth_username}) != 0:
            result["msgs"].append({"type": "warn", "text": "账号已存在"})
            return result

        if not auth_password_1:
            result["msgs"].append({"type": "warn", "text": "请输入密码"})
            return result

        if not auth_password_2:
            result["msgs"].append({"type": "warn", "text": "请再次输入密码"})
            return result

        if auth_password_1 != auth_password_2:
            result["msgs"].append({"type": "warn", "text": "密码不一致"})
            return result

        guest_idno = mongo.coll_auth_info.count_documents(
            {"idno": {"$regex": "%s_*" % UserRole.guest}}
        ) + 1

        auth_user = auth_utils.new_doc
        auth_user["role"] = "guest"
        auth_user["idno"] = "guest_%03d" % guest_idno
        auth_user["username"] = auth_username
        auth_user["password"] = auth_password_1

        mongo.coll_auth_info.insert_one(auth_user)

        result["msgs"].append({"type": "success", "text": "注册成功"})
        result["auth_user"] = auth_user
        return result

    # ---
    # blueprints.view_auth.account
    # ---

    def update_account(
        self,
        auth_idno,
        auth_username_new,
        auth_password_new_1,
        auth_password_new_2
    ):
        result = {
            "auth_user": None,
            "msgs": []
        }

        # 修改用户名
        if auth_username_new:
            if mongo.coll_auth_info.count_documents({"username": auth_username_new}) != 0:
                result["msgs"].append({"type": "warn", "text": "账号已存在"})
            else:
                mongo.coll_auth_info.update_one(
                    {"idno": auth_idno},
                    {
                        "$set": {
                            "username": auth_username_new,
                            "modifytime": datetime.datetime.now(),
                            "modifyuser": current_user.idno
                        }
                    }
                )
                result["msgs"].append({"type": "success", "text": "账号修改成功"})

        # 修改密码
        if auth_password_new_1 or auth_password_new_2:

            auth_user_old = mongo.coll_auth_info.find_one({"idno": auth_idno})

            if not auth_password_new_1:
                result["msgs"].append({"type": "warn", "text": "请输入新密码"})
            if not auth_password_new_2:
                result["msgs"].append({"type": "warn", "text": "请再次输入新密码"})

            elif auth_password_new_1 == auth_user_old["password"]:
                result["msgs"].append({"type": "warn", "text": "新密码不能与旧密码相同"})
            elif auth_password_new_1 != auth_password_new_2:
                result["msgs"].append({"type": "warn", "text": "新密码不一致"})

            else:
                mongo.coll_auth_info.update_one(
                    {"idno": auth_idno},
                    {
                        "$set": {
                            "password": auth_password_new_1,
                            "modifytime": datetime.datetime.now(),
                            "modifyuser": current_user.idno,
                        }
                    }
                )
                result["msgs"].append({"type": "success", "text": "密码修改成功"})

        auth_user_new = mongo.coll_auth_info.find_one({"idno": auth_idno})

        result["auth_user"] = auth_user_new
        return result

    # ---
    # blueprints.view_auth.role
    # ---

    def get_role_infos(self):
        auth_role_infos = {
            auth_role: list(mongo.coll_auth_info.find({"role": auth_role}).sort([("idno", 1)]))
            for auth_role in self.field_role_options
        }
        return auth_role_infos

    def update_role(self, auth_idno, auth_role_new):
        result = {
            "msgs": [],
        }
        auth_user = mongo.coll_auth_info.find_one({"idno": auth_idno})

        if not auth_user:
            msg = {
                "type": "error",
                "text": "更新失败<br>ID不存在<br>[ %s=\"%s\" ]" % (
                    self.field_headers["idno"], auth_idno,
                )
            }
            result["msgs"].append(msg)
            return result

        auth_role_old = auth_user["role"]

        if not auth_role_new:
            msg = {
                "type": "warn",
                "text": "请选择权限"
            }
            result["msgs"].append(msg)
            return result

        if auth_role_old == auth_role_new:
            msg = {
                "type": "warn",
                "text": "无需改变"
            }
            result["msgs"].append(msg)
            return result

        if current_user.role != UserRole.admin:
            msg = {
                "type": "error",
                "text": "更新失败<br>您无权修改权限"
            }
            result["msgs"].append(msg)
            return result

        if auth_role_old == UserRole.admin and auth_role_new != UserRole.admin:
            if mongo.coll_auth_info.count_documents({"role": UserRole.admin}) == 1:
                msg = {
                    "type": "error",
                    "text": "更新失败<br>请至少保留1名管理员"
                }
                result["msgs"].append(msg)
                return result

        update_result = mongo.coll_auth_info.update_one({"idno": auth_idno}, {"$set": {"role": auth_role_new}})
        if update_result.modified_count != 0:
            msg = {
                "type": "success",
                "text": "更新成功<br>[ update_count=%s ]" % update_result.modified_count
            }
        else:
            msg = {
                "type": "error",
                "text": "更新失败<br>[ update_count=%s ]" % update_result.modified_count
            }
        result["msgs"].append(msg)
        return result


auth_utils = AuthUtils()
