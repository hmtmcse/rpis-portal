from flask import Blueprint

url_prefix = "/register-ass"
register_ass_controller = Blueprint(
    "register_ass_controller",
    __name__,
    url_prefix=url_prefix
)
