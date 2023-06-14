from flask import Blueprint, redirect, url_for
from kpi_reunion.common.kpir_auth_util import KPIRAuthUtil
from kpi_reunion.service.admin_service import AdminService
from kpi_reunion.service.member_service import MemberService

url_prefix = "/admin"
admin_controller = Blueprint(
    "admin_controller",
    __name__,
    url_prefix=url_prefix
)

member_service = MemberService()
admin_service = AdminService()


@admin_controller.route("/member-list", methods=['GET'])
def member_list():
    return member_service.member_list()


@admin_controller.route("/member-details/<int:id>", methods=['GET'])
def member_details(id: int):
    return member_service.member_details(id)


@admin_controller.route("/event-list", methods=['GET'])
def event_list():
    return admin_service.event_list()


@admin_controller.before_request
def check_member_role():
    if not KPIRAuthUtil.is_admin():
        return redirect(url_for("member_controller.dashboard"))


@admin_controller.route("/event-details/<int:id>", methods=['GET'])
def event_details(id: int):
    return admin_service.event_details(id)


@admin_controller.route("/event-verify-payment/<int:id>", methods=['GET', 'POST'])
def event_verify_payment(id: int):
    return admin_service.event_verify_payment(id)


@admin_controller.route("/reset/<int:id>", methods=['POST', 'GET'])
def reset(id: int):
    return member_service.reset(id)
