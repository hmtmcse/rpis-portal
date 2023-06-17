from flask import Blueprint
from rpi_portal.common.template_processor import render
from rpi_portal.service.management_service import ManagementService
from rpi_portal.service.member_service import MemberService

url_prefix = "/member"
member_controller = Blueprint(
    "member_controller",
    __name__,
    url_prefix=url_prefix
)

member_service = MemberService()
management_service = ManagementService()


@member_controller.route("/dashboard", methods=['POST', 'GET'])
def dashboard():
    return render("member/dashboard", {})


@member_controller.route("/support", methods=['GET'])
def support():
    return member_service.support()


@member_controller.route("/mark-sheet", methods=['GET'])
def mark_sheet():
    return management_service.my_mark_sheet()


@member_controller.route("/certificate", methods=['GET'])
def certificate():
    return management_service.my_certificate()


@member_controller.route("/protoyon-potro", methods=['GET'])
def protoyon_potro():
    return member_service.protoyon_potro()


@member_controller.route("/profile", methods=['GET'])
def profile():
    return member_service.profile()


@member_controller.route("/update-profile", methods=['POST', 'GET'])
def update_profile():
    return member_service.update_profile()


@member_controller.route("/change-password", methods=['POST', 'GET'])
def change_password():
    return member_service.change_password()


@member_controller.route("/upload-profile-photo", methods=['POST'])
def upload_profile_photo():
    return member_service.upload_profile_photo()


@member_controller.route("/send-mark-sheet-request/<int:id>", methods=['GET'])
def send_mark_sheet_request(id: int):
    return management_service.send_receive_request(id)


@member_controller.route("/receive-request-details/<int:id>", methods=['GET'])
def receive_request_details(id: int):
    return management_service.receive_request_details(id)


@member_controller.route("/attestation", methods=['GET'])
def attestation():
    return management_service.my_attestation()


@member_controller.route("/apply-attestation", methods=['GET', 'POST'])
def apply_attestation():
    return management_service.apply_attestation()
