from flask import Blueprint, redirect, url_for
from rpi_portal.common.rpi_auth_util import RPIAuthUtil
from rpi_portal.service.management_service import ManagementService
from rpi_portal.service.member_service import MemberService

url_prefix = "/admin"
admin_controller = Blueprint(
    "admin_controller",
    __name__,
    url_prefix=url_prefix
)

member_service = MemberService()
management_service = ManagementService()


@admin_controller.route("/operator-list", methods=['GET'])
def operator_list():
    return member_service.operator_list()


@admin_controller.route("/operator-cu/<int:id>", methods=['GET', 'POST'])
@admin_controller.route("/operator-cu", methods=['GET', 'POST'])
def operator_cu(id: int = None):
    return member_service.operator_cu(id)


@admin_controller.route("/student-list", methods=['GET'])
def student_list():
    return member_service.student_list()


@admin_controller.route("/member-details/<int:id>", methods=['GET'])
def member_details(id: int):
    return member_service.member_details(id)


@admin_controller.route("/reset/<int:id>", methods=['POST', 'GET'])
def reset(id: int):
    return member_service.reset(id)


@admin_controller.route("/reset-operator/<int:id>", methods=['POST', 'GET'])
def reset_operator(id: int):
    return member_service.reset(id, success_url="admin_controller.operator_list")


@admin_controller.route("/import-mark-sheet", methods=['POST', 'GET'])
def import_mark_sheet():
    return management_service.import_mark_sheet()


@admin_controller.route("/import-certificate", methods=['POST', 'GET'])
def import_certificate():
    return management_service.import_certificate()


@admin_controller.before_request
def check_member_role():
    if not RPIAuthUtil.is_admin():
        return redirect(url_for("member_controller.dashboard"))
