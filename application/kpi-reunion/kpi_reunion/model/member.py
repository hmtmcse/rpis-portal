import json
from sqlalchemy.dialects.mysql import LONGTEXT
from kpi_reunion.data.kpi_reunio_enum import MemberTypeEnum
from pf_flask_auth.model.pffa_abstract_model import OperatorAbstract
from pf_flask_web.system12.pweb_db import pweb_db


class Member(OperatorAbstract):
    accessType = pweb_db.Column("access_type", pweb_db.String(100), default=MemberTypeEnum.Member.value, nullable=False)
    mobile = pweb_db.Column("mobile", pweb_db.String(30))
    emergencyContact = pweb_db.Column("emergency_contact", pweb_db.String(50))
    technology = pweb_db.Column("technology", pweb_db.String(50))
    session = pweb_db.Column("session", pweb_db.String(50))
    shift = pweb_db.Column("shift", pweb_db.String(50))
    passingYear = pweb_db.Column("passing_year", pweb_db.String(50))
    homeDistrict = pweb_db.Column("home_district", pweb_db.String(50))
    bloodGroup = pweb_db.Column("blood_group", pweb_db.String(50))

    isKnown = pweb_db.Column("is_known", pweb_db.Boolean, default=False)

    presentAddress = pweb_db.Column("present_address", pweb_db.Text().with_variant(LONGTEXT, "mysql"))
    permanentAddress = pweb_db.Column("permanent_address", pweb_db.Text().with_variant(LONGTEXT, "mysql"))
    jobDetails = pweb_db.Column("job_details", pweb_db.Text().with_variant(LONGTEXT, "mysql"))
    jobAddress = pweb_db.Column("job_address", pweb_db.Text().with_variant(LONGTEXT, "mysql"))

    additionalDataJson = pweb_db.Column("additional_data_json", pweb_db.Text().with_variant(LONGTEXT, "mysql"))

    @property
    def additionalData(self):
        if self.additionalDataJson and isinstance(self.additionalDataJson, str):
            return json.loads(self.additionalDataJson)
        return {}

    @additionalData.setter
    def additionalData(self, dataDict: dict):
        self.additionalDataJson = json.dumps(dataDict)
