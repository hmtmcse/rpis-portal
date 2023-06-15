from pf_flask_web.system12.pweb_interfaces import PWebAppRegistry
from rpi_portal.controller.site_controller import site_controller


class RPIPortalRegistry(PWebAppRegistry):

    def run_on_cli_init(self, pweb_app):
        pass

    def run_on_start(self, pweb_app):
        pass

    def register_model(self, pweb_db):
        pass

    def register_controller(self, pweb_app):
        pweb_app.register_blueprint(site_controller)
