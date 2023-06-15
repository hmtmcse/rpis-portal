from flask import Blueprint
from application.config.app_config import Config

url_prefix = "/"
rpi_portal_controller = Blueprint(
    "rpi-portal",
    __name__,
    url_prefix=url_prefix,
    template_folder=Config.TEMPLATE_PATH,
    static_folder=Config.ASSETS_PATH,
    static_url_path=Config.ASSETS_URL,
)
