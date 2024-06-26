from flask import Blueprint, redirect, url_for

from rpi_portal.common.rpi_auth_util import RPIAuthUtil
from rpi_portal.service.management_service import ManagementService
from rpi_portal.service.member_service import MemberService

url_prefix = "/register"
register_controller = Blueprint(
    "register_controller",
    __name__,
    url_prefix=url_prefix
)

member_service = MemberService()
management_service = ManagementService()


@register_controller.route("/registration-approval", methods=['GET'])
def registration_approval():
    return member_service.pending_registration_list()


@register_controller.route("/student-details/<int:id>", methods=['GET'])
def student_details(id: int):
    return member_service.member_details(id)


@register_controller.route("/registration-approve/<int:id>", methods=['GET'])
def registration_approve(id: int):
    return member_service.registration_approve(id)


@register_controller.route("/mark-sheet", methods=['GET'])
def mark_sheet():
    return management_service.mark_sheet()


@register_controller.route("/certificate", methods=['GET'])
def certificate():
    return management_service.certificate()


@register_controller.route("/import-certificate", methods=['GET', 'POST'])
def import_certificate():
    return management_service.import_certificate()


@register_controller.route("/import-mark-sheet", methods=['GET', 'POST'])
def import_mark_sheet():
    return management_service.import_mark_sheet()


@register_controller.route("/receive-request", methods=['GET'])
def receive_request():
    return management_service.receive_request()


@register_controller.route("/pass-to-department/<int:id>", methods=['GET'])
def pass_to_department(id: int):
    return management_service.pass_to_department(id)


@register_controller.route("/attestation-details/<int:id>", methods=['GET'])
def attestation_details(id: int):
    return management_service.attestation_details(id, redirect_url="register_controller.receive_request")


@register_controller.route("/process-request/<int:id>", methods=['GET', 'POST'])
def process_request(id: int):
    return management_service.process_request(id)


@register_controller.route("/resolve-request/<int:id>", methods=['GET', 'POST'])
def resolve_request(id: int):
    return management_service.resolve_request(id)


@register_controller.before_request
def check_member_role():
    if not RPIAuthUtil.is_register():
        return redirect(url_for("member_controller.dashboard"))
