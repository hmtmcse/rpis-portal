import os.path
import qrcode
from flask import url_for
from application.config.app_config import Config
from bdash.security.web_security import WebSecurity
from pf_flask_auth.common.pffa_auth_util import AuthUtil
from pf_flask_auth.data.pffa_form_auth_data import FormAuthData
from pf_flask_rest_com.pf_flask_request_helper import request_helper
from pf_py_file.pfpf_file_util import FileUtil
from rpi_portal.common.rpi_assets_config import RPIAssetsConfig


class TemplateUtil:

    @property
    def base_url(self):
        info = request_helper.get_url_info()
        return info.baseURL

    def recaptcha(self, action="recaptcha"):
        return WebSecurity.recaptcha(Config.RECAPTCHA_SITE_KEY, action)

    @property
    def profile_photo_url(self):
        form_auth_data: FormAuthData = AuthUtil.get_ssr_auth_data()
        if form_auth_data.profilePhoto:
            return f"/assets/profile/{form_auth_data.profilePhoto}"
        return url_for('rpi-portal.static', filename='img/profile-photo.jpg')

    @property
    def session_data(self):
        form_auth_data: FormAuthData = AuthUtil.get_ssr_auth_data()
        return form_auth_data

    @property
    def account_name(self):
        form_auth_data: FormAuthData = AuthUtil.get_ssr_auth_data()
        return form_auth_data.name

    @property
    def qr_code_image(self):
        form_auth_data: FormAuthData = AuthUtil.get_ssr_auth_data()
        file_name = form_auth_data.uuid + ".png"
        FileUtil.create_directories(RPIAssetsConfig.qrcode)
        path = os.path.join(RPIAssetsConfig.qrcode, file_name)
        if not os.path.exists(path):
            img = qrcode.make(form_auth_data.uuid)
            type(img)
            img.save(path)
        return f"/assets/qrcode/{file_name}"

    @property
    def session_dropdown_data(self):
        start_year = 2000
        select_options = []
        for year in range(0, 23):
            current_year = start_year + year
            year = f"{current_year}-{current_year + 1}"
            select_options.append(year)
        return select_options
