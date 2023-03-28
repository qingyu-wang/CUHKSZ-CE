"""
Utils Board
"""

from .utils_mongo import mongo
from .utils_user import user_utils
from .utils_course_record import course_record_utils


class BoardUtils(object):

    # ---
    # function.get
    # ---

    def get_overview_infos(self):
        result = {
            "msgs": [],
            "overview_infos": None,
        }
        __overviews = mongo.coll_course_record.aggregate([
            # 查询人员信息
            {"$lookup": {
                "from": "coll_user_info", "as": "user_info",
                "localField": "campus_idno", "foreignField": "campus_idno"
            }},
            {"$unwind": "$user_info"},
            # 匹配
            {"$match": {
                "user_info.campus_role": "学生",
                "user_info.campus_type": "1 本科生",
                "user_info.campus_status": "1 修读",
                "user_info.campus_source": {"$ne": "6 国际"}
            }},
            # 聚合
            {"$group": {
                "_id": {
                    "course_code":  "$course_code",
                    "status":       "$status",
                    "campus_grade": "$user_info.campus_grade",
                    "campus_year":  "$user_info.campus_year",
                },
                "count": {"$count": {}},
            }}
        ])
        if not __overviews:
            return result

        overview_infos = {
            "campus_grade": {},
            "campus_year":  {},
        }
        for __overview in __overviews:
            __course_code  = __overview["_id"]["course_code"]
            __status       = __overview["_id"]["status"]
            __campus_grade = __overview["_id"]["campus_grade"]
            __campus_year  = __overview["_id"]["campus_year"]
            __count        = __overview["count"]
            # 聚合 年级
            if __course_code not in overview_infos["campus_grade"]:
                overview_infos["campus_grade"][__course_code] = {}
            if __campus_grade not in overview_infos["campus_grade"][__course_code]:
                overview_infos["campus_grade"][__course_code][__campus_grade] = {"总计": 0}
            if __status not in overview_infos["campus_grade"][__course_code][__campus_grade] :
                overview_infos["campus_grade"][__course_code][__campus_grade][__status] = 0
            overview_infos["campus_grade"][__course_code][__campus_grade][__status] += __count
            overview_infos["campus_grade"][__course_code][__campus_grade]["总计"] += __count
            # 聚合 入学年份 
            if __course_code not in overview_infos["campus_year"]:
                overview_infos["campus_year"][__course_code] = {}
            if __campus_year not in overview_infos["campus_year"][__course_code]:
                overview_infos["campus_year"][__course_code][__campus_year] = {"总计": 0}
            if __status not in overview_infos["campus_year"][__course_code][__campus_year] :
                overview_infos["campus_year"][__course_code][__campus_year][__status] = 0
            overview_infos["campus_year"][__course_code][__campus_year][__status] += __count
            overview_infos["campus_year"][__course_code][__campus_year]["总计"] += __count
        result["overview_infos"] = overview_infos
        result["msgs"].append({
            "type": "success",
            "text": "<br>".join([
                "查询逻辑", 
                "人员信息.%s == \"%s\"" % (user_utils.field_headers["campus_role"],   "学生"),
                "人员信息.%s == \"%s\"" % (user_utils.field_headers["campus_type"],   "1 本科生"),
                "人员信息.%s == \"%s\"" % (user_utils.field_headers["campus_status"], "1 修读"),
                "人员信息.%s <> \"%s\"" % (user_utils.field_headers["campus_source"], "6 国际")
            ])
        })
        return result

    def get_college_infos(self):
        result = {
            "msgs": [],
            "activity_rules": None,
            "college_infos": None,
        }
        course_code = "CEC1020"
        course_info = mongo.coll_course_info.find_one({"course_code": course_code})
        if not course_info:
            result["msgs"].append({
                "type": "error",
                "text": "查询失败<br>课程不存在 [ %s = %s]" % (
                    course_record_utils.field_headers["course_code"],  course_code
                )
            })
            return result
        activity_rules = course_info["activity_rules"]
        activity_types = ["已完成书院活动"] + sorted(list({activity_type 
            for activity_rule in activity_rules 
            for activity_type in activity_rule if activity_type
        }))
        result["activity_types"] = activity_types
        # 聚合参数
        group_config = {
            "_id": {
                "campus_addr":  "$user_info.campus_addr",
                "status":       "$status",
                "campus_grade": "$user_info.campus_grade",
                "campus_year":  "$user_info.campus_year",
            },
            "count": {"$count": {}}
        }
        for activity_rule in activity_rules:
            for acitivty_type, count in activity_rule.items():
                group_config[acitivty_type] = {"$sum": {"$cond": [
                    {"$gte": ["$activity_done.%s" % acitivty_type, count]}, 1, 0
                ]}}
        group_config["已完成书院活动"] = {"$sum": {"$cond": [
            {"$or" : [
                {"$gte": ["$activity_done.%s" % acitivty_type, count]}
                for activity_rule in activity_rules
                for acitivty_type, count in activity_rule.items()
                if acitivty_type in ["大型活动签到", "常规活动学时"]
            ]}, 1, 0
        ]}}
        # 查询  
        __colleges = mongo.coll_course_record.aggregate([
            # 匹配
            {"$match": {
                "course_code": "CEC1020",
            }},
            # 查询人员信息
            {"$lookup": {
                "from": "coll_user_info", "as": "user_info",
                "localField": "campus_idno", "foreignField": "campus_idno"
            }},
            {"$unwind": "$user_info"},
            # 匹配
            {"$match": {
                "user_info.campus_role": "学生",
                "user_info.campus_type": "1 本科生",
                "user_info.campus_status": "1 修读",
                "user_info.campus_source": {"$ne": "6 国际"}
            }},
            # 聚合
            {"$group": group_config}
        ])
        if not __colleges:
            return result

        college_infos = {
            "campus_grade": {},
            "campus_year":  {},
        }
        for __college in __colleges:
            __campus_addr    = __college["_id"]["campus_addr"]
            __status         = __college["_id"]["status"]
            __campus_grade   = __college["_id"]["campus_grade"]
            __campus_year    = __college["_id"]["campus_year"]
            __count          = __college["count"]
            __activity_types = {activity_type: __college[activity_type] for activity_type in activity_types}
            # 聚合 年级
            if __campus_addr not in college_infos["campus_grade"]:
                college_infos["campus_grade"][__campus_addr] = {}
            if __campus_grade not in college_infos["campus_grade"][__campus_addr]:
                college_infos["campus_grade"][__campus_addr][__campus_grade] = {"总计": 0}
            if __status not in college_infos["campus_grade"][__campus_addr][__campus_grade] :
                college_infos["campus_grade"][__campus_addr][__campus_grade][__status] = 0
            for __activity_type, __activity_type_count in __activity_types.items():
                if __activity_type not in college_infos["campus_grade"][__campus_addr][__campus_grade] :
                    college_infos["campus_grade"][__campus_addr][__campus_grade][__activity_type] = 0
                college_infos["campus_grade"][__campus_addr][__campus_grade][__activity_type] += __activity_type_count
            college_infos["campus_grade"][__campus_addr][__campus_grade][__status] += __count
            college_infos["campus_grade"][__campus_addr][__campus_grade]["总计"] += __count
            # 聚合 入学年份 
            if __campus_addr not in college_infos["campus_year"]:
                college_infos["campus_year"][__campus_addr] = {}
            if __campus_year not in college_infos["campus_year"][__campus_addr]:
                college_infos["campus_year"][__campus_addr][__campus_year] = {"总计": 0}
            if __status not in college_infos["campus_year"][__campus_addr][__campus_year] :
                college_infos["campus_year"][__campus_addr][__campus_year][__status] = 0
            for __activity_type, __activity_type_count in __activity_types.items():
                if __activity_type not in college_infos["campus_year"][__campus_addr][__campus_year] :
                    college_infos["campus_year"][__campus_addr][__campus_year][__activity_type] = 0
                college_infos["campus_year"][__campus_addr][__campus_year][__activity_type] += __activity_type_count
            college_infos["campus_year"][__campus_addr][__campus_year][__status] += __count
            college_infos["campus_year"][__campus_addr][__campus_year]["总计"] += __count
        result["college_infos"] = college_infos
        result["msgs"].append({
            "type": "success",
            "text": "<br>".join([
                "查询逻辑", 
                "人员信息.%s == \"%s\"" % (user_utils.field_headers["campus_role"],   "学生"),
                "人员信息.%s == \"%s\"" % (user_utils.field_headers["campus_type"],   "1 本科生"),
                "人员信息.%s == \"%s\"" % (user_utils.field_headers["campus_status"], "1 修读"),
                "人员信息.%s <> \"%s\"" % (user_utils.field_headers["campus_source"], "6 国际")
            ] + sorted(["课程记录.活动进度.%s >= %s" % (acitivty_type, count) for activity_rule in activity_rules for acitivty_type, count in activity_rule.items()])
            )
        })
        print(college_infos)
        return result


board_utils = BoardUtils()
