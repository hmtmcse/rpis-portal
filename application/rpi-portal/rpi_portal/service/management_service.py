from pf_flask_rest.helper.pf_flask_form_crud_helper import FormCRUDHelper
from rpi_portal.common.template_processor import TemplateProcessor
from rpi_portal.form.management_form import MarkSheetImportForm, CertificateImportForm
from rpi_portal.model.member import Member


class ManagementService:
    form_crud_helper = FormCRUDHelper(Member, template_helper=TemplateProcessor())

    def import_mark_sheet(self):
        params = {}
        form = MarkSheetImportForm()
        return self.form_crud_helper.template_helper.render("management/import-mark-sheet", params=params, form=form)

    def import_certificate(self):
        params = {}
        form = CertificateImportForm()
        return self.form_crud_helper.template_helper.render("management/import-certificate", params=params, form=form)
