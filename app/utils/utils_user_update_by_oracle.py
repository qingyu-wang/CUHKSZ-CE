from tqdm import tqdm

from .utils_mongo import mongo
from .utils_oracle import oracle
from .utils_user import user_utils


campus_role_skip = [
    "校友", "家属", "物业", "安保", "钥匙", "中航物业",
    "访客", "外来人员", "附属单位", "商户",
    "测试部门"
]

campus_dept_map = {
    "AIRS":                 "未知部门 / AIRS",
    "AO":                   "招生办 / AO",
    "AO-IA":                "国际招生 / AO-IA",
    "APO":                  "学术规划办公室 / APO",
    "ASO":                  "行政事务处 / ASO",
    "AVP-Admin":            "协理副校长办公室 (行政) / AVP-Admin",
    "AVP-EDU&CU":           "协理副校长办公室 (教育与港中大事务) / AVP-EDU&CU",
    "AVP-GA":               "协理副校长办公室 (国际事务) / AVP-GA",
    "AVP-ID":               "协理副校长办公室 (拓展事务) / AVP-ID",
    "AVP-SA":               "协理副校长办公室 (学生事务) / AVP-SA",
    "BEO":                  "基础教育处 / BEO",
    "BFMO":                 "楼宇与设施管理处 / BFMO",
    "CDO":                  "校园发展处 / CDO",
    "CIDE":                 "创新创业中心 / CIDE",
    "CLEAR":                "学能提升研究中心 / CLEAR",
    "CPDO":                 "职业规划与发展处 / CPDO",
    "CPRO":                 "传讯及公共关系处 / CPRO",
    "DILIGENTIA":           "学勤书院 / DILIGENTIA",
    "EAMO":                 "设备与资产管理处 / EAMO",
    "EMSc-SCLM":            "供应链与物流管理高级管理人员理学硕士项目 / EMSc-SCLM",
    "金融工程/FE":          "金融工程 / FE",
    "FNii":                 "未来智联网络研究院 / FNii",
    "FO":                   "财务处 / FO",
    "Foundation":           "未知部门 / Foundation",
    "GCCS":                 "全球与当代中国高等研究院 / GCCS",
    "GS":                   "研究生院 / GS",
    "HARMONIA":             "祥波书院 / HARMONIA",
    "HKO":                  "香港办公室 / HKO",
    "HRO":                  "人力资源处 / HRO",
    "HSS":                  "人文社科学院 / HSS",
    "人文学院/HSS":         "人文社科学院 / HSS",
    "iDDA":                 "数据与运筹科学研究院 / iDDA",
    "数据运筹院/iDDA":      "数据与运筹科学研究院 / iDDA",
    "IIA":                  "国际事务研究院 / IIA",
    "IRIM":                 "机器人与智能制造研究院 / IRIM",
    "ISSSO":                "国际学者学生服务处 / ISSSO",
    "ITSO":                 "资讯科技服务处 / ITSO",
    "JPOSM":                "未知部门 / JPOSM",
    "KOBILKA":              "科比尔卡创新药物开发研究院 / KOBILKA",
    "LHS":                  "生命健康学院 / LHS",
    "MED-LHS":              "生命健康学院 / LHS",
    "生命健康学院/LHS":     "生命健康学院 / LHS",
    "Library":              "图书馆 / Library",
    "Ling College":         "道扬书院 / LING",
    "LING":                 "道扬书院 / LING",
    "MED":                  "医学院 / MED",
    "医学院/MED":           "医学院 / MED",
    "MUS":                  "音乐学院 / MUS",
    "音乐学院/MUS":         "音乐学院 / MUS",
    "MUSE":                 "思廷书院 / MUSE",
    "NCPO":                 "书院筹建办公室 / NCPO",
    "OAL":                  "学术交流处 / OAL",
    "OAL-ISSS":             "国际学者学生服务 / OAL-ISSS",
    "OIA":                  "拓展处/基金会 / OIA",
    "OSA":                  "学生事务处 / OSA",
    "PO":                   "校长办公室 / PO",
    "POIUSE":               "城市地下空间及能源研究院筹建办公室 / POIUSE",
    "POSMED":               "未知部门 / POSMED",
    "PSM":                  "未知部门 / PSM",
    "QOCUHKSZ":             "大学前海办公室 / QOCUHKSZ",
    "RAO":                  "科研处 / RAO",
    "RO":                   "未知部门 / RO",
    "Registry":             "教务处 / Registry",
    "SAO":                  "空间资源管理办公室 / SAO",
    "SDS":                  "数据科学学院 / SDS",
    "数据科学学院/SDS":     "数据科学学院 / SDS",
    "SHAW":                 "逸夫书院 / SHAW",
    "SHCC":                 "学生健康辅导中心 / SHCC",
    "SME":                  "经管学院 / SME",
    "经管学院/SME":         "经管学院 / SME",
    "SSE":                  "理工学院 / SSE",
    "理工学院/SSE":         "理工学院 / SSE",
    "理科实验班/SSE-TEST":  "理科实验班 / SSE-TEST",
    "SUSSEX":               "萨塞克斯大学 / SUSSEX",
    "TTC":                  "科技成果转化中心 / TTC",
    "UAC":                  "大学艺术中心 / UAC",
    "UDO":                  "大学发展处 / UDO",
    "VPO-Academic":         "副校长办公室 (学术) / VPO-Academic",
    "VPO-Admin":            "副校长办公室 (行政) / VPO-Admin",
    "VPO-ESA":              "副校长办公室 (外事) / VPO-ESA",
    "WARSHEL":              "瓦谢尔计算生物研究院 / WARSHEL",
}

