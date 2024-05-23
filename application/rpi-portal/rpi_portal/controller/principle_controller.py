from flask import Blueprint, redirect, url_for, flash
from rpi_portal.common.rpi_auth_util import RPIAuthUtil
from rpi_portal.service.management_service import ManagementService

url_prefix = "/principle"
principle_controller = Blueprint(
    "principle_controller",
    __name__,
    url_prefix=url_prefix
)

management_service = ManagementService()


@principle_controller.route("/receive-request", methods=['GET'])
def receive_request():
    return management_service.receive_request_by_principle()


@principle_controller.route("/attestation-details/<int:id>", methods=['GET'])
def attestation_details(id: int):
    return management_service.attestation_details(id, redirect_url="principle_controller.receive_request")


@principle_controller.route("/approved/<int:id>", methods=['GET'])
def approved(id: int):
    return management_service.approved(id)


@principle_controller.before_request
def check_member_role():
    if not RPIAuthUtil.is_principle():
        flash("Access denied", "error")
        return redirect(url_for("member_controller.dashboard"))
