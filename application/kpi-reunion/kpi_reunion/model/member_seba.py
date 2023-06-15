import json
from sqlalchemy.dialects.mysql import LONGTEXT
from kpi_reunion.data.kpi_reunio_enum import MemberTypeEnum
from pf_flask_auth.model.pffa_abstract_model import OperatorAbstract
from pf_flask_db.pf_app_model import AppModel
from pf_flask_web.system12.pweb_db import pweb_db


class MemberSeba(AppModel):
    roll = pweb_db.Column("roll", pweb_db.String(20))
    technology = pweb_db.Column("technology", pweb_db.String(50))
    session = pweb_db.Column("session", pweb_db.String(50))
    shift = pweb_db.Column("shift", pweb_db.String(50))
    semester = pweb_db.Column("semester", pweb_db.String(50))
    registration = pweb_db.Column("registration", pweb_db.String(30))

    name = pweb_db.Column("name", pweb_db.String(30), nullable=False)
    status = pweb_db.Column("status", pweb_db.String(15), nullable=False)
    paymentStatus = pweb_db.Column("paymentStatus", pweb_db.String(15))

    identifier = pweb_db.Column("identifier", pweb_db.String(50))
    prove = pweb_db.Column("prove", pweb_db.String(250))

    response = pweb_db.Column("response", pweb_db.String(500))
    token = pweb_db.Column("token", pweb_db.String(20))

    charge = pweb_db.Column("charge", pweb_db.Float())
    paid = pweb_db.Column("paid", pweb_db.Float())

    description = pweb_db.Column("roll", pweb_db.String(1000))

    resolveDate = pweb_db.Column("resolve_date", pweb_db.DateTime)

    additionalDataJson = pweb_db.Column("additional_data_json", pweb_db.Text().with_variant(LONGTEXT, "mysql"))

    @property
    def additionalData(self):
        if self.additionalDataJson and isinstance(self.additionalDataJson, str):
            return json.loads(self.additionalDataJson)
        return {}

    @additionalData.setter
    def additionalData(self, dataDict: dict):
        self.additionalDataJson = json.dumps(dataDict)
