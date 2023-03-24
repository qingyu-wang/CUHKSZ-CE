from flask import render_template, request

from .utils_index import get_nav


def get_error(message, detail):
    error = {
        "header": {
            "message": message
        },
        "detail": {
            "detail": detail,
            "url": request.url,
            "endpoint": request.endpoint,
            "method": request.method,
            "args": dict(request.args),
            "data": request.data.decode(),
            "json": dict(request.json) if request.headers.get("Content-Type", "") == "application/json" else {},
            "form": dict(request.form),
            "files": {key: val.filename for key, val in request.files.items()},
            "account": ["idno", "role", "username"],
            "headers": {key: request.headers[key] for key in request.headers.keys()},
        }
    }
    return error


def render_error_template(message="", detail=""):
    error_params = {"nav": get_nav(), "error": get_error(message=message, detail=detail)}
    return render_template("error.html", **error_params)
