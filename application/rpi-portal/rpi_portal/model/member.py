import json
from sqlalchemy.dialects.mysql import LONGTEXT
from pf_flask_auth.model.pffa_abstract_model import OperatorAbstract
from pf_flask_web.system12.pweb_db import pweb_db
from rpi_portal.data.rpi_portal_enum import MemberTypeEnum, MemberStatus


class Member(OperatorAbstract):
    accessType = pweb_db.Column("access_type", pweb_db.String(100), default=MemberTypeEnum.Student.value, nullable=False)
    mobile = pweb_db.Column("mobile", pweb_db.String(30))
    emergencyContact = pweb_db.Column("emergency_contact", pweb_db.String(50))
    technology = pweb_db.Column("technology", pweb_db.String(50))
    session = pweb_db.Column("session", pweb_db.String(50))
    shift = pweb_db.Column("shift", pweb_db.String(50))

    roll = pweb_db.Column("roll", pweb_db.String(20))
    registration = pweb_db.Column("registration", pweb_db.String(30))

    passingYear = pweb_db.Column("passing_year", pweb_db.String(10))
    homeDistrict = pweb_db.Column("home_district", pweb_db.String(50))
    bloodGroup = pweb_db.Column("blood_group", pweb_db.String(50))

    status = pweb_db.Column("status", pweb_db.String(15), default=MemberStatus.Pending.value)

    additionalDataJson = pweb_db.Column("additional_data_json", pweb_db.Text().with_variant(LONGTEXT, "mysql"))

    @property
    def additionalData(self):
        if self.additionalDataJson and isinstance(self.additionalDataJson, str):
            return json.loads(self.additionalDataJson)
        return {}

    @additionalData.setter
    def additionalData(self, dataDict: dict):
        self.additionalDataJson = json.dumps(dataDict)
