# MongoDB

- [Server](#1-server)
- [Config](#2-config)
- [Service](#3-service)
- [Database](#4-database)
  - [Login](#login)
  - [Authorization](#authorization)
  - [Dump](#dump)
  - [Restore](#restore)
- [Usage](#5-usage)
  - [Database](#database)
  - [Collection](#collection)



## 1 Server

[server](./server.md#mongodb)



## 2 Config
- Linux
  - setting: [mongod-linux.conf](./mongod-linux.conf)
  - location: `/etc/mongod.conf`
- Windows:
  - setting: [mongod-windows.conf](./mongod-windows.conf)
  - location: `C:\Program Files\MongoDB\Server\X.X\bin\mongod.cfg`



## 3 Service

**linux**
```shell
# presetting
sudo ulimit -n 64000
sudo sysctl -w vm.max_map_count=262144


# execute once (config)
mongod --config /etc/mongod.conf
mongod --config ./mongodb/mongod-linux.conf
# execute once (option, auth, internal access)
mongod \
--auth \
--bind_ip 127.0.0.1 \
--port 27017 \
--dbpath /var/lib/mongodb \
--logpath /var/log/mongodb/mongod.log
# execute once (option, auth, external access)
mongod \
--auth \
--bind_ip 0.0.0.0 \
--port 27017 \
--dbpath /var/lib/mongodb \
--logpath /var/log/mongodb/mongod.log


# execute as service (tool: service)
service mongod start
service mongod status
service mongod stop

# execute as service (tool: systemctl)
systemctl start  mongod
systemctl status mongod
systemctl stop   mongod
systemctl enable mongod # start on reboot
```

**windows**

add `C:\Program Files\MongoDB\Server\X.X\bin\` to enviroment path

```shell
# execute once
mongod --config "C:\Program Files\MongoDB\Server\X.X\bin\mongod.cfg"
mongod --config ".\mongodb\mongod-windows.conf"


# execute as service (register first)
mongod --config "C:\Program Files\MongoDB\Server\5.0\bin\mongod.cfg" --install
# execute as service (tool: net)
net start mongodb-cuhkszce
net stop  mongodb-cuhkszce
```



## 4 Database

### Login

login **without** authorization

```shell
# port (default host = localhost = 127.0.0.1)
mongosh \
--port 27017

# host & port (internal access)
mongosh \
--host 127.0.0.1 \
--port 27017

# host & port (external access)
mongosh \
--host 0.0.0.0 \
--port 27017
```

login **with** authorization

```shell
mongosh \
--port 27017 \
--authenticationDatabase "admin" \
-u "myUserAdmin" \
-p "P@ss1234"
```

### Authorization

step 1: restart mongodb service **without** authorization

- ```shell
  service mongod stop
  ```
- ```shell
  vim /etc/mongod.conf
  ```
  - ```yaml
    security:
      authorization: disabled
    ```
- ```shell
  service mongod start
  ```

step 2: **create user**

- ```shell
  mongosh \
  --port 27017
  ```
  - ```shell
    use admin

    # create user
    db.createUser(
      {
        user: "myUserAdmin",
        pwd: "P@ss1234",
        roles: [
          {role: "userAdminAnyDatabase", db: "admin"}
        ]
      }
    )

    # show users
    db.getUsers()

    # show user
    db.getUser("myUserAdmin")
    ```

step 3: **grant or revoke roles**

- ```shell
  mongosh \
  --port 27017
  ```
  - ```shell
    use admin

    # grant roles
    db.grantRolesToUser(
      "myUserAdmin",
      [
        { role: 'root', db: 'admin' }
      ]
    )
    db.grantRolesToUser(
      "myUserAdmin",
      [
        { role: 'readWrite', db: 'cuhksz-ce' }
      ]
    )

    # revoke roles
    db.revokeRolesFromUser(
      "myUserAdmin",
      [
        { role: 'root', db: 'admin' }
      ]
    )
    ```

step 4: restart mongodb service **with** authorization

- ```shell
  service mongod stop
  ```
- ```shell
  vim /etc/mongod.conf
  ```
  - ```yaml
    security:
      authorization: enabled
    ```
- ```shell
  service mongod start
  ```

### Dump

```shell
mongodump \
--port 27017 \
--authenticationDatabase "admin" \
-u "myUserAdmin" \
-p "P@ss1234" \
--db "cuhksz-ce" \
--out "data/mongodb/yyyy-mm-dd"
```

### Restore

```shell
# whole database
mongorestore \
--port 27017 \
--authenticationDatabase "admin" \
-u "myUserAdmin" \
-p "P@ss1234" \
"data/mongodb/yyyy-mm-dd"

# certain database
mongorestore \
--port 27017 \
--authenticationDatabase "admin" \
-u "myUserAdmin" \
-p "P@ss1234" \
--db cuhksz-ce-temp \
"data/mongodb/yyyy-mm-dd"

# certain collection
mongorestore \
--port 27017 \
--authenticationDatabase "admin" \
-u "myUserAdmin" \
-p "P@ss1234" \
--db cuhksz-ce \
--collection coll_course_backup \
"data/mongodb/yyyy-mm-dd/cuhksz-ce/course.bson"

mongorestore --port 27017 --authenticationDatabase "admin" -u "myUserAdmin" -p "P@ss1234" --db cuhksz-ce \
--collection coll_activity_info_backup    "data/mongodb/2023-03-24/cuhksz/activity.bson"

mongorestore --port 27017 --authenticationDatabase "admin" -u "myUserAdmin" -p "P@ss1234" --db cuhksz-ce \
--collection coll_activity_record_backup  "data/mongodb/2023-03-24/cuhksz/activity_record.bson"

mongorestore --port 27017 --authenticationDatabase "admin" -u "myUserAdmin" -p "P@ss1234" --db cuhksz-ce \
--collection coll_course_info_backup      "data/mongodb/2023-03-24/cuhksz/course.bson"

mongorestore --port 27017 --authenticationDatabase "admin" -u "myUserAdmin" -p "P@ss1234" --db cuhksz-ce \
--collection coll_course_record_backup    "data/mongodb/2023-03-24/cuhksz/course_record.bson"
```

## 5 Usage

### Database

**login**
```shell
mongosh \
--port 27017 \
--authenticationDatabase "admin" \
-u "myUserAdmin" \
-p "P@ss1234"
```

**show**
```shell
# (mongosh)

show dbs
```

**choose**
```shell
# (mongosh)

use cuhksz-ce
```

**rename**
```shell
mongodump --archive --db=db_old | mongorestore --archive --nsFrom="db_old.*" --nsTo="db_new.*"

mongodump \
--port 27017 \
--authenticationDatabase "admin" \
-u "myUserAdmin" \
-p "P@ss1234" \
--archive \
--db=db_old | \
mongorestore \
--port 27017 \
--authenticationDatabase "admin" \
-u "myUserAdmin" \
-p "P@ss1234" \
--archive \
--nsFrom="db_old.*" \
--nsTo="db_new.*"
```

### Collection

**collection - show**
```shell
show collections
```

**collection - rename**
```shell
# (mongosh)

# Example
db.coll_name_old.renameCollection("coll_name_new")
# Temp
db.coll_course_backup.renameCollection("coll_course_info_backup")
```

**field - find**
```shell
# (mongosh)

# Example
db.coll_name.find({})
# Temp
db.coll_activity_record.find({"signin": true, "num_signin": 0})
```

**field - update**
```shell
# (mongosh)

# Example
db.coll_name.updateMany({}, {$set: {"field_name": "value_new"}})
# Temp
db.coll_user_info.updateMany({"modifyuser": {$exists : false}}, {$set: {"modifyuser": ""}})
```

**field - delete**
```shell
# (mongosh)

# Example
db.coll_name.updateMany({}, {$unset: {"field_name":""} } )
# Temp
db.coll_activity_record.updateMany({}, {$unset: {"course_code":""} } )
```

**field - rename**
```shell
# (mongosh)

# Example
db.coll_name.updateMany({}, {$rename: {"field_name_old":"field_name_new"} } )
# Temp
db.coll_auth_info.updateMany({}, {$rename: {"type": "role"}})
```

**field - exist**
```shell
# (mongosh)

# Example
db.coll_name.find({"field_name": {$exists : true}})
# Temp
db.coll_user_info.find({"modifyuser": {$exists : false}})
```

**document - delete**
```shell
# (mongosh)

# Example
db.coll_name.deleteMany({"field_name": "value"})
# Temp
db.coll_activity_record.deleteMany({"activity_code": "CEC1020-MOVIE-001-report"})
```
