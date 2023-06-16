from pf_flask_rest.form.pf_app_form_def import FormAppDef
from pf_flask_rest_com.api_def import FileField


class CertificateImportForm(FormAppDef):
    file = FileField(required=True, error_messages={"required": "Please upload file."}, type="file").set_allowed_extension(["csv"])


class MarkSheetImportForm(FormAppDef):
    file = FileField(required=True, error_messages={"required": "Please upload file."}, type="file").set_allowed_extension(["csv"])
