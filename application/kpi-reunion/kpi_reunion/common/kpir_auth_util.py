from kpi_reunion.data.kpi_reunio_enum import MemberTypeEnum
from pf_flask_auth.common.pffa_auth_util import AuthUtil
from pf_flask_auth.data.pffa_form_auth_data import FormAuthData


class KPIRAuthUtil:

    @staticmethod
    def is_admin():
        form_auth_data: FormAuthData = AuthUtil.get_ssr_auth_data()
        if form_auth_data.otherFields and "accessType" in form_auth_data.otherFields and form_auth_data.otherFields["accessType"] == MemberTypeEnum.Admin.value:
            return True
        return False

    @staticmethod
    def is_manager():
        form_auth_data: FormAuthData = AuthUtil.get_ssr_auth_data()
        if form_auth_data.otherFields and "accessType" in form_auth_data.otherFields and form_auth_data.otherFields["accessType"] == MemberTypeEnum.Manager.value:
            return True
        return False


    @staticmethod
    def is_volunteer():
        form_auth_data: FormAuthData = AuthUtil.get_ssr_auth_data()
        if form_auth_data.otherFields and "accessType" in form_auth_data.otherFields and form_auth_data.otherFields["accessType"] == MemberTypeEnum.Volunteer.value:
            return True
        return False