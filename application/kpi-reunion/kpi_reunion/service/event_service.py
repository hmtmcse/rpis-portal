from flask import redirect, url_for, flash
from sqlalchemy import and_
from kpi_reunion.common.template_processor import TemplateProcessor
from kpi_reunion.dto.member_form import EventRegistrationForm
from kpi_reunion.model.event_details import EventDetails
from kpi_reunion.model.event_registration import EventRegistration
from kpi_reunion.model.member import Member
from pf_flask_auth.common.pffa_auth_util import AuthUtil
from pf_flask_auth.common.pffa_session_man import SessionMan
from pf_flask_auth.data.pffa_form_auth_data import FormAuthData
from pf_flask_rest.helper.pf_flask_form_crud_helper import FormCRUDHelper
from pf_flask_rest.pf_flask_request_processor import RequestProcessor
from pf_py_common.py_common import PyCommon
from pf_py_common.py_data_util import PyDataUtil


class EventService:
    EVENT_SESSION = "EVENT_SESSION"
    form_crud_helper = FormCRUDHelper(Member, template_helper=TemplateProcessor())
    request_processor = RequestProcessor()

    def get_default_event(self):
        return EventDetails.query.filter(and_(EventDetails.isDeleted == False, EventDetails.isDefault == True)).first()

    def save(self):
        pass

    def get_booking_session(self, event, adult=None, child=None):
        existing = SessionMan.get(self.EVENT_SESSION, {})
        if not existing:
            existing = {
                "eventId": event.id,
                "child": 0,
                "childAmount": 0,
                "childFee": event.childFee,
                "adultFee": event.adultFee,
                "adultAmount": 0,
                "adult": 0,
                "total": 0,
            }
        else:
            total_adult = existing["adult"]
            total_child = existing["child"]
            if child is None:
                child = total_child

            if adult is None:
                adult = total_adult

        if adult is not None:
            existing["adult"] = adult

        if child is not None:
            existing["child"] = child

        existing["childAmount"] = existing["child"] * existing["childFee"]
        existing["adultAmount"] = existing["adult"] * existing["adultFee"]
        existing["total"] = existing["childAmount"] + existing["adultAmount"]
        SessionMan.add(self.EVENT_SESSION, existing)
        return existing

    def event_booking_manage(self):
        return self.event_booking(wrapper=False)

    def set_shirt(self, event_data):
        adult = PyDataUtil.get_dict_value(event_data, "adult", default=0)
        child = PyDataUtil.get_dict_value(event_data, "child", default=0)

        tshirt = {}
        data = self.request_processor.request_helper.form_data()

        if adult:
            for i in range(1, adult + 1):
                name = f"adultShirt{i}"
                tshirt[name] = PyDataUtil.get_dict_value(data, name)

        if child:
            for i in range(1, child + 1):
                name = f"childShirt{i}"
                tshirt[name] = PyDataUtil.get_dict_value(data, name)

        event_data["tshirt"] = tshirt
        return event_data

    def get_reference_code(self, loop=0):
        code = PyCommon.get_random_6digit()
        model = EventRegistration.query.filter(EventRegistration.referenceCode == code).first()
        if model and loop < 5:
            code = self.get_reference_code(loop + 1)
        elif loop >= 5:
            code = f"f{code}{model.id}"
        return code

    def save_event(self, event_data):
        model_id = PyDataUtil.get_dict_value(event_data, "id")
        instance = None
        if model_id:
            instance = EventRegistration.query.filter(and_(EventRegistration.id == model_id)).first()

        if not instance:
            instance = EventRegistration()
            instance.eventId = PyDataUtil.get_dict_value(event_data, "eventId")
            form_auth_data: FormAuthData = AuthUtil.get_ssr_auth_data()
            instance.memberId = form_auth_data.id
            instance.updateById = form_auth_data.id
            instance.referenceCode = self.get_reference_code()

        instance.adult = PyDataUtil.get_dict_value(event_data, "adult")
        instance.child = PyDataUtil.get_dict_value(event_data, "child")
        instance.total = PyDataUtil.get_dict_value(event_data, "total")

        tshirt = PyDataUtil.get_dict_value(event_data, "tshirt")
        if tshirt:
            instance.config = {"tshirt": tshirt}

        instance.adultTotal = PyDataUtil.get_dict_value(event_data, "adultAmount")
        instance.childTotal = PyDataUtil.get_dict_value(event_data, "childAmount")
        instance.save()
        return instance

    def is_already_registered(self, event):
        form_auth_data: FormAuthData = AuthUtil.get_ssr_auth_data()
        registration = EventRegistration.query.filter(and_(EventRegistration.eventId == event.id, EventRegistration.memberId == form_auth_data.id)).first()
        return registration

    def get_my_event(self):
        event = self.get_default_event()
        return self.is_already_registered(event)

    def event_booking(self, wrapper=True):

        flash("Sorry currently registration is closed", "error")
        return redirect(url_for("site_controller.bismillah"))

        event = self.get_default_event()
        if not event:
            flash("Sorry there is no event available now", "error")
            return redirect(url_for("site_controller.bismillah"))

        if self.is_already_registered(event):
            flash("You have already registered the event", "success")
            return redirect(url_for("member_controller.my_event"))

        adult = self.request_processor.get_query_param("adult", exception=False, default=None, type=int)
        child = self.request_processor.get_query_param("child", exception=False, default=None, type=int)

        event_data = self.get_booking_session(event, adult=adult, child=child)

        form = EventRegistrationForm()
        if form.is_post_request():
            event_data = self.set_shirt(event_data)
            instance = self.save_event(event_data)
            if instance:
                flash("Successfully event registered", "success")
                return redirect(url_for("site_controller.payment_reference"))

        params = {"event": event_data, "wrapper": wrapper}
        return self.form_crud_helper.template_helper.render("site/event-booking", params=params)

    def scan(self):
        params = {}
        return self.form_crud_helper.template_helper.render("event/scan", params=params)

    def update_scan_item(self):
        id = self.request_processor.get_query_param("id", exception=False, default=None)
        key = self.request_processor.get_query_param("key", exception=False, default=None)
        quantity = self.request_processor.get_query_param("quantity", exception=False, default=None)
        instance = EventRegistration.query.filter(and_(EventRegistration.id == id, EventRegistration.paymentStatus == "Paid")).first()
        if not instance:
            return "Error"

        config = instance.config
        if "result" not in config:
            config["result"] = {}
        key_data = {
            "size": quantity,
            "status": "Done"
        }
        config["result"][key] = key_data
        instance.config = config
        instance.save()
        return "Done"

    def scan_details(self):
        params = {}
        uuid = self.request_processor.get_query_param("id", exception=False, default=None)
        instance = None
        member = None
        if uuid:
            member = Member.query.filter(and_(Member.uuid == uuid)).first()
            if member:
                instance = EventRegistration.query.filter(and_(EventRegistration.memberId == member.id, EventRegistration.paymentStatus == "Paid")).first()
        params["event"] = instance
        params["member"] = member
        result = {}
        tshirt = []
        if instance and instance.config:
            if "result" in instance.config:
                result = instance.config["result"]

            for data_key in instance.config:
                if data_key.startswith("tshirt"):
                    data = instance.config[data_key]
                    count = 0
                    for item_key in data:
                        count = count + 1
                        if item_key not in result:
                            key_data = {
                                "size": data[item_key],
                                "status": ""
                            }
                            result[item_key] = key_data
                        tshirt.append(item_key)

                    if "lunch" not in result:
                        key_data = {
                            "size": count,
                            "status": ""
                        }
                        result["lunch"] = key_data

                    if "cap_key" not in result:
                        key_data = {
                            "size": count,
                            "status": ""
                        }
                        result["cap_key"] = key_data

                    if "breakfast" not in result:
                        key_data = {
                            "size": count,
                            "status": ""
                        }
                        result["breakfast"] = key_data

            params["result"] = result
            params["tshirt"] = tshirt
        return self.form_crud_helper.template_helper.render("event/registration-details", params=params)
