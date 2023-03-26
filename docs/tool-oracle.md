# connect 连接

```python
from pprint import pprint

import cx_Oracle


cx_Oracle.init_oracle_client(lib_dir= "D:/Software/instantclient_21_6")


# 连接
oracle_client = cx_Oracle.connect(
    user="qinqiong1",
    password="qinqiong1",
    dsn="10.20.198.2:1521/iddbsvr",
    encoding="UTF-8"
)
oracle_cur = oracle_client.cursor()

# 断开
oracle_client.close()
```

# show database 数据库

```python
oracle_cur.execute("SELECT * FROM v$database")
headers = [i[0] for i in oracle_cur.description]
for idx, header in enumerate(headers):
    print(idx, header)

for row in cur:
    print(row[1]) # NAME
```

# show tables 表

- `DBA_TABLES` >= `ALL_TABLES` >= `USER_TABLES`
- `DBA_TABLES`  describes all relational tables in the database.
- `ALL_TABLES`  describes the relational tables accessible to the current user.
- `USER_TABLES` describes the relational tables owned by the current user.

```python
oracle_cur.execute("SELECT * FROM all_tables WHERE rownum=1")
headers = [i[0] for i in oracle_cur.description]
for idx, header in enumerate(headers):
    print(idx, header)

# Show Owner
oracle_cur.execute("SELECT DISTINCT owner FROM all_tables ORDER BY owner")
for row in oracle_cur:
    print(row) # OWNER

# Show Table by Owner
oracle_cur.execute("SELECT * FROM all_tables WHERE owner='IDDBUSER' ORDER BY owner, table_name")
for row in oracle_cur:
    print(row[0], row[1]) # OWNER, TABLE_NAME

oracle_cur.execute("SELECT * FROM all_tables WHERE owner='QINQIONG' ORDER BY owner, table_name")
for row in oracle_cur:
    print(row[0], row[1]) # OWNER, TABLE_NAME

# IDDBUSER ACCOUNT 身份
# IDDBUSER DEPARTMENT 部门
# IDDBUSER PID 校园身份

# Show Table
oracle_cur.execute("SELECT * FROM iddbuser.account")
oracle_cur.execute("SELECT * FROM qinqiong1.conference ORDER BY conferencedate DESC")
headers = [i[0] for i in oracle_cur.description]
for idx, header in enumerate(headers):
    print(idx, header)

infos = {i: [headers[i]] for i in range(len(headers))}
cnt = 0
for row in oracle_cur:
    for i in range(len(headers)):
        infos[i].append(row[i])
    cnt += 1
    if cnt == 10:
        break

pprint(infos)
# QINQIONG1.CONFERENCE BOARDROOMID      会议室   7 核酸检测 44 校门准入
# QINQIONG1.CONFERENCE ATTENDENCETYPE   签到方式 0 指定人员 1 指定部门 2不指定
```

# show views 虚表

- `DBA_VIEWS` >= `ALL_VIEWS` >= `USER_VIEWS`
- `DBA_VIEWS`  describes all views in the database.
- `ALL_VIEWS`  describes the views accessible to the current user.
- `USER_VIEWS` describes the views owned by the current user.

```python
oracle_cur.execute("SELECT * FROM all_views WHERE rownum=1")
headers = [i[0] for i in oracle_cur.description]
for idx, header in enumerate(headers):
    print(idx, header)

oracle_cur.execute("SELECT * FROM all_views ORDER BY owner, view_name")
for row in cur:
    print("[%s] [%s] %s" % (row[0], row[1], row[3])) # OWNER, TABLE_NAME, TEXT

oracle_cur.execute("SELECT * FROM all_views WHERE owner='QINQIONG1' ORDER BY owner, view_name")
for row in cur:
    print("[%s] [%s] %s" % (row[0], row[1], row[3])) # OWNER, TABLE_NAME, TEXT
```

# 表: 人员信息 IDDBUSER.ACCOUNT

