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
from rpi_portal.common.rpi_auth_util import RPIAuthUtil
from rpi_portal.common.template_processor import TemplateProcessor, render
from rpi_portal.data.rpi_portal_enum import MemberTypeEnum, MemberStatus, DataGroupEnum
from rpi_portal.form.member_form import MemberRegistrationForm, MemberEditProfileForm, ResetPasswordBySMSForm, \
    ChangePasswordForm, UploadProfileForm, ResetPasswordForm, OperatorDataDTO, OperatorCreateForm, OperatorUpdateForm
from rpi_portal.model.academic_seba import AcademicSeba
from rpi_portal.model.member import Member
from rpi_portal.service.sms_service import SMSService


class MemberService:
    form_crud_helper = FormCRUDHelper(Member, template_helper=TemplateProcessor())
    city_service = CityService()
    request_processor = RequestProcessor()
    file_upload_man = PFFFFileUploadMan()
    operator_form_service: OperatorFormService = OperatorFormService()
    operator_service = OperatorService()
    sms_service = SMSService()

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
                form_data["isVerified"] = False
                model = self.form_crud_helper.save(form_def=form, data=form_data)
                if model:
                    self.sms_service.send_registration_request(member=model)
                    flash("Registration data received", "success")
                    return redirect(url_for("site_controller.registration_success"))
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
        params = {}
        return self.form_crud_helper.template_helper.render("site/registration-success", params=params)

    def support(self):
        params = {}
        return self.form_crud_helper.template_helper.render("member/support", params=params)

    def my_mark_sheet(self):
        member = self.get_logged_in_member()
        params = {}
        my_mark_sheets = AcademicSeba.query.filter(and_(AcademicSeba.memberId == member.id, AcademicSeba.dataGroup == DataGroupEnum.Sheet.value)).all()

        if not my_mark_sheets:
            _my_mark_sheets = AcademicSeba.query.filter(and_(AcademicSeba.roll == member.roll, AcademicSeba.dataGroup == DataGroupEnum.Sheet.value)).all()
            if _my_mark_sheets:
                for sheet in _my_mark_sheets:
                    sheet.technology = member.technology
                    sheet.session = member.academicSession
                    sheet.shift = member.shift
                    sheet.registration = member.registration
                    sheet.memberId = member.id
                    sheet.save()
            my_mark_sheets = _my_mark_sheets
        params["table"] = my_mark_sheets
        return self.form_crud_helper.template_helper.render("member/mark-sheet", params=params)

    def certificate(self):
        params = {}
        return self.form_crud_helper.template_helper.render("member/certificate", params=params)

    def protoyon_potro(self):
        params = {}
        return self.form_crud_helper.template_helper.render("member/protoyon-potro", params=params)

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
        is_student = RPIAuthUtil.is_student()
        params = {"data": profile_data, "is_student": is_student}
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

    def student_list(self):
        search_fields = ["name", "email", "homeDistrict", "mobile", "session", "passingYear", "technology", "bloodGroup"]
        query = Member.query.filter(Member.accessType == MemberTypeEnum.Student.value)
        return self.form_crud_helper.form_paginated_list("member/member-list", search_fields=search_fields, response_def=MemberRegistrationForm(), query=query)

    def operator_cu(self, id):
        button = "Create"
        form = OperatorCreateForm()
        action_url = url_for("admin_controller.operator_cu")
        is_edit = False
        existing_model = None
        if id:
            button = "Update"
            form = OperatorUpdateForm()
            is_edit = True
            action_url = url_for("admin_controller.operator_cu", id=id)
            existing_model = Member.query.filter(Member.id == id).first()
            form.set_model_value(existing_model)
        params = {"button": button, "action": action_url, "is_edit": is_edit}
        if form.is_post_request() and form.is_valid_data():
            form_data = form.get_requested_data()
            is_email_available = self._is_email_available(form_data, form=form, member_id=id)
            is_username_and_mobile = self._is_username_and_mobile_num_available(form_data, form=form, member_id=id)
            if is_username_and_mobile and is_email_available:
                if existing_model:
                    model = self.form_crud_helper.update(form_def=form, data=form_data, existing_model=existing_model)
                else:
                    model = self.form_crud_helper.save(form_def=form, data=form_data)
                if model:
                    flash(f"Operator {button}", "success")
                    return redirect(url_for("admin_controller.operator_list"))
            else:
                flash("Please check the validation errors", "error")
        return self.form_crud_helper.template_helper.render("operator/operator-cu", params=params, form=form)

    def operator_list(self):
        search_fields = ["name", "email", "homeDistrict"]
        query = Member.query.filter(Member.accessType != MemberTypeEnum.Student.value)
        return self.form_crud_helper.form_paginated_list("operator/operator-list", search_fields=search_fields, response_def=OperatorDataDTO(), query=query)

    def registration_approve(self, model_id: int):
        existing_model = Member.query.filter(and_(Member.id == model_id, Member.isDeleted == False)).first()
        if not existing_model:
            flash("Invalid Student", "error")
            return redirect(url_for("register_controller.registration_approval"))

        existing_model.isVerified = True
        existing_model.status = MemberStatus.Approved.value
        existing_model.save()
        self.sms_service.send_registration_approve(member=existing_model)
        flash(f"Approved", "success")
        return redirect(url_for("register_controller.registration_approval"))

    def member_details(self, model_id: int):
        return self.form_crud_helper.form_details("member/member-details", model_id, url_for("admin_controller.student_list"), display_def=MemberRegistrationForm())

    def upload_profile_photo(self):
        files = self.request_processor.request_helper.file_data()
        member = self.get_logged_in_member()
        files = self.file_upload_man.validate_and_upload(files, UploadProfileForm(), RPIAssetsConfig.profile, {"profilePhoto": member.uuid})
        member.profilePhoto = files["profilePhoto"]
        member.save()
        FormAuthData().ins().update_data(member)
        return {"success": True, "message": "Successfully Uploaded"}

    def reset(self, model_id: int, success_url: str = "admin_controller.student_list"):
        form = ResetPasswordForm()
        params = {"id": model_id, "redirect_to": success_url}
        if form.is_post_request() and form.is_valid_data():
            data = form.get_data()
            model_id = PyDataUtil.get_dict_value(data, "id")
            success_url = PyDataUtil.get_dict_value(data, "redirect_to", success_url)
            operator = self.operator_service.get_operator_by_id(model_id)
            if not operator:
                form.definition.set_field_errors({"confirmPassword": "Invalid operator"})
            else:
                operator.password = form.confirmPassword
                operator.save()
                flash("Successfully reset!", "success")
                redirect_url = url_for(success_url)
                return redirect(redirect_url)
        return self.form_crud_helper.render_view(view_name="member/reset", form=form, params=params)

    def pending_registration_list(self):
        search_fields = ["name", "mobile", "roll", "registration"]
        query = Member.query.filter(and_(Member.accessType == MemberTypeEnum.Student.value, Member.isVerified == False, Member.status == MemberStatus.Pending.value))
        return self.form_crud_helper.form_paginated_list("register/registration-pending", search_fields=search_fields, response_def=MemberRegistrationForm(), query=query)

    def get_student_by_roll(self, roll):
        return Member.query.filter(and_(Member.roll == roll, Member.isDeleted == False)).first()
