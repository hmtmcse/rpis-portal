from marshmallow import fields, validates_schema, ValidationError
from bl_common.common.CommonHelper import CommonHelper
from bl_common.common.common_validation import CommonValidation
from pf_flask_auth.dto.default_dto import OperatorDTO
from pf_flask_rest.form.pf_app_form_def import FormAppDef, FormBaseDef
from pf_flask_rest_com.api_def import FileField
from pf_flask_rest_com.common.pffrc_enum_helper import EnumField
from rpi_portal.data.rpi_portal_enum import MemberTypeEnum, Technology, Shift, BloodGroup
from rpi_portal.model.member import Member


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

    mobile = fields.String(required=True, error_messages={"required": "Please enter mobile"})
    emergencyContact = fields.String(allow_none=True)
    technology = EnumField(Technology, required=True, error_messages={"required": "Please select technology"}, selectOptionLabel="value", selectFirstEntry="Technology")
    academicSession = fields.String(required=True, error_messages={"required": "Please enter session"}, type="select")
    shift = EnumField(Shift, required=True, error_messages={"required": "Please select shift"}, selectOptionLabel="value", selectFirstEntry="Shift")

    roll = fields.String(required=True, error_messages={"required": "Please enter roll number"})
    registration = fields.String(required=True, error_messages={"required": "Please enter registration number"})
    passingYear = fields.String(error_messages={"required": "Please enter passing year"})

    homeDistrict = fields.String(required=True, error_messages={"required": "Please select home district"}, type="select", inputAttrClass="searchable-select")
    bloodGroup = EnumField(BloodGroup, selectOptionLabel="value", selectFirstEntry="Blood Group")

    name = fields.String(required=True, error_messages={"required": "Please enter name"})

    email = fields.String(allow_none=True)

    password = fields.String(required=True, error_messages={"required": "Please enter password"}, type="password")

    username = fields.String(allow_none=True)

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


class ResetPasswordBySMSForm(FormAppDef):
    mobile = fields.String(required=True, error_messages={"required": "Please enter mobile"})

    @validates_schema
    def validates_schema(self, data, **kwargs):
        CommonHelper.enum_to_string(data, "passingYear")
        CommonValidation.validate_bd_mobile_email(data)
