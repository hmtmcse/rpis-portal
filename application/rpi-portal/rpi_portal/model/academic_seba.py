import json
from sqlalchemy import Integer
from sqlalchemy.dialects.mysql import LONGTEXT
from pf_flask_db.pf_app_model import AppModel
from pf_flask_web.system12.pweb_db import pweb_db


class AcademicSeba(AppModel):

    dataGroup = pweb_db.Column("data_group", pweb_db.String(10))
    roll = pweb_db.Column("roll", pweb_db.String(20))
    technology = pweb_db.Column("technology", pweb_db.String(50))
    session = pweb_db.Column("session", pweb_db.String(50))
    shift = pweb_db.Column("shift", pweb_db.String(50))
    semester = pweb_db.Column("semester", pweb_db.String(50))
    registration = pweb_db.Column("registration", pweb_db.String(30))

    name = pweb_db.Column("name", pweb_db.String(30), nullable=False)
    status = pweb_db.Column("status", pweb_db.String(15), nullable=False)

    identifier = pweb_db.Column("identifier", pweb_db.String(50))
    prove = pweb_db.Column("prove", pweb_db.String(250))

    response = pweb_db.Column("response", pweb_db.String(500))
    token = pweb_db.Column("token", pweb_db.String(20))

    charge = pweb_db.Column("charge", pweb_db.Float())
    paid = pweb_db.Column("paid", pweb_db.Float())

    description = pweb_db.Column("description", pweb_db.String(500))
    resolveDate = pweb_db.Column("resolve_date", pweb_db.DateTime)

    memberId = pweb_db.Column("member_Id", pweb_db.BigInteger().with_variant(Integer, "sqlite"), pweb_db.ForeignKey('member.id'))

    additionalDataJson = pweb_db.Column("additional_data_json", pweb_db.Text().with_variant(LONGTEXT, "mysql"))

    @property
    def additionalData(self):
        if self.additionalDataJson and isinstance(self.additionalDataJson, str):
            return json.loads(self.additionalDataJson)
        return {}

    @additionalData.setter
    def additionalData(self, dataDict: dict):
        self.additionalDataJson = json.dumps(dataDict)
