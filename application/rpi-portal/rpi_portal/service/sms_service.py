from sqlalchemy import and_
from rpi_portal.common.greenweb_sms import GreenWebSMS
from rpi_portal.data.rpi_portal_enum import MemberTypeEnum
from rpi_portal.model.member import Member


class SMSService:

    def send_registration_request(self, member):
        return
        register = Member.query.filter(and_(Member.isDeleted == False, Member.accessType == MemberTypeEnum.Register.value)).order_by(Member.id.desc()).first()
        if register and register.mobile:
            message = f"RPIR \nNew Registration Request.\nRoll: {member.roll}\nTech: {member.technology}\nMob: {member.mobile}"
            GreenWebSMS.send_sms(register.mobile, message=message)

    def send_registration_approve(self, member):
        return
        message = f"Rangpur Polytechnic Institute\nYour Registration has been Approved."
        GreenWebSMS.send_sms(member.mobile, message=message)
