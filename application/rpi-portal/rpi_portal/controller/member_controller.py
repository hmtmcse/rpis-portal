from flask import Blueprint
from rpi_portal.common.template_processor import render
from rpi_portal.service.member_service import MemberService

url_prefix = "/member"
member_controller = Blueprint(
    "member_controller",
    __name__,
    url_prefix=url_prefix
)

member_service = MemberService()


@member_controller.route("/dashboard", methods=['POST', 'GET'])
def dashboard():
    return render("member/dashboard", {})


@member_controller.route("/support", methods=['GET'])
def support():
    return member_service.support()


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
