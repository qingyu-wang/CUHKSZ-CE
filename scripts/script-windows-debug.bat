@REM Service Windows Debug
@REM http://127.0.0.1:5000

set FLASK_APP=app
set FLASK_DEBUG=True
flask run -h 0.0.0.0
