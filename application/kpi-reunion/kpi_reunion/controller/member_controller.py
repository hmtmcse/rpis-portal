from flask import Blueprint
from kpi_reunion.common.template_processor import render
from kpi_reunion.service.event_service import EventService
from kpi_reunion.service.member_service import MemberService

url_prefix = "/member"
member_controller = Blueprint(
    "member_controller",
    __name__,
    url_prefix=url_prefix
)

member_service = MemberService()
event_service = EventService()


@member_controller.route("/dashboard", methods=['POST', 'GET'])
def dashboard():
    event = event_service.get_my_event()
    return render("member/dashboard", {"event": event})


@member_controller.route("/my-event", methods=['GET'])
def my_event():
    event = event_service.get_my_event()
    return render("member/my-event", {"event": event})


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


@member_controller.route("/my-invitation", methods=['GET'])
def my_invitation():
    return member_service.my_invitation()


@member_controller.route("/download-invitation", methods=['GET'])
def download_invitation():
    return member_service.my_invitation(True)


@member_controller.route("/upload-profile-photo", methods=['POST'])
def upload_profile_photo():
    return member_service.upload_profile_photo()