```python
oracle_cur.execute("SELECT * FROM iddbuser.account WHERE rownum<=10")
headers = [i[0] for i in oracle_cur.description]
for idx, header in enumerate(headers):
    print(idx, header)

infos = {i: [headers[i]] for i in range(len(headers))}
for row in cur:
    for i in range(len(headers)):
        infos[i].append(row[i])
pprint(infos)

# 0  ACCOUNT    人员ID (CONFERENCEWATERLIST.ACCOUNTID)
# 5  NAME       姓名
# 6  SEX        性别 1男 2女
# 7  PID        校园身份编码 (IDDBUSER.PID.CODE)
# 8  DEPTCODE   部门编码 (IDDBUSER.DEPARTMENT.CODE)
# 22 BANKACC    银行账户
# 23 IDENTITY   身份证号
# 25 SNO        学号

# 显示所有部门
oracle_cur.execute("SELECT DISTINCT a.deptcode FROM iddbuser.account a")
for row in cur:
    print(row)

# 根据人员ID查询
oracle_cur.execute("SELECT DISTINCT * FROM iddbuser.account a WHERE a.account = 205")
for row in cur:
    print(row)

# 根据人员身份证
oracle_cur.execute("SELECT a.name, a.sno, a.createdatetime FROM iddbuser.account a WHERE a.sno='219021047'")
for row in cur:
    print(row)
```

# 表: 部门信息 IDDBUSER.DEPARTMENT

```python
oracle_cur.execute("SELECT * FROM iddbuser.department")
# oracle_cur.execute("SELECT * FROM iddbuser.department WHERE rownum<=10")
headers = [i[0] for i in oracle_cur.description]
for idx, header in enumerate(headers):
    print(idx, header)

infos = {i: [headers[i]] for i in range(len(headers))}
for row in cur:
    for i in range(len(headers)):
        infos[i].append(row[i])
pprint(infos)

# 0 CODE 部门编码
# 1 NAME 部门名
# 7 DEPTDESC 描述

detail = dict()
for i in range(1, len(infos[0])):
    code = infos[0][i]
    name = infos[1][i]
    desc = infos[7][i]
    if len(code) == 3:
        detail[code] = {
            "code": code,
            "name": name,
            "desc": desc,
            "dept": list()
        }

for i in range(1, len(infos[0])):
    code = infos[0][i]
    name = infos[1][i]
    desc = infos[7][i]
    if len(code) > 3:
        detail[code[:3]]["dept"].append({
            "code": code,
            "name": name,
            "desc": desc
        })

for code in detail:
    detail[code]["dept"] = sorted(detail[code]["dept"], key=lambda x: x["code"])
pprint(detail)
```

## 常用表

```python
oracle_cur.execute("""
SELECT
    d1.code AS "一级部门编码",
    d1.name AS "一级部门名称",
    d2.code AS "二级部门编码",
    d2.name AS "二级部门名称"
FROM
    iddbuser.department d2
    INNER JOIN iddbuser.department d1 ON d1.code = substr(d2.code, 1, 3)
ORDER BY
    d1.code,
    d2.code
""")

headers = [i[0] for i in oracle_cur.description]
print(headers)
for row in cur:
    print(row)
```

# 表: 校园身份信息 IDDBUSER.PID

```python
# oracle_cur.execute("SELECT * FROM iddbuser.pid")
oracle_cur.execute("SELECT * FROM iddbuser.pid WHERE rownum<=10")
headers = [i[0] for i in oracle_cur.description]
for idx, header in enumerate(headers):
    print(idx, header)

infos = {i: [headers[i]] for i in range(len(headers))}
for row in cur:
    for i in range(len(headers)):
        infos[i].append(row[i])
pprint(infos)

# 0 CODE 校园身份编码
# 3 NAME 校园身份名称

details = dict()
for i in range(1, len(infos[0])):
    code = infos[0][i]
    name = infos[1][i]
    desc = infos[7][i]
    if len(code) == 3:
        details[code] = {
            "code": code,
            "name": name,
            "desc": desc,
            "dept": list()
        }

for i in range(1, len(infos[0])):
    code = infos[0][i]
    name = infos[1][i]
    desc = infos[7][i]
    if len(code) > 3:
        details[code[:3]]["dept"].append({
            "code": code,
            "name": name,
            "desc": desc
        })
```

