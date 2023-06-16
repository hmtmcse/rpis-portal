import csv
import os.path
from datetime import datetime

from flask import redirect, url_for, flash
from sqlalchemy import and_, or_
from pf_flask_file.pfff_file_upload_man import PFFFFileUploadMan
from pf_flask_rest.helper.pf_flask_form_crud_helper import FormCRUDHelper
from pf_flask_rest.pf_flask_request_processor import RequestProcessor
from pf_py_common.py_common import PyCommon
from pf_py_common.py_data_util import PyDataUtil
from rpi_portal.common.rpi_assets_config import RPIAssetsConfig
from rpi_portal.common.template_processor import TemplateProcessor
from rpi_portal.data.rpi_portal_enum import MarkSheetStatus, DataGroupEnum
from rpi_portal.form.management_form import MarkSheetImportForm, CertificateImportForm, ProcessRequestForm, \
    ResolveRequestForm
from rpi_portal.model.academic_seba import AcademicSeba
from rpi_portal.service.member_service import MemberService


class ManagementService:
    request_processor = RequestProcessor()
    form_crud_helper = FormCRUDHelper(AcademicSeba, template_helper=TemplateProcessor())
    file_upload_man = PFFFFileUploadMan()
    member_service = MemberService()

    def get_mark_sheet_name(self, key):
        if key == "1st":
            return "First Semester"
        elif key == "2nd":
            return "Second Semester"
        elif key == "3rd":
            return "Third Semester"
        elif key == "4th":
            return "Fourth Semester"
        elif key == "5th":
            return "Fifth Semester"
        elif key == "6th":
            return "Six Semester"
        elif key == "7th":
            return "Seven Semester"
        elif key == "8th":
            return "Eight Semester"
        return "Unknown"

    def import_mark_sheet(self):
        params = {}
        form = MarkSheetImportForm()
        if form.is_post_request() and form.is_valid_data():
            files = self.request_processor.request_helper.file_data()
            uploaded_files = self.file_upload_man.validate_and_upload(files, form, RPIAssetsConfig.register, {"file": "uploaded-mark-sheet"})
            file_name = uploaded_files["file"]
            file_path = os.path.join(RPIAssetsConfig.register, file_name)

            if not file_name or not os.path.exists(file_path):
                flash(f"Invalid file", "error")
                return redirect(url_for("register_controller.mark_sheet"))

            with open(file_path, 'r') as csv_file:
                csvreader = csv.reader(csv_file)
                next(csvreader, None)
                index = 2
                for row in csvreader:
                    if len(row) < 3:
                        continue
                    roll = row[0].strip()
                    semester = row[1].strip()
                    status = row[2].strip()

                    if not roll or not semester:
                        continue

                    student = self.member_service.get_student_by_roll(roll)
                    existing_entry: AcademicSeba = AcademicSeba.query.filter(and_(AcademicSeba.roll == roll, AcademicSeba.semester == semester, AcademicSeba.dataGroup == DataGroupEnum.Sheet.value)).first()
                    if not existing_entry:
                        existing_entry = AcademicSeba()

                    if not existing_entry.status and not status:
                        existing_entry.status = MarkSheetStatus.NotReceived.value
                    elif not existing_entry.status and status:
                        existing_entry.status = status

                    existing_entry.name = self.get_mark_sheet_name(semester)
                    existing_entry.semester = semester
                    existing_entry.roll = roll
                    existing_entry.dataGroup = DataGroupEnum.Sheet.value

                    if student:
                        existing_entry.technology = student.technology
                        existing_entry.session = student.academicSession
                        existing_entry.shift = student.shift
                        existing_entry.registration = student.registration
                        existing_entry.memberId = student.id

                    existing_entry.save()
                    index += 1

                flash(f"Successfully Imported", "success")
                return redirect(url_for("register_controller.mark_sheet"))

        return self.form_crud_helper.template_helper.render("register/mark-sheet-import", params=params, form=form)

    def import_certificate(self):
        params = {}
        form = CertificateImportForm()
        if form.is_post_request() and form.is_valid_data():
            files = self.request_processor.request_helper.file_data()
            uploaded_files = self.file_upload_man.validate_and_upload(files, form, RPIAssetsConfig.register, {"file": "uploaded-certificate"})
            file_name = uploaded_files["file"]
            file_path = os.path.join(RPIAssetsConfig.register, file_name)

            if not file_name or not os.path.exists(file_path):
                flash(f"Invalid file", "error")
                return redirect(url_for("register_controller.certificate"))

            with open(file_path, 'r') as csv_file:
                csvreader = csv.reader(csv_file)
                next(csvreader, None)
                index = 2
                for row in csvreader:
                    if len(row) < 3:
                        continue
                    roll = row[0].strip()
                    certificate = row[1].strip()
                    status = row[2].strip()

                    if not roll or not certificate:
                        continue

                    student = self.member_service.get_student_by_roll(roll)
                    existing_entry: AcademicSeba = AcademicSeba.query.filter(
                        and_(AcademicSeba.roll == roll, AcademicSeba.name == certificate,
                             AcademicSeba.dataGroup == DataGroupEnum.Certificate.value)).first()
                    if not existing_entry:
                        existing_entry = AcademicSeba()

                    if not existing_entry.status and not status:
                        existing_entry.status = MarkSheetStatus.NotReceived.value
                    elif not existing_entry.status and status:
                        existing_entry.status = status

                    existing_entry.name = certificate
                    existing_entry.roll = roll
                    existing_entry.dataGroup = DataGroupEnum.Certificate.value

                    if student:
                        existing_entry.technology = student.technology
                        existing_entry.session = student.academicSession
                        existing_entry.shift = student.shift
                        existing_entry.registration = student.registration
                        existing_entry.memberId = student.id

                    existing_entry.save()
                    index += 1

                flash(f"Successfully Imported", "success")
                return redirect(url_for("register_controller.certificate"))
        return self.form_crud_helper.template_helper.render("register/certificate-import", params=params, form=form)

    def mark_sheet(self):
        search_fields = ["roll", "technology", "session", "name", "registration"]
        query = AcademicSeba.query.filter(and_(AcademicSeba.dataGroup == DataGroupEnum.Sheet.value))
        return self.form_crud_helper.form_paginated_list("register/mark-sheet", search_fields=search_fields, query=query)

    def certificate(self):
        search_fields = ["roll", "technology", "session", "name", "registration"]
        query = AcademicSeba.query.filter(and_(AcademicSeba.dataGroup == DataGroupEnum.Certificate.value))
        return self.form_crud_helper.form_paginated_list("register/certificate", search_fields=search_fields, query=query)

    def adjust_mark_sheet_mapping(self, member):
        my_mark_sheets = AcademicSeba.query.filter(and_(AcademicSeba.roll == member.roll, AcademicSeba.dataGroup == DataGroupEnum.Sheet.value, AcademicSeba.memberId == None)).all()
        if not my_mark_sheets:
            return

        for sheet in my_mark_sheets:
            sheet.technology = member.technology
            sheet.session = member.academicSession
            sheet.shift = member.shift
            sheet.registration = member.registration
            sheet.memberId = member.id
            sheet.save()

    def my_mark_sheet(self):
        search_fields = ["roll", "technology", "session", "name", "registration"]
        member = self.member_service.get_logged_in_member()
        self.adjust_mark_sheet_mapping(member)
        query = AcademicSeba.query.filter(and_(AcademicSeba.dataGroup == DataGroupEnum.Sheet.value, AcademicSeba.memberId == member.id))
        return self.form_crud_helper.form_paginated_list("member/mark-sheet", search_fields=search_fields, query=query)

    def my_certificate(self):
        search_fields = ["roll", "technology", "session", "name", "registration"]
        member = self.member_service.get_logged_in_member()
        self.adjust_mark_sheet_mapping(member)
        query = AcademicSeba.query.filter(and_(AcademicSeba.dataGroup == DataGroupEnum.Certificate.value, AcademicSeba.memberId == member.id))
        return self.form_crud_helper.form_paginated_list("member/certificate", search_fields=search_fields, query=query)

    def get_service_by_id(self, id):
        return AcademicSeba.query.filter(and_(AcademicSeba.id == id)).first()

    def send_receive_request(self, model_id, redirect_url="member_controller.mark_sheet"):
        model = self.get_service_by_id(model_id)
        if not model or model.status != MarkSheetStatus.NotReceived.value:
            flash(f"Invalid request", "error")
            return redirect(url_for(redirect_url))
        model.status = MarkSheetStatus.ReceivedRequest.value
        model.requestDate = datetime.now()
        model.save()
        flash(f"Success fully send request", "success")
        return redirect(url_for(redirect_url))

    def receive_request(self):
        search_fields = ["roll", "technology", "session", "name", "registration"]
        query = AcademicSeba.query.filter(or_(AcademicSeba.status == MarkSheetStatus.ReceivedRequest.value, AcademicSeba.status == MarkSheetStatus.Processing.value))
        return self.form_crud_helper.form_paginated_list("register/receive-request", search_fields=search_fields, query=query)

    def process_request(self, model_id):
        form = ProcessRequestForm()
        params = {"model_id": model_id}
        service = self.get_service_by_id(model_id)
        if not service:
            flash(f"Invalid request", "error")
            return redirect(url_for("register_controller.receive_request"))

        params["model"] = service
        if form.is_post_request() and form.is_valid_data():
            if not service.token:
                service.token = PyCommon.get_random_6digit()
            service.status = MarkSheetStatus.Processing.value
            model = self.form_crud_helper.update(form_def=form, existing_model=service)
            flash(f"Successfully Processed", "success")
            return redirect(url_for("register_controller.receive_request"))
        else:
            form.set_dict_value(form.dump(service))
        return self.form_crud_helper.template_helper.render("register/process-request", params=params, form=form)

    def resolve_request(self, model_id):
        form = ResolveRequestForm()
        params = {"model_id": model_id}
        service = self.get_service_by_id(model_id)
        if not service:
            flash(f"Invalid request", "error")
            return redirect(url_for("register_controller.receive_request"))

        params["model"] = service
        if form.is_post_request() and form.is_valid_data():
            if not service.token:
                service.token = PyCommon.get_random_6digit()
            service.status = MarkSheetStatus.Processing.value
            model = self.form_crud_helper.update(form_def=form, existing_model=service)
            flash(f"Successfully Processed", "success")
            return redirect(url_for("register_controller.receive_request"))
        else:
            form.set_dict_value(form.dump(service))
        return self.form_crud_helper.template_helper.render("register/process-request", params=params, form=form)