campus_type_skip = [
    "校友", "非全职学生",
    "交流人员或访客", "外来人员",
    "附属单位", "非全职教职员", "相关部门认可人员",
    "全职教职员家属", "教职员非直系家属",
    "物业", "访客无门禁权限", "访客无游泳馆权限"
]

campus_addr_skip = [
    "/",
    "818000983/819000018",
    "818001025/27/28 920000187/8/9",
    "920000087",
    "923000001/002",
    "923000074",
    "923000078",
    "923000091/092/093",
    "923000094/095/096",
    "923000110/111",
    "GCCS",
    "Zhang Yimin",
    "广东省深圳市福田区紫竹六道6号110",
    "数据科学学院/SDS",
    "计算机与信息工程",
    "访问学生（沙田校区）",
]


def update_user_by_oracle():

    update_cnt = 0

    # 查询 Oracle 人员信息
    oracle_query = """
    SELECT
        trim(a.name)        AS name,
        trim(a.identity)    AS idno,
        to_number(a.sex)    AS sex,
        trim(a.bankacc)     AS bankacc,
        trim(a.phone)       AS phoneno,
        trim(a.sno)         AS campus_idno,
        p.code              AS campus_type_code,
        p.name              AS campus_type,
        d.d1_code           AS campus_role_code,
        d.d1_name           AS campus_role,
        d.d2_code           AS campus_dept_code,
        d.d2_name           AS campus_dept,
        i.addr              AS campus_addr,
        a.createdatetime    AS createtime,
        a.procdatetime      AS modifytime
    FROM
        iddbuser.account a
        INNER JOIN iddbuser.pid p ON p.code = a.pid
        INNER JOIN (
            SELECT
                d1.code AS d1_code,
                d1.name AS d1_name,
                d2.code AS d2_code,
                d2.name AS d2_name
            FROM
                iddbuser.department d2
                INNER JOIN iddbuser.department d1 ON d1.code = substr(d2.code, 1, 3)
        ) d ON d.d2_code = trim(substr(a.deptcode, 4))
        INNER JOIN iddbuser.idinformation i on i.no = a.identityid
    ORDER BY
        trim(a.identity),
        a.createdatetime
    """

    # 查询信息
    oracle.execute(oracle_query)
    oracle_headers = [i[0].lower() for i in oracle.cursor.description]

    # 处理信息
    with tqdm(desc="[INFO] user_update_oracle") as pbar:
        for oracle_row in oracle.cursor:
            oracle_user = dict(zip(oracle_headers, oracle_row))
            oracle_user.pop("campus_type_code")
            oracle_user.pop("campus_role_code")
            oracle_user.pop("campus_dept_code")
            oracle_user.pop("modifytime")

            for key in oracle_user:
                if not oracle_user[key]:
                    oracle_user[key] = "/"
            
            # Field: campus_role (d.d1_name)
            if oracle_user["campus_role"] in [
                "学生", "教工"
            ]:
                pass
            elif oracle_user["campus_role"] in campus_role_skip:
                continue
            else:
                print("[ERROR] unknown value [campus_role=%s]" % oracle_user["campus_role"])

            # Field: campus_type (p.name)
            if oracle_user["campus_type"] in [
                "教职员",
                "本科生", "研究生", "博士生", "交换生",
            ]:
                if oracle_user["campus_type"] == "教职员":
                    oracle_user["campus_type"] = "0 教职员"
                elif oracle_user["campus_type"] == "本科生":
                    oracle_user["campus_type"] = "1 本科生"
                elif oracle_user["campus_type"] == "研究生":
                    oracle_user["campus_type"] = "2 研究生"
                elif oracle_user["campus_type"] == "博士生":
                    oracle_user["campus_type"] = "3 博士生"
                elif oracle_user["campus_type"] == "交换生":
                    oracle_user["campus_type"] = "4 交换生"
            elif oracle_user["campus_type"] in campus_type_skip:
                continue
            else:
                print("[ERROR] unknown value [campus_type=%s]" % oracle_user["campus_type"])

            # Field: campus_dept (d.d2_name)
            if oracle_user["campus_dept"] in campus_dept_map:
                oracle_user["campus_dept"] = campus_dept_map[oracle_user["campus_dept"]]
            else:
                print("[ERROR] unknown value [campus_dept=%s]" % oracle_user["campus_dept"])

            # Field: campus_addr (i.addr)
            if oracle_user["campus_addr"] in campus_addr_skip:
                oracle_user["campus_addr"] = "/"
            elif "家属" in oracle_user["campus_addr"]:
                oracle_user["campus_addr"] = "/"
            elif "逸夫" in oracle_user["campus_addr"] or "SHAW"        in oracle_user["campus_addr"].upper():
                oracle_user["campus_addr"] = "逸夫书院 / SHAW"
            elif "学勤" in oracle_user["campus_addr"] or "DILIGENTIA"  in oracle_user["campus_addr"].upper():
                oracle_user["campus_addr"] = "学勤书院 / DILIGENTIA"
            elif "思廷" in oracle_user["campus_addr"] or "MUSE"        in oracle_user["campus_addr"].upper():
                oracle_user["campus_addr"] = "思廷书院 / MUSE"
            elif "祥波" in oracle_user["campus_addr"] or "HARMONIA"    in oracle_user["campus_addr"].upper():
                oracle_user["campus_addr"] = "祥波书院 / HARMONIA"
            elif "道扬" in oracle_user["campus_addr"] or "LING"        in oracle_user["campus_addr"].upper():
                oracle_user["campus_addr"] = "道扬书院 / LING"
            elif "厚含" in oracle_user["campus_addr"] or "MINERVA"     in oracle_user["campus_addr"].upper():
                oracle_user["campus_addr"] = "厚含书院 / MINERVA"
            else:
                print("[ERROR] unknown value [campus_addr=%s]" % oracle_user["campus_addr"])

            # Field: sex
            if len(oracle_user["idno"]) == 18:
                oracle_user["sex"] = "男" if int(oracle_user["idno"][-2]) % 2 == 1 else "女"
            else:
                oracle_user["sex"] = "男" if oracle_user["sex"] == 1 else "女"

            # Field: bankacc
            if oracle_user["bankacc"] == "BankAcc":
                oracle_user["bankacc"] = ""

            # Field: phoneno
            if oracle_user["phoneno"] and "家属卡" in oracle_user["phoneno"]:
                oracle_user["phoneno"] = ""

            # Field: campus_year
            if oracle_user["campus_role"] == "学生":
                oracle_user["campus_year"] = "20%s" % oracle_user["campus_idno"][1:3]
            else:
                oracle_user["campus_year"] = ""

            # 查询用户
            if not oracle_user["campus_idno"]:
                continue
            user_num = mongo.coll_user_info.count_documents(
                {"campus_idno": oracle_user["campus_idno"]}
            )

            # 新增用户
            if user_num == 0:
                mongo_user = user_utils.new_doc
                for key in mongo_user:
                    if key in oracle_user:
                        mongo_user[key] = oracle_user[key]
                mongo.coll_user_info.insert_one(mongo_user)
                print("\n[INFO] insert [campus_idno=%s]\n%s" % (
                    oracle_user["campus_idno"],
                    mongo_user
                ))

            # 更新用户
            elif user_num == 1:
                mongo_user = mongo.coll_user_info.find_one({"campus_idno": oracle_user["campus_idno"]})
                mongo_user_origin_info = {}
                mongo_user_update_info = {}
                for key in mongo_user:
                    if key in mongo_user["modifykeys"]: # 人工修改过的不更新
                        continue
                    if key not in oracle_user:
                        continue
                    if oracle_user[key] and mongo_user[key] != oracle_user[key]:
                        mongo_user_origin_info[key] = mongo_user[key]
                        mongo_user_update_info[key] = oracle_user[key]
                if mongo_user_update_info:
                    update_result = mongo.coll_user_info.update_one(
                        {"campus_idno": oracle_user["campus_idno"]},
                        {"$set": mongo_user_update_info}
                    )
                    if update_result.modified_count == 1:
                        print("\n[INFO] update [campus_idno=%s]\norigin: %s\nupdate: %s" % (
                            oracle_user["campus_idno"],
                            mongo_user_origin_info,
                            mongo_user_update_info
                        ))
                        update_cnt += 1
                    else:
                        print("[ERROR] update error (modified_count: %s)" % update_result.modified_count)

            else:
                print("[ERROR] multi results [campus_idno=%s, user_num=%s]" % (
                    oracle_user["campus_idno"], user_num
                ))

            pbar.update(1)

    print("[INFO] done [update_cnt=%s]" % update_cnt)
    return update_cnt


if __name__ == "__main__":

    """
python -m utils.utils_user_update_by_oracle
    """

    update_user_by_oracle()
