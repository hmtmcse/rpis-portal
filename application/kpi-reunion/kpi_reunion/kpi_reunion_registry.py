from kpi_reunion.controller.admin_controller import admin_controller
from kpi_reunion.controller.kpi_reunion_controller import kpi_reunion_controller
from kpi_reunion.controller.manager_controller import manager_controller
from kpi_reunion.controller.member_controller import member_controller
from kpi_reunion.controller.site_controller import site_controller
from pf_flask_web.system12.pweb_interfaces import PWebAppRegistry


class KpiReunionRegistry(PWebAppRegistry):

    def run_on_cli_init(self, pweb_app):
        pass

    def run_on_start(self, pweb_app):
        pass

    def register_model(self, pweb_db):
        pass

    def register_controller(self, pweb_app):
        pweb_app.register_blueprint(kpi_reunion_controller)
        pweb_app.register_blueprint(site_controller)
        pweb_app.register_blueprint(member_controller)
        pweb_app.register_blueprint(admin_controller)
        pweb_app.register_blueprint(manager_controller)
