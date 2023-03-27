from flask import url_for
from flask_login import current_user

from .utils_auth import UserRole


def get_nav():

    nav_info = {
        "人员": {
            "url": None,
            "auth": [UserRole.staff, UserRole.admin],
            "sub": {
                "人员信息": {
                    "url": url_for("view_user.info"),
                    "auth": [UserRole.staff, UserRole.admin]
                },
                "---1---": {
                    "url": None,
                    "auth": [UserRole.admin]
                },
                "人员管理": {
                    "url": url_for("view_user.info_for_admin"),
                    "auth": [UserRole.admin]
                },
                "人员数据": {
                    "url": url_for("view_user.data"),
                    "auth": [UserRole.admin]
                },
            }
        },
        "课程": {
            "url": None,
            "auth": [UserRole.guest, UserRole.staff, UserRole.admin],
            "sub": {
                "课程信息": {
                    "url": url_for("view_course.info"),
                    "auth": [UserRole.guest, UserRole.staff, UserRole.admin]
                },
                "课程记录": {
                    "url": url_for("view_course.record"),
                    "auth": [UserRole.staff, UserRole.admin]
                },
                "---1---": {
                    "url": None,
                    "auth": [UserRole.admin],
                },
                "课程管理": {
                    "url": url_for("view_course.info_for_admin"),
                    "auth": [UserRole.admin],
                },
                "课程数据": {
                    "url": url_for("view_course.data"),
                    "auth": [UserRole.admin],
                }
            }
        },
        "活动": {
            "url": None,
            "auth": [UserRole.guest, UserRole.staff, UserRole.admin],
            "sub": {
                "活动信息": {
                    "url": url_for("view_activity.info"),
                    "auth": [UserRole.guest, UserRole.staff, UserRole.admin],
                },
                "活动记录": {
                    "url": url_for("view_activity.record"),
                    "auth": [UserRole.staff, UserRole.admin]
                },
                "---1---": {
                    "url": None,
                    "auth": [UserRole.admin],
                },
                "活动管理": {
                    "url": url_for("view_activity.info_for_admin"),
                    "auth": [UserRole.admin],
                },
                "活动数据": {
                    "url": url_for("view_activity.data"),
                    "auth": [UserRole.admin],
                },
            }
        },
        "工具": {
            "url": None,
            "auth": [UserRole.staff, UserRole.admin],
            "sub": {
                "问卷星": {
                    "url": url_for("view_tool.wenjuanxing"),
                    "auth": [UserRole.admin]
                },
                "Zoom": {
                    "url": url_for("view_tool.zoom"),
                    "auth": [UserRole.admin]
                },                
                "腾讯会议": {
                    "url": url_for("view_tool.tencent"),
                    "auth": [UserRole.admin]
                },
                "打卡机": {
                    "url": url_for("view_tool.dakaji"),
                    "auth": [UserRole.admin]
                },
                "---2---": {
                    "url": None,
                    "auth": [UserRole.admin],
                },
                "权限管理": {
                    "url": url_for("view_auth.role"),
                    "auth": [UserRole.admin]
                },
                "数据结构": {
                    "url": url_for("view_tool.data_structure"),
                    "auth": [UserRole.admin]
                },
            }
        }
    }
    current_nav_info = {}
    for nav1_name, nav1_info in nav_info.items():
        if nav1_info["auth"] is None or (not current_user.is_anonymous and current_user.role in nav1_info["auth"]):
            current_nav_info[nav1_name] = {
                "url": nav1_info["url"],
                "sub": {}
            }
            for nav2_name, nav2_info in nav1_info["sub"].items():
                if nav2_info["auth"] is None or (not current_user.is_anonymous and current_user.role in nav2_info["auth"]):
                    current_nav_info[nav1_name]["sub"][nav2_name] = {
                        "url": nav2_info["url"]
                    }
    return current_nav_info
