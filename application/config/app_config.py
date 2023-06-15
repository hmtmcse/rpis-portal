from pf_flask_auth.dto.default_dto import OperatorDTO
from pf_flask_auth.model.pffa_abstract_model import OperatorAbstract
from rpi_portal.form.member_form import MemberDetailsDTO
from rpi_portal.model.member import Member


class Config:
    APP_NAME = "RPI Portal"
    PORT: int = 1911

    SECRET_KEY: str = 'rpi_portal_secret_key_base'

    ENABLE_AUTH_SYSTEM: bool = True
    LOGIN_IDENTIFIER: str = "username"
    SUCCESS_REDIRECT = "/member/dashboard"

    ENABLE_DEFAULT_AUTH_MODEL: bool = False
    CUSTOM_OPERATOR_MODEL: OperatorAbstract = Member
    CUSTOM_OPERATOR_DTO: OperatorDTO = MemberDetailsDTO
    CUSTOM_OPERATOR_ADDITIONAL_FIELDS: list = [
        {
            "name": "accessType"
        }
    ]

    SKIP_URL_LIST: list = [
        "/registration",
        "/registration-success",
        "/payment-reference",
        "/robots.txt",
    ]

    # Swagger Configuration
    ENABLE_SWAGGER_VIEW_PAGE: bool = True
    ENABLE_SWAGGER_PAGE_AUTH: bool = False
    SWAGGER_ENABLE: bool = True
    SWAGGER_TITLE: str = "Reunion"

    # API
    ENABLE_API_AUTH: bool = True
    ENABLE_API_END_POINTS: bool = True
    SWAGGER_ENABLE_JWT_AUTH_GLOBAL: bool = True

    SKIP_START_WITH_URL_LIST: list = [
        "/ir-assets"
    ]

    TEMPLATE_PATH = "../template-assets/templates"
    ASSETS_PATH = "../template-assets/ir-assets"
    ASSETS_URL = "ir-assets"

    RECAPTCHA_SITE_KEY: str = "6Lcyh88kAAAAAP_6HJYq2bx0kwcV1Vl25_tpGL_t"
    RECAPTCHA_SECRET_KEY: str = "6Lcyh88kAAAAAO1yvpADdnuhUUk7B0mc3c58ccxa"

    SMS_PROVIDER: str = None
    SMS_API_URL: str = None
    SMS_API_TOKEN: str = None