# 表: 会议信息 CONFERENCE

```python
# oracle_cur.execute("SELECT * FROM conference")
oracle_cur.execute("SELECT * FROM conference WHERE rownum<=10")
headers = [i[0] for i in oracle_cur.description]
for idx, header in enumerate(headers):
    print(idx, header)

infos = {i: [headers[i]] for i in range(len(headers))}
for row in cur:
    for i in range(len(headers)):
        infos[i].append(row[i])
pprint(infos)

# 0  ID                 会议ID
# 2  CONFERENCENAME     会议名称
# 3  CONFERENCEDATE     会议日期
# 8  STARTTIME          开始时间
# 9  ENDTIME            结束时间
# 10 ATTENDENCETYPE     签到方式 0指定人员 1指定部门 2不指定人员部门
# 14 CONFERENCETYPEID   会议类型ID
# 15 ACCOUNTID          创建者ID (CONFERENCEWATERLIST.ACCOUNTID)
# 17 BEFORETIME         允许早到时间
# 18 LATETIME           允许迟到时间
# 20 LEAVETIME          允许早退时间
# 21 AFTERTIME          允许迟退时间

oracle_cur.execute("SELECT * FROM conference c WHERE c.id = 1069")
oracle_cur.execute("SELECT * FROM conference c WHERE c.conferencename LIKE '%形势与政策%二%'")
for row in cur:
    print(row)
```

# 表: 签到信息 CONFERENCEWATERLIST

```python
# oracle_cur.execute("SELECT * FROM conferencewaterlist")
oracle_cur.execute("SELECT * FROM conferencewaterlist WHERE rownum<=10")
oracle_cur.execute("SELECT * FROM conferencewaterlist c WHERE c.conferenceid=988")
headers = [i[0] for i in oracle_cur.description]
for idx, header in enumerate(headers):
    print(idx, header)

infos = {i: [headers[i]] for i in range(len(headers))}
for row in cur:
    for i in range(len(headers)):
        infos[i].append(row[i])
pprint(infos)

# 1 ACCOUNTID       打卡人ID (IDDBUSER.ACCOUNT.ACCOUNT)
# 2 WATERTIME       打卡时间
# 3 CONFERENCEID    会议ID (CONFERENCE.ID)
```

# 人员信息查询

