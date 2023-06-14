import csv
from io import StringIO
from flask import Blueprint, redirect, url_for, make_response
from kpi_reunion.common.kpir_auth_util import KPIRAuthUtil
from kpi_reunion.service.report_service import ReportService

url_prefix = "/report"
report_controller = Blueprint(
    "report_controller",
    __name__,
    url_prefix=url_prefix
)

report_service = ReportService()


@report_controller.route("/", methods=['GET'])
def report():
    return report_service.get_report()


@report_controller.route("/lottery", methods=['GET'])
def lottery():
    return report_service.get_lottery()


@report_controller.route("/download", methods=['GET'])
def download():
    header, row = report_service.download_registration_report()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(header)
    cw.writerows(row)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=booking-report.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@report_controller.before_request
def check_member_role():
    if not KPIRAuthUtil.is_admin() and not KPIRAuthUtil.is_manager():
        return redirect(url_for("member_controller.dashboard"))
