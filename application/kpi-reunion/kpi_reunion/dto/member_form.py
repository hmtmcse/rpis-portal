from marshmallow import fields, validates_schema, ValidationError
from bl_common.common.CommonHelper import CommonHelper
from bl_common.common.common_validation import CommonValidation
from kpi_reunion.data.kpi_reunio_enum import MemberTypeEnum, SessionEnum, BloodGroup, PassingYear, Technology, Shift
from kpi_reunion.model.member import Member
from pf_flask_auth.dto.default_dto import OperatorDTO
from pf_flask_rest.form.pf_app_form_def import FormAppDef, FormBaseDef
from pf_flask_rest_com.api_def import FileField
from pf_flask_rest_com.common.pffrc_enum_helper import EnumField


class MemberDetailsForm(FormAppDef):

    class Meta:
        model = Member
        load_instance = True

    firstName = fields.String(required=True, error_messages={"required": "Please enter first name"})
    lastName = fields.String(allow_none=True)
    email = fields.String(required=True, error_messages={"required": "Please enter email"})
    accessType = EnumField(MemberTypeEnum, required=True, error_messages={"required": "Please enter access type"})

    @validates_schema
    def validates_schema(self, data, **kwargs):
        self.enum_to_string(data, "accessType")

    def enum_to_string(self, data, name):
        if name in data and data[name]:
            data[name] = str(data[name])


class MemberCreateForm(MemberDetailsForm):
    class Meta:
        model = Member
        load_instance = True

    password = fields.String(required=True, error_messages={"required": "Please enter password"}, type="password")


class MemberUpdateForm(MemberDetailsForm):
    class Meta:
        model = Member
        load_instance = True

    id = fields.Integer(required=True, error_messages={"required": "Please enter id"}, type="hidden", isIgnoreLabel=True)


class ResetPasswordForm(FormBaseDef):
    newPassword = fields.String(required=True, error_messages={"required": "Please enter new password."}, type="password")
    confirmPassword = fields.String(required=True, error_messages={"required": "Please enter confirm password."}, type="password")
    id = fields.Integer(required=True, error_messages={"required": "Please enter id"})

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data["newPassword"] != data["confirmPassword"]:
            raise ValidationError("New password & confirm password not matched!", "confirmPassword")


class MemberDetailsDTO(OperatorDTO):
    accessType = EnumField(MemberTypeEnum, required=True, error_messages={"required": "Please enter access type"})

    @validates_schema
    def validates_schema(self, data, **kwargs):
        self.enum_to_string(data, "accessType")

    def enum_to_string(self, data, name):
        if name in data and data[name]:
            data[name] = str(data[name])


class MemberRegistrationForm(FormAppDef):
    class Meta:
        model = Member
        load_instance = True

    name = fields.String(required=True, error_messages={"required": "Please enter name"})
    emergencyContact = fields.String(allow_none=True)
    email = fields.String(allow_none=True)
    homeDistrict = fields.String(required=True, error_messages={"required": "Please select home district"}, type="select", inputAttrClass="searchable-select")
    password = fields.String(required=True, error_messages={"required": "Please enter password"}, type="password")
    mobile = fields.String(required=True, error_messages={"required": "Please enter mobile"})
    username = fields.String(allow_none=True)
    session = EnumField(SessionEnum, required=True, error_messages={"required": "Please select session"}, selectOptionLabel="value", selectFirstEntry="Session")
    shift = EnumField(Shift, required=True, error_messages={"required": "Please select shift"}, selectOptionLabel="value", selectFirstEntry="Shift")
    passingYear = EnumField(PassingYear, required=True, error_messages={"required": "Please select passing year"}, selectOptionLabel="value", selectFirstEntry="Passing Year")
    technology = EnumField(Technology, required=True, error_messages={"required": "Please select technology"}, selectOptionLabel="value", selectFirstEntry="Technology")
    bloodGroup = EnumField(BloodGroup, selectOptionLabel="value", selectFirstEntry="Blood Group")

    presentAddress = fields.String(type="textarea")
    permanentAddress = fields.String(type="textarea")
    jobDetails = fields.String(type="textarea")
    jobAddress = fields.String(type="textarea")

    @validates_schema
    def validates_schema(self, data, **kwargs):
        CommonHelper.enum_to_string(data, "session")
        CommonHelper.enum_to_string(data, "shift")
        CommonHelper.enum_to_string(data, "passingYear")
        CommonHelper.enum_to_string(data, "technology")
        CommonHelper.enum_to_string(data, "bloodGroup")
        CommonValidation.validate_bd_mobile_email(data)


class MemberEditProfileForm(MemberRegistrationForm):
    class Meta:
        model = Member
        load_instance = True
        exclude = ('password',)

    id = fields.Integer(required=True, error_messages={"required": "Please enter id"}, type="hidden", isIgnoreLabel=True)


class ChangePasswordForm(FormAppDef):
    currentPassword = fields.String(required=True, error_messages={"required": "Please enter current password."}, type="password")
    newPassword = fields.String(required=True, error_messages={"required": "Please enter new password."}, type="password")
    confirmPassword = fields.String(required=True, error_messages={"required": "Please enter confirm password."}, type="password")

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data["newPassword"] != data["confirmPassword"]:
            raise ValidationError("New password & confirm password not matched!", "confirmPassword")


class UploadCoverForm(FormAppDef):
    coverPhoto = FileField(required=True, error_messages={"required": "Please upload file."}).set_allowed_extension(["jpg", "png", "jpeg"])


class UploadProfileForm(FormAppDef):
    profilePhoto = FileField(required=True, error_messages={"required": "Please upload file."}).set_allowed_extension(["jpg", "png", "jpeg"])


class EventRegistrationForm(FormAppDef):
    adult = fields.Float()
    child = fields.Float()


class ResetPasswordBySMSForm(FormAppDef):
    mobile = fields.String(required=True, error_messages={"required": "Please enter mobile"})
    passingYear = EnumField(PassingYear, required=True, error_messages={"required": "Please select passing year"}, selectOptionLabel="value", selectFirstEntry="Passing Year")

    @validates_schema
    def validates_schema(self, data, **kwargs):
        CommonHelper.enum_to_string(data, "passingYear")
        CommonValidation.validate_bd_mobile_email(data)
