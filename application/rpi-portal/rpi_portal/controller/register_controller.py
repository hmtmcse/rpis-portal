from flask import Blueprint

from rpi_portal.service.member_service import MemberService

url_prefix = "/register"
register_controller = Blueprint(
    "register_controller",
    __name__,
    url_prefix=url_prefix
)

member_service = MemberService()


@register_controller.route("/registration-approval", methods=['GET'])
def registration_approval():
    return member_service.pending_registration_list()


@register_controller.route("/student-details/<int:id>", methods=['GET'])
def student_details(id: int):
    return member_service.member_details(id)


@register_controller.route("/registration-approve/<int:id>", methods=['GET'])
def registration_approve(id: int):
    return member_service.registration_approve(id)
