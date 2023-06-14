from flask import Blueprint, redirect, url_for
from kpi_reunion.service.event_service import EventService
from kpi_reunion.service.member_service import MemberService

url_prefix = "/"
site_controller = Blueprint(
    "site_controller",
    __name__,
    url_prefix=url_prefix
)

member_service = MemberService()
event_service = EventService()


@site_controller.route("/", methods=['GET'])
def bismillah():
    return member_service.registration()


@site_controller.route("/registration", methods=['POST', 'GET'])
def registration():
    return member_service.registration()


@site_controller.route("/reset-password", methods=['POST', 'GET'])
def reset_password():
    return member_service.reset_password()


@site_controller.route("/registration-success", methods=['POST', 'GET'])
def registration_success():
    return redirect(url_for("site_controller.bismillah"))
    # return member_service.registration_success()


@site_controller.route("/event-booking", methods=['POST', 'GET'])
def event_booking():
    return event_service.event_booking()


@site_controller.route("/event-booking-manage", methods=['GET'])
def event_booking_manage():
    return event_service.event_booking_manage()


@site_controller.route("/payment-reference", methods=['POST', 'GET'])
def payment_reference():
    return member_service.payment_reference()


@site_controller.route("/robots.txt", methods=['GET'])
def robots_txt():
    return """
        User-agent: *
        Disallow: /
    """
