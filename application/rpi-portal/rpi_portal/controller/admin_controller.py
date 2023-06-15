from flask import Blueprint

url_prefix = "/admin"
admin_controller = Blueprint(
    "admin_controller",
    __name__,
    url_prefix=url_prefix
)