```python
query = """
SELECT
    *
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
WHERE
    trim(a.identity) = '654201199808070822'
    
"""
headers = [i[0] for i in oracle_cur.description]
oracle_cur.execute(query)
for row in oracle.execute(query):
    pprint(list(zip(headers, row)))




 ('SUBSEQ', 2),
 ('PRESUBSEQ', 2),
 ('USECARDNUM', 46),
 ('MANAGEFEERATE', 0),
 ('QUERYPIN', 'A15AEBB9A221E62C'),
 ('OPERCODE', '001'),
 ('FLAG', '000001000100001'),
 ('CODE', '01'),
 ('CLASS', '2'),
 ('NAME', '教职员'),
 ('D1_CODE', '102'),
 ('D1_NAME', '教工'),
 ('D2_CODE', '102110'),
 ('D2_NAME', 'HSS')

 ('SUBSEQ', 1),
 ('PRESUBSEQ', 1),
 ('USECARDNUM', 3),
 ('MANAGEFEERATE', 0),
 ('QUERYPIN', '7B1A11412D34FA88'),
 ('OPERCODE', '010'),
 ('FLAG', '000001000100002'),
 ('CODE', '01'),
 ('CLASS', '2'),
 ('NAME', '教职员'),
 ('D1_CODE', '102'),
 ('D1_NAME', '教工'),
 ('D2_CODE', '102110'),
 ('D2_NAME', 'HSS')

 ('SUBSEQ', 0),
 ('PRESUBSEQ', 0),
 ('USECARDNUM', 1),
 ('MANAGEFEERATE', 0),
 ('QUERYPIN', 'E8115B39392EB4EE'),
 ('OPERCODE', '003'),
 ('FLAG', '000001000100000'),
 ('CODE', '06'),
 ('CLASS', '3'),
 ('NAME', '全职教职员家属'),
 ('D1_CODE', '107'),
 ('D1_NAME', '家属'),
 ('D2_CODE', '107116'),
 ('D2_NAME', 'HSS')



oracle_cur.execute("SELECT * FROM iddbuser.ACCOUNT")
headers = [i[0] for i in oracle_cur.description]
cnt = 0
for row in oracle_cur:
    pprint(list(zip(headers, row)))
    cnt += 1
    if cnt == 10:
        break

IDDBUSER ACCCONFIG
IDDBUSER ACCDIST
IDDBUSER ACCIDX
IDDBUSER ACCINFO
IDDBUSER ACCOUNT
IDDBUSER ACCTYPE
IDDBUSER AREA
IDDBUSER BANKCONFIG
IDDBUSER BRANCH
IDDBUSER CARDTYPE
IDDBUSER CHINAMOBILE
IDDBUSER CLOSE
IDDBUSER CMAPPIDX
IDDBUSER COMPARE_FILE
IDDBUSER CONFIGINFO
IDDBUSER CONSUMEREPORT
IDDBUSER CSZD
IDDBUSER CZYQX
IDDBUSER DATABKUPLOG
IDDBUSER DAYREPORT
IDDBUSER DEPARTMENT
IDDBUSER DEPTOPRNDEP
IDDBUSER DEPTREPORT
IDDBUSER E_CZLOG
IDDBUSER FEE
IDDBUSER FEEREPORT
IDDBUSER IDACCOUNT
IDDBUSER IDINFOBATCHOPERRESULT
IDDBUSER IDINFOEX
IDDBUSER IDINFORMATION
IDDBUSER IDINFORMATION_WEB
IDDBUSER IDOPERATOR
IDDBUSER IDTYPE
IDDBUSER ID_MUTEX
IDDBUSER ID_PIC_000
IDDBUSER ID_PIC_001
IDDBUSER ID_PIC_002
IDDBUSER ID_PIC_003
IDDBUSER ID_PIC_004
IDDBUSER ID_PIC_005
IDDBUSER JSZC
IDDBUSER LOG
IDDBUSER LSHZB
IDDBUSER L_FORUM
IDDBUSER L_ID
IDDBUSER L_ITEMS
IDDBUSER L_MESSAGE
IDDBUSER L_QUESTIONS
IDDBUSER L_TOPIC
IDDBUSER MERCACC
IDDBUSER MESSAGE
IDDBUSER MESSTEST
IDDBUSER MHISTRJN
IDDBUSER MHISTRJN_CP
IDDBUSER MQSBB
IDDBUSER NATION
IDDBUSER N_FIXCARD
IDDBUSER N_INFO
IDDBUSER N_MANAGER
IDDBUSER OPENINFO
IDDBUSER OPERATELOG
IDDBUSER OPERATOR
IDDBUSER OPERRIGHT
IDDBUSER OPERRIGHTEX
IDDBUSER OUTEREX
IDDBUSER OUTEREX_WEB
IDDBUSER OUTERPIC_WEB
IDDBUSER PEOPLE
IDDBUSER PID
IDDBUSER PIDSECTIONS
IDDBUSER PIDTOCTFC
IDDBUSER PLAN_TABLE
IDDBUSER QSBB
IDDBUSER SCHOOLCODE
IDDBUSER SFMX
IDDBUSER SFTJ
IDDBUSER SNOOPERCODES
IDDBUSER SSMX
IDDBUSER SS_YUAN
IDDBUSER STUDENTEX
IDDBUSER STUDENTEX_WEB
IDDBUSER STUDENTPIC_WEB
IDDBUSER SUBJECT
IDDBUSER SUBJN
IDDBUSER SUBREPORT
IDDBUSER SYSREGISTER
IDDBUSER SYSREPORT
IDDBUSER TABREPORT_DEPT_PID
IDDBUSER TABREPORT_GRADE
IDDBUSER TABREPORT_MERCDEPT
IDDBUSER TABREPORT_MERC_CARDTYPE
IDDBUSER TABREPORT_MERC_PID
IDDBUSER TABREPORT_MERC_SYSCODE
IDDBUSER TABREPORT_MONTH
IDDBUSER TABREPORT_PID_SEX
IDDBUSER TEACHEREX
IDDBUSER TEACHEREX_WEB
IDDBUSER TEACHERPIC_WEB
IDDBUSER TRCD
IDDBUSER TRCDIDX
IDDBUSER TRJN
IDDBUSER TTRJ
IDDBUSER TZREPORT
IDDBUSER T_DEPTCOMP
IDDBUSER T_GZ
IDDBUSER T_SCHOOLBEDFEE
IDDBUSER T_YL
IDDBUSER WEBTRJN
IDDBUSER WEBTRJN01
IDDBUSER WEBTRJN02
IDDBUSER WEBTRJN03
IDDBUSER WEBTRJN04
IDDBUSER WEBTRJN05
IDDBUSER WEBTRJN06
IDDBUSER WEBTRJN07
IDDBUSER WEBTRJN08
IDDBUSER WEBTRJN09
IDDBUSER WEBTRJN10
IDDBUSER WEBTRJN11
IDDBUSER WEBTRJN12
IDDBUSER WEBTRJNREPORT
IDDBUSER WEBTRJNTOTAL
IDDBUSER WEB_CM
IDDBUSER WEB_COMPARE_RESULT
IDDBUSER WEB_FBXXB
IDDBUSER WEB_FTPB
IDDBUSER WEB_GW
IDDBUSER WEB_GWJSB
IDDBUSER WEB_JKRYB
IDDBUSER WEB_PC
IDDBUSER WEB_ROLE
IDDBUSER WEB_ROLEMENU
IDDBUSER WEB_ROLESHB
IDDBUSER WEB_ROLEZYZB
IDDBUSER WEB_USERGWB
IDDBUSER WEB_USERINFO
IDDBUSER WEB_USERJSB
IDDBUSER WEB_XTGNB
IDDBUSER WEB_XTGNCD
IDDBUSER WEB_XXFJ
IDDBUSER WEB_XXLM
IDDBUSER WEB_ZYZB
IDDBUSER WHCD
IDDBUSER W_OP_MERCACC
IDDBUSER W_OP_ORDERINFO
IDDBUSER W_THIRD_MESSAGE
IDDBUSER XFZKL
IDDBUSER XZZW
IDDBUSER YSREPORT
IDDBUSER ZBHD
IDDBUSER ZH
IDDBUSER ZZMM

```

