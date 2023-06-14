from flask import Blueprint, url_for, redirect

from kpi_reunion.common.kpir_auth_util import KPIRAuthUtil
from kpi_reunion.service.event_service import EventService

url_prefix = "/volunteer"
volunteer_controller = Blueprint(
    "volunteer_controller",
    __name__,
    url_prefix=url_prefix
)

event_service = EventService()


@volunteer_controller.route("/", methods=['GET', 'POST'])
def scan():
    return event_service.scan()


@volunteer_controller.route("/scan-details", methods=['GET'])
def scan_details():
    return event_service.scan_details()


@volunteer_controller.route("/update-scan-item", methods=['GET'])
def update_scan_item():
    return event_service.update_scan_item()


@volunteer_controller.before_request
def check_member_role():
    if not KPIRAuthUtil.is_admin() and not KPIRAuthUtil.is_manager() and not KPIRAuthUtil.is_volunteer():
        return redirect(url_for("member_controller.dashboard"))
