from flask import Blueprint
from rpi_portal.service.member_service import MemberService

url_prefix = "/admin"
admin_controller = Blueprint(
    "admin_controller",
    __name__,
    url_prefix=url_prefix
)

member_service = MemberService()


@admin_controller.route("/member-list", methods=['GET'])
def member_list():
    return member_service.member_list()


@admin_controller.route("/member-details/<int:id>", methods=['GET'])
def member_details(id: int):
    return member_service.member_details(id)


@admin_controller.route("/reset/<int:id>", methods=['POST', 'GET'])
def reset(id: int):
    return member_service.reset(id)
