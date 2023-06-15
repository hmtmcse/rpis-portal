from flask import url_for, redirect, flash
from sqlalchemy import and_
from application.config.app_config import Config
from bdash.security.web_security import WebSecurity
from pf_flask_auth.common.pffa_auth_util import AuthUtil
from pf_flask_auth.data.pffa_form_auth_data import FormAuthData
from pf_flask_auth.service.operator_form_service import OperatorFormService
from pf_flask_auth.service.operator_service import OperatorService
from pf_flask_file.pfff_file_upload_man import PFFFFileUploadMan
from pf_flask_rest.helper.pf_flask_form_crud_helper import FormCRUDHelper
from pf_flask_rest.pf_flask_request_processor import RequestProcessor
from pf_messaging.sms.sms_sender import SMSSender
from pf_messaging.structure.sms_abc import SMSABC
from pf_py_common.py_common import PyCommon
from pf_py_common.py_data_util import PyDataUtil
from region.service.city_service import CityService
from rpi_portal.common.rpi_assets_config import RPIAssetsConfig
from rpi_portal.common.template_processor import TemplateProcessor, render
from rpi_portal.form.member_form import MemberRegistrationForm, MemberEditProfileForm, ResetPasswordBySMSForm, \
    ChangePasswordForm, UploadProfileForm, ResetPasswordForm
from rpi_portal.model.member import Member


