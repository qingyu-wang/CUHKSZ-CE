import datetime
import socket

from flask import Flask
from flask_apscheduler import APScheduler
from flask_login import LoginManager

from .blueprints import *
from .utils.utils_mongo import mongo
from .utils.utils_auth import FlaskUser


HOSTNAME = socket.gethostname()


def create_app():

    app = Flask(__name__)
    print("[INFO] init application [name=%s]" % app.name)

    # Config - SECRET_KEY
    # import secrets; print(secrets.token_hex())
    app.config["SECRET_KEY"] = "600ff58f012fa2f57350fca51ed459792fbcc5c9112b4e06e9b94c066e6c394e"
    # Config - JSON_AS_ASCII
    app.config["JSON_AS_ASCII"] = False


    # APScheduler
    # http://127.0.0.1:5000/scheduler/jobs
    scheduler = APScheduler()
    scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()
    print("[INFO] scheduler running: %s" % scheduler.running)

    @scheduler.task(
        "interval",
        id="update_user_by_oracle",
        minutes=30,
        misfire_grace_time=600,
        # next_run_time=datetime.datetime.now() # run immediately
    )
    def job_update_user_by_oracle():
        print("[INFO] APSchedulerD [%s] start..." % "update_user_by_oracle")
        from .utils.utils_user_update_by_oracle import update_user_by_oracle
        update_user_by_oracle()
        mongo.coll_cache.update_one(
            {"name": "[%s] update_user_by_oracle" % HOSTNAME},
            {"$set": {"data": {"updatetime": datetime.datetime.now()}}},
            upsert=True
        )
        print("[INFO] APSchedulerD [%s] executed" % "update_user_by_oracle")
        return

    @scheduler.task(
        "interval",
        id="clean_dir",
        minutes=5,
        misfire_grace_time=100,
        next_run_time=datetime.datetime.now() # run immediately
    )
    def job_clean_dir():
        print("[INFO] APSchedulerD [%s] start..." % "clean_dir")
        from .utils.utils_file import file_utils
        file_utils.clean_dir(file_dir="temp_dir", max_seconds=300)
        mongo.coll_cache.update_one(
            {"name": "[%s] job_clean_dir" % HOSTNAME},
            {"$set": {"data": {
                "updatetime": datetime.datetime.now(),
                "updatetime": datetime.datetime.now(),
            }}},
            upsert=True
        )
        print("[INFO] APSchedulerD [%s] executed" % "clean_dir")
        return


    # Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "view_auth.login" # redirect page for login_required decorator
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(auth_idno):
        try:
            auth_user = mongo.coll_auth_info.find_one({"idno": auth_idno})
        except:
            print("[ERROR] %s load_user failed [ auth_idno=%s ]" % (
                datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), auth_idno
            ))
            auth_idno = "guest_001"
            auth_user = mongo.coll_auth_info.find_one({"idno": auth_idno})
        print("[INFO] %s load_user [ auth_idno=%s ]" % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), auth_idno
        ))
        flask_user = FlaskUser(auth_user=auth_user)
        return flask_user


    # Jinja2 Template Filter - strftime
    @app.template_filter()
    def strftime(text, format="%Y-%m-%d %H:%M:%S"):
        if isinstance(text, datetime.datetime):
            return text.strftime(format)
        else:
            return text


    # Blueprint
    app.register_blueprint(bp_view_index,       url_prefix="/")
    app.register_blueprint(bp_view_auth,        url_prefix="/auth")
    app.register_blueprint(bp_view_dashboard,       url_prefix="/dashboard")
    app.register_blueprint(bp_view_user,        url_prefix="/user")
    app.register_blueprint(bp_view_course,      url_prefix="/course")
    app.register_blueprint(bp_view_activity,    url_prefix="/activity")
    app.register_blueprint(bp_view_tool,        url_prefix="/tool")
    return app


app = create_app()


if __name__ == "__main__":
    app.run()
