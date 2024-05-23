from flask import Blueprint, redirect, url_for, flash

from rpi_portal.common.rpi_auth_util import RPIAuthUtil

url_prefix = "/register-ass"
register_ass_controller = Blueprint(
    "register_ass_controller",
    __name__,
    url_prefix=url_prefix
)


@register_ass_controller.before_request
def check_member_role():
    if not RPIAuthUtil.is_admin():
        flash("Access denied", "error")
        return redirect(url_for("member_controller.dashboard"))
