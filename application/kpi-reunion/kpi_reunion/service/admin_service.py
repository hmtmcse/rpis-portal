from flask import url_for, flash, redirect
from kpi_reunion.common.template_processor import TemplateProcessor
from kpi_reunion.dto.event_form import PaymentVerifyForm
from kpi_reunion.model.event_registration import EventRegistration
from pf_flask_auth.common.pffa_auth_util import AuthUtil
from pf_flask_auth.data.pffa_form_auth_data import FormAuthData
from pf_flask_rest.helper.pf_flask_form_crud_helper import FormCRUDHelper
from pf_py_common.py_data_util import PyDataUtil


class AdminService:
    event_crud_helper = FormCRUDHelper(EventRegistration, template_helper=TemplateProcessor())

    def event_list(self):
        search_fields = ["memberId", "eventId", "paymentStatus", "paymentReference", "paid", "total", "due", "referenceCode"]
        return self.event_crud_helper.form_paginated_list("admin/event-list", search_fields=search_fields)

    def event_details(self, model_id):
        return self.event_crud_helper.form_details("admin/event-details", model_id, url_for("admin_controller.event_list"))

    def event_verify_payment(self, model_id):
        form = PaymentVerifyForm()
        data = None
        params = {"action": url_for("admin_controller.event_verify_payment", id=model_id)}
        redirect_url = url_for("admin_controller.event_list")
        form_model = self.event_crud_helper.details(model_id=model_id)
        if not form_model:
            flash('Invalid data', 'error')
            if redirect_url:
                return redirect(redirect_url)

        if form_model and form_model.paymentStatus == "Paid":
            flash("Already Paid. You are not allowed to edit.", "error")
            return redirect(redirect_url)

        if form.is_post_request() and form.is_valid_data():
            data = form.get_requested_data()
            payment_reference = PyDataUtil.get_dict_value(data, "paymentReference")

            if not payment_reference or str(payment_reference).count(f"Ref {form_model.referenceCode}") < 1:
                flash("Reference number not found", "error")
                return redirect(redirect_url)

            form_auth_data: FormAuthData = AuthUtil.get_ssr_auth_data()
            data["paymentVerifiedById"] = form_auth_data.id
            paid_amount = form_model.paid if form_model.paid else 0
            get_paid_amount = PyDataUtil.get_dict_value(data, "paid")
            data["paid"] = paid_amount = float(str(get_paid_amount)) + paid_amount
            if form_model.total <= paid_amount:
                data["paymentStatus"] = "Paid"
                data["due"] = 0
            else:
                data["paymentStatus"] = "Unpaid"
                data["due"] = form_model.total - paid_amount
            model = self.event_crud_helper.update(form_def=form, existing_model=form_model, data=data)
            if model:
                flash("Successfully updated", "success")
                return redirect(redirect_url)

        elif form.is_get_request():
            form.set_model_value(form_model)
            params["model"] = form_model
        return self.event_crud_helper.template_helper.render("admin/event-verify-payment", form=form, params=params)
