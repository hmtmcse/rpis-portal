import json
from sqlalchemy import Integer
from sqlalchemy.dialects.mysql import LONGTEXT
from pf_flask_web.system12.pweb_db import pweb_db
from pf_flask_db.pf_app_model import AppModel


class EventRegistration(AppModel):
    eventId = pweb_db.Column("event_id", pweb_db.BigInteger().with_variant(Integer, "sqlite"), pweb_db.ForeignKey('event_details.id'), nullable=False)
    memberId = pweb_db.Column("member_Id", pweb_db.BigInteger().with_variant(Integer, "sqlite"), pweb_db.ForeignKey('member.id'), nullable=False)

    updateById = pweb_db.Column("update_by_id", pweb_db.BigInteger().with_variant(Integer, "sqlite"), pweb_db.ForeignKey('member.id'))

    paymentVerifiedById = pweb_db.Column("payment_verified_by_id", pweb_db.BigInteger().with_variant(Integer, "sqlite"), pweb_db.ForeignKey('member.id'))
    paymentReference = pweb_db.Column("payment_reference", pweb_db.String(1000))
    paymentStatus = pweb_db.Column("payment_status", pweb_db.String(30))

    referenceCode = pweb_db.Column("reference_code", pweb_db.String(20))

    due = pweb_db.Column("due", pweb_db.Float())
    paid = pweb_db.Column("paid", pweb_db.Float())
    total = pweb_db.Column("total", pweb_db.Float())

    adult = pweb_db.Column("adult", pweb_db.Integer(), nullable=False)
    child = pweb_db.Column("child", pweb_db.Integer())

    adultTotal = pweb_db.Column("adult_total", pweb_db.Float(), nullable=False)
    childTotal = pweb_db.Column("child_total", pweb_db.Float())
    configJson = pweb_db.Column("config_json", pweb_db.Text().with_variant(LONGTEXT, "mysql"))

    member = pweb_db.relationship(
        "Member",
        lazy="joined",
        remote_side="Member.id",
        primaryjoin="and_(EventRegistration.memberId==Member.id)", uselist=False)

    verifyMember = pweb_db.relationship(
        "Member",
        lazy="joined",
        remote_side="Member.id",
        primaryjoin="and_(EventRegistration.paymentVerifiedById==Member.id)", uselist=False)

    @property
    def config(self):
        if self.configJson and isinstance(self.configJson, str):
            return json.loads(self.configJson)
        return {}

    @config.setter
    def config(self, dataDict: dict):
        self.configJson = json.dumps(dataDict)

