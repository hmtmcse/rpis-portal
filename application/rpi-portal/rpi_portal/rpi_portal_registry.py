from pf_flask_web.system12.pweb_interfaces import PWebAppRegistry
from rpi_portal.controller.admin_controller import admin_controller
from rpi_portal.controller.department_controller import department_controller
from rpi_portal.controller.member_controller import member_controller
from rpi_portal.controller.principle_controller import principle_controller
from rpi_portal.controller.register_ass_controller import register_ass_controller
from rpi_portal.controller.register_controller import register_controller
from rpi_portal.controller.rpi_portal_controller import rpi_portal_controller
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
        pweb_app.register_blueprint(rpi_portal_controller)
        pweb_app.register_blueprint(admin_controller)
        pweb_app.register_blueprint(register_controller)
        pweb_app.register_blueprint(register_ass_controller)
        pweb_app.register_blueprint(member_controller)
        pweb_app.register_blueprint(department_controller)
        pweb_app.register_blueprint(principle_controller)
