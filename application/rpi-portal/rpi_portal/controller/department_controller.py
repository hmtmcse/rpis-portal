from flask import Blueprint, redirect, url_for, flash

from rpi_portal.common.rpi_auth_util import RPIAuthUtil
from rpi_portal.service.management_service import ManagementService

url_prefix = "/department"
department_controller = Blueprint(
    "department_controller",
    __name__,
    url_prefix=url_prefix
)

management_service = ManagementService()


@department_controller.route("/pass-to-department/<int:id>", methods=['GET'])
def pass_to_principle(id: int):
    return management_service.pass_to_principle(id)


@department_controller.route("/attestation-details/<int:id>", methods=['GET'])
def attestation_details(id: int):
    return management_service.attestation_details(id, redirect_url="register_controller.receive_request")


@department_controller.route("/receive-request", methods=['GET'])
def receive_request():
    return management_service.receive_request_by_department()


@department_controller.before_request
def check_member_role():
    if not RPIAuthUtil.is_department():
        flash("Access denied", "error")
        return redirect(url_for("member_controller.dashboard"))