class MemberService:
    form_crud_helper = FormCRUDHelper(Member, template_helper=TemplateProcessor())
    city_service = CityService()
    request_processor = RequestProcessor()
    file_upload_man = PFFFFileUploadMan()
    operator_form_service: OperatorFormService = OperatorFormService()
    operator_service = OperatorService()

    def is_username_available(self, username: str, member_id=None):
        member = Member.query.filter(and_(Member.isDeleted == False, Member.username == username)).first()
        if member:
            if member_id and member.id == member_id:
                return True
            return False
        return True

    def is_email_available(self, email: str, member_id=None):
        member = Member.query.filter(and_(Member.isDeleted == False, Member.email == email)).first()
        if member:
            if member_id and member.id == member_id:
                return True
            return False
        return True

    def is_mobile_available(self, mobile: str, member_id=None):
        member = Member.query.filter(and_(Member.isDeleted == False, Member.mobile == mobile)).first()
        if member:
            if member_id and member.id == member_id:
                return True
            return False
        return True

    def get_member_by_mobile_and_passing_year(self, mobile: str, passing_year: str):
        member = Member.query.filter(and_(Member.isDeleted == False, Member.mobile == mobile, Member.passingYear == passing_year)).first()
        if not member:
            return None
        return member

    def _is_username_and_mobile_num_available(self, form_data, form, member_id=None):
        mobile = PyDataUtil.get_dict_value(form_data, "mobile")
        if not mobile:
            return False
        form_data["mobile"] = mobile = mobile.strip()
        form_data["username"] = mobile
        is_available_mobile = self.is_mobile_available(mobile, member_id=member_id)
        is_available_username = self.is_username_available(mobile, member_id=member_id)
        if not is_available_mobile or not is_available_username:
            form.set_field_error("mobile", "Already used")
            return False
        return True

    def _is_email_available(self, form_data, form, member_id=None):
        email = PyDataUtil.get_dict_value(form_data, "email")
        if not email or email == "":
            form_data["email"] = None
            return True
        is_email_available = self.is_email_available(email, member_id=member_id)
        if not is_email_available:
            form.set_field_error("email", "Already used")
            return False
        return True

    def registration(self):
        params = {"button": "Create", "action": "site_controller.registration"}
        form = MemberRegistrationForm()
        response = self.city_service.name_only_dropdown()
        if response and response.json:
            district = response.json["data"]
            form.set_select_option("homeDistrict", district, "name", "name")

        if form.is_post_request() and form.is_valid_data() and WebSecurity.verify_recaptcha(Config.RECAPTCHA_SECRET_KEY):
            form_data = form.get_requested_data()
            is_email_available = self._is_email_available(form_data, form=form)
            is_username_and_mobile = self._is_username_and_mobile_num_available(form_data, form=form)
            if is_username_and_mobile and is_email_available:
                model = self.form_crud_helper.save(form_def=form, data=form_data)
                if model:
                    username = PyDataUtil.get_dict_value(form_data, "username")
                    password = PyDataUtil.get_dict_value(form_data, "password")
                    self.operator_form_service.login_by_credential(username, password)
                    flash("Registration success", "success")
                    return redirect(url_for("site_controller.event_booking"))
            else:
                flash("Please check the validation errors", "error")
        return self.form_crud_helper.template_helper.render("site/bismillah", params=params, form=form)

    def update_profile(self):
        params = {"button": "Create", "action": "member_controller.update_profile"}
        form = MemberEditProfileForm()
        response = self.city_service.name_only_dropdown()
        if response and response.json:
            district = response.json["data"]
            form.set_select_option("homeDistrict", district, "name", "name")

        member = self.get_logged_in_member()
        if form.is_post_request() and form.is_valid_data() and member:
            form_data = form.get_requested_data()
            is_email_available = self._is_email_available(form_data, form=form, member_id=member.id)
            is_username_and_mobile = self._is_username_and_mobile_num_available(form_data, form=form, member_id=member.id)
            if is_username_and_mobile and is_email_available:
                model = self.form_crud_helper.update(form_def=form, data=form_data, existing_model=member)
                if model:
                    flash("Successfully Profile Updated", "success")
                    return redirect(url_for("member_controller.profile"))
            else:
                flash("Please check the validation errors", "error")
        else:
            if not member:
                flash("Information not found", "error")
                return redirect(url_for("member_controller.profile"))
            form.set_model_value(member)
        return self.form_crud_helper.template_helper.render("member/update-profile", params=params, form=form)

    def send_password(self, mobile, password):
        if Config.SMS_PROVIDER and Config.SMS_API_URL and Config.SMS_API_TOKEN:
            sms_sender: SMSABC = SMSSender.instance(Config.SMS_PROVIDER)
            if not sms_sender:
                return
            sms_sender.setup(url=Config.SMS_API_URL, token=Config.SMS_API_TOKEN)
            message = f"Welcome to KPI Reunion\n"
            message += f"Your New Password is: {password}"
            sms_sender.send(mobile, message=message)

    def reset_password(self):
        reset_done = False
        params = {}
        form = ResetPasswordBySMSForm()
        if form.is_post_request() and form.is_valid_data() and WebSecurity.verify_recaptcha(Config.RECAPTCHA_SECRET_KEY):
            form_data = form.get_requested_data()
            mobile = PyDataUtil.get_dict_value(form_data, "mobile")
            passing_year = PyDataUtil.get_dict_value(form_data, "passingYear")
            member = self.get_member_by_mobile_and_passing_year(mobile=mobile, passing_year=passing_year)
            if member:
                new_password = PyCommon.get_random_6digit()
                member.password = new_password
                self.send_password(mobile=mobile, password=new_password)
                member.save()
                reset_done = True
            else:
                flash("Invalid reset password request", "error")
        return self.form_crud_helper.template_helper.render("auth/reset-password", params={"reset_done": reset_done}, form=form)

    def registration_success(self):
        params = {"button": "Create", "action": "site_controller.registration"}
        form = MemberRegistrationForm()
        return self.form_crud_helper.form_create("site/registration-success", form, params=params, redirect_url=url_for("site_controller.bismillah"))

    def support(self):
        params = {}
        return self.form_crud_helper.template_helper.render("member/support", params=params)

    def get_logged_in_member(self):
        form_auth_data: FormAuthData = AuthUtil.get_ssr_auth_data()
        if not form_auth_data or not form_auth_data.isLoggedIn:
            return None
        member_info = Member.query.filter(and_(Member.isDeleted == False, Member.id == form_auth_data.id)).first()
        return member_info

    def get_profile_data(self):
        return self.get_logged_in_member()

    def profile(self, form=ChangePasswordForm()):
        profile_data = self.get_profile_data()
        params = {"data": profile_data}
        return render("member/profile", params, form=form)

    def change_password(self):
        form = ChangePasswordForm()
        if form.is_post_request() and form.is_valid_data():
            data = form.get_requested_data()
            member = self.get_logged_in_member()
            current_password = PyDataUtil.get_dict_value(data, "currentPassword")
            if not member or not member.verify_password(current_password):
                flash("Invalid Request", "error")
            else:
                member.password = PyDataUtil.get_dict_value(data, "confirmPassword")
                member.save()
                flash("Successfully Password Changed", "success")
                return redirect(url_for("member_controller.profile"))
        return self.profile(form=form)

    def member_list(self):
        search_fields = ["name", "email", "homeDistrict", "mobile", "session", "passingYear", "technology", "bloodGroup"]
        return self.form_crud_helper.form_paginated_list("member/member-list", search_fields=search_fields, response_def=MemberRegistrationForm())

    def member_details(self, model_id: int):
        return self.form_crud_helper.form_details("member/member-details", model_id, url_for("admin_controller.member_list"), display_def=MemberRegistrationForm())

    def upload_profile_photo(self):
        files = self.request_processor.request_helper.file_data()
        member = self.get_logged_in_member()
        files = self.file_upload_man.validate_and_upload(files, UploadProfileForm(), RPIAssetsConfig.profile, {"profilePhoto": member.uuid})
        member.profilePhoto = files["profilePhoto"]
        member.save()
        FormAuthData().ins().update_data(member)
        return {"success": True, "message": "Successfully Uploaded"}

    def reset(self, model_id: int):
        form = ResetPasswordForm()
        params = {"id": model_id}
        if form.is_post_request() and form.is_valid_data():
            data = form.get_data()
            model_id = PyDataUtil.get_dict_value(data, "id")
            operator = self.operator_service.get_operator_by_id(model_id)
            if not operator:
                form.definition.set_field_errors({"confirmPassword": "Invalid operator"})
            else:
                operator.password = form.confirmPassword
                operator.save()
                flash("Successfully reset!", "success")
                redirect_url = url_for("admin_controller.member_list")
                return redirect(redirect_url)
        return self.form_crud_helper.render_view(view_name="member/reset", form=form, params=params)

