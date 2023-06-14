import calendar
import json
from datetime import datetime

from sqlalchemy import func, and_

from kpi_reunion.common.template_processor import TemplateProcessor
from kpi_reunion.model.event_registration import EventRegistration
from kpi_reunion.model.member import Member
from pf_flask_rest.helper.pf_flask_form_crud_helper import FormCRUDHelper


class ReportService:
    event_crud_helper = FormCRUDHelper(EventRegistration, template_helper=TemplateProcessor())

    def get_report(self):
        member_report = self.get_member_report()
        booking_report = self.get_booking_report()
        collection_report = self.get_collection_report()
        all_report = self.get_all_report()
        data = {"all_report": all_report}
        data.update(member_report)
        data.update(booking_report)
        data.update(collection_report)
        return self.event_crud_helper.template_helper.render("report/report", params={"data": data})

    def _get_today_first(self):
        current_month_int = datetime.now().month
        current_day_int = datetime.now().day
        current_month = "{:02d}".format(current_month_int)
        current_year = datetime.now().year
        start_date_time = datetime.strptime(f"{current_day_int}-{current_month}-{current_year} 00:00:00", '%d-%m-%Y %H:%M:%S')
        return start_date_time

    def get_member_report(self):
        start_date_time = self._get_today_first()
        today_registration = Member.query.filter(Member.created > start_date_time).count()
        total_registration = Member.query.count()
        return {"todayRegistration": today_registration, "totalRegistration": total_registration}

    def get_booking_report(self):
        start_date_time = self._get_today_first()
        today_registration = EventRegistration.query.filter(EventRegistration.created > start_date_time).count()
        total_registration = EventRegistration.query.count()
        return {"todayBooking": today_registration, "totalBooking": total_registration}

    def get_collection_report(self):
        start_date_time = self._get_today_first()
        today_paid = EventRegistration.query.with_entities(func.sum(EventRegistration.paid)).filter(EventRegistration.created > start_date_time).first()
        if today_paid:
            today_paid = today_paid[0]

        total_paid = EventRegistration.query.with_entities(func.sum(EventRegistration.paid)).first()
        if total_paid:
            total_paid = total_paid[0]
        return {"todayPaid": today_paid, "totalPaid": total_paid}

    def download_registration_report(self):
        event_data = Member.query.join(EventRegistration, EventRegistration.memberId == Member.id).add_columns(
            Member.name,
            Member.mobile,
            Member.technology,
            Member.session,
            Member.shift,
            Member.passingYear,
            Member.homeDistrict,
            EventRegistration.paid,
            EventRegistration.referenceCode,
            EventRegistration.adult,
            EventRegistration.paymentStatus,
        ).filter(and_(
            EventRegistration.paid != None)).order_by(Member.technology).all()
        header = ["Name", "Mobile", "Technology", "Session", "Shift", "Pass", "Home", "Paid", "Code", "Sit", "Status"]
        row = []
        for data in event_data:
            row.append(
                [data.name, data.mobile, data.technology, data.session, data.shift, data.passingYear, data.homeDistrict, data.paid, data.referenceCode, data.adult, data.paymentStatus]
            )
        return header, row

    def get_all_report(self):
        event_data = EventRegistration.query.all()
        report = {
            "totalParticipant": 0,
            "totalGuest": 0,
            "totalAlumni": 0,
            "M": 0,
            "L": 0,
            "XL": 0,
            "XXL": 0
        }
        if not event_data:
            return report
        for registration in event_data:
            member = registration.member
            if member.technology and registration.paid:
                if member.technology not in report:
                    report[member.technology] = {
                        "booking": 0,
                        "paid": 0,
                        "totalPaid": 0,
                        "participant": 0,
                        "withGuest": 0,
                    }
                report[member.technology]["booking"] += 1
                report[member.technology]["participant"] += registration.adult

                if registration.adult > 1:
                    guest = registration.adult - 1
                    report["totalGuest"] += guest
                    report["totalAlumni"] += 1
                    report[member.technology]["withGuest"] += guest
                else:
                    report["totalAlumni"] += 1

                if registration.paid:
                    report[member.technology]["paid"] += 1
                    report["totalParticipant"] += registration.adult
                    report[member.technology]["totalPaid"] += registration.paid

                config = {}
                if registration.configJson and isinstance(registration.configJson, str):
                    config = json.loads(registration.configJson)

                if config and "tshirt" in config:
                    tshirt = config["tshirt"]
                    for size in tshirt.values():
                        if size in report:
                            report[size] += 1

        return report

    def get_lottery(self):
        header, row = self.download_registration_report()
        table_row = []
        table_data = []
        loop = 0
        for data in row:
            table_data.append(data[8])
            loop += 1
            if loop == 6:
                table_row.append(table_data)
                table_data = []
                loop = 0
        table_row.append(table_data)

        return self.event_crud_helper.template_helper.render("report/lottery", params={"data": table_row})