# 打卡记录查询

```python
query = """
SELECT
    t.account           AS "ID (打卡系统)",
    trim(t.name)        AS "姓名",
    t.sex               AS "性别",
    trim(t.identity)    AS "身份证号",
    trim(t.sno)         AS "学号/工号",
    t.p_code            AS "校园身份ID",
    t.p_name            AS "校园身份名称",
    t.d1_code           AS "一级部门ID",
    t.d1_name           AS "一级部门名称",
    t.d2_code           AS "二级部门ID",
    t.d2_name           AS "二级部门名称",
    c.conferencename    AS "会议名称",
    c.conferencedate    AS "会议日期",
    c.starttime         AS "开始时间",
    c.endtime           AS "结束时间",
    cw.watertime        AS "打卡时间"
FROM
    conferencewaterlist cw
    INNER JOIN conference c ON c.id = cw.conferenceid
    INNER JOIN (
        SELECT
            a.account,
            a.name,
            a.sex,
            a.identity,
            a.sno,
            p.code AS p_code,
            p.name AS p_name,
            d.d1_code,
            d.d1_name,
            d.d2_code,
            d.d2_name
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
    ) t ON t.account = cw.accountid
WHERE
    c.conferencename LIKE '%形势与政策%二%'
ORDER BY
    cw.watertime,
    t.sno
"""
for row in oracle_cur.execute(query):
    pprint(row)
    break
```

