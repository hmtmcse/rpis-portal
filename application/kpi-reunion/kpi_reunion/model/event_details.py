import json
from sqlalchemy.dialects.mysql import LONGTEXT
from pf_flask_web.system12.pweb_db import pweb_db
from pf_flask_db.pf_app_model import AppModel


class EventDetails(AppModel):
    name = pweb_db.Column("name", pweb_db.String(150), nullable=False)
    content = pweb_db.Column("content", pweb_db.String(1000))
    adultFee = pweb_db.Column("adult_fee", pweb_db.Float(), nullable=False)
    childFee = pweb_db.Column("child_fee", pweb_db.Float())
    isDefault = pweb_db.Column("is_default", pweb_db.Boolean(), default=True)

    eventDate = pweb_db.Column("event_date", pweb_db.DateTime())
    registrationLastDate = pweb_db.Column("registration_last_date", pweb_db.DateTime())

    configJson = pweb_db.Column("config_json", pweb_db.Text().with_variant(LONGTEXT, "mysql"))

    @property
    def config(self):
        if self.configJson and isinstance(self.configJson, str):
            return json.loads(self.configJson)
        return {}

    @config.setter
    def config(self, dataDict: dict):
        self.configJson = json.dumps(dataDict)



