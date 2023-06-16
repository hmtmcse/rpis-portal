from pf_flask_file.pfff_file_upload_man import PFFFFileUploadMan
from pf_flask_rest.helper.pf_flask_form_crud_helper import FormCRUDHelper
from pf_flask_rest.pf_flask_request_processor import RequestProcessor
from rpi_portal.common.rpi_assets_config import RPIAssetsConfig
from rpi_portal.common.template_processor import TemplateProcessor
from rpi_portal.form.management_form import MarkSheetImportForm, CertificateImportForm
from rpi_portal.model.academic_seba import AcademicSeba


class ManagementService:
    request_processor = RequestProcessor()
    form_crud_helper = FormCRUDHelper(AcademicSeba, template_helper=TemplateProcessor())
    file_upload_man = PFFFFileUploadMan()

    def import_mark_sheet(self):
        params = {}
        form = MarkSheetImportForm()
        if form.is_post_request() and form.is_valid_data():
            files = self.request_processor.request_helper.file_data()
            uploaded_files = self.file_upload_man.validate_and_upload(files, form, RPIAssetsConfig.register, {"file": "uploaded-mark-sheet"})
            print("--")
        return self.form_crud_helper.template_helper.render("register/mark-sheet-import", params=params, form=form)

    def import_certificate(self):
        params = {}
        form = CertificateImportForm()
        return self.form_crud_helper.template_helper.render("register/certificate-import", params=params, form=form)

    def mark_sheet(self):
        search_fields = ["roll", "technology", "session", "name", "registration"]
        return self.form_crud_helper.form_paginated_list("register/mark-sheet", search_fields=search_fields)
