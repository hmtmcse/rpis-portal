from pf_flask_auth.common.pffa_auth_util import AuthUtil
from pf_flask_auth.data.pffa_form_auth_data import FormAuthData
from rpi_portal.data.rpi_portal_enum import MemberTypeEnum


class RPIAuthUtil:

    @staticmethod
    def is_admin():
        form_auth_data: FormAuthData = AuthUtil.get_ssr_auth_data()
        if form_auth_data.otherFields and "accessType" in form_auth_data.otherFields and form_auth_data.otherFields["accessType"] == MemberTypeEnum.Admin.value:
            return True
        return False

    @staticmethod
    def is_role(name):
        form_auth_data: FormAuthData = AuthUtil.get_ssr_auth_data()
        if form_auth_data.otherFields and "accessType" in form_auth_data.otherFields and form_auth_data.otherFields["accessType"] == name:
            return True
        return False

    @staticmethod
    def is_student():
        return RPIAuthUtil.is_role(MemberTypeEnum.Student.value)

    @staticmethod
    def is_register():
        return RPIAuthUtil.is_role(MemberTypeEnum.Register.value)

    @staticmethod
    def is_principle():
        return RPIAuthUtil.is_role(MemberTypeEnum.Principle.value)

    @staticmethod
    def is_department():
        return RPIAuthUtil.is_role(MemberTypeEnum.Department.value)
