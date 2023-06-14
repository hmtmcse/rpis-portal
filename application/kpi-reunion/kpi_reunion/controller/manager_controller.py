from flask import Blueprint

url_prefix = "/manager"
manager_controller = Blueprint(
    "manager_controller",
    __name__,
    url_prefix=url_prefix
)
