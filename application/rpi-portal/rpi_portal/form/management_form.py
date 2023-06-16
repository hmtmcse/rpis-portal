from marshmallow import fields
from pf_flask_rest.form.pf_app_form_def import FormAppDef
from pf_flask_rest_com.api_def import FileField
from rpi_portal.model.academic_seba import AcademicSeba


class ProcessRequestForm(FormAppDef):

    class Meta:
        model = AcademicSeba
        load_instance = True

    appointmentDate = fields.Date(required=True, format="%d/%m/%Y", label="Appointment Date", inputAttrClass="add-datepicker", attributes="autocomplete='off'")
    response = fields.String(allow_none=True, type="textarea")
    token = fields.String(allow_none=True)


class ResolveRequestForm(FormAppDef):
    pass


class CertificateImportForm(FormAppDef):
    file = FileField(required=True, error_messages={"required": "Please upload file."}, type="file").set_allowed_extension(["csv"])


class MarkSheetImportForm(FormAppDef):
    file = FileField(required=True, error_messages={"required": "Please upload file."}, type="file").set_allowed_extension(["csv"])
