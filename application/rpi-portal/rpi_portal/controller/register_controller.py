from flask import Blueprint

url_prefix = "/register"
register_controller = Blueprint(
    "register_controller",
    __name__,
    url_prefix=url_prefix
)
