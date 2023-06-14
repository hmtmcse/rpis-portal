from marshmallow import fields
from kpi_reunion.model.member import Member
from pf_flask_rest.form.pf_app_form_def import FormAppDef


class PaymentVerifyForm(FormAppDef):
    class Meta:
        model = Member
        load_instance = True

    paymentReference = fields.String(required=True, error_messages={"required": "Please enter payment reference"}, type="textarea")
    paid = fields.Float(required=True, error_messages={"required": "Please enter amount"}, type="number")
    id = fields.Integer(required=True, error_messages={"required": "Please enter id"}, type="hidden", isIgnoreLabel=True)

    paymentVerifiedById = fields.Integer(allow_none=None)
    paymentStatus = fields.String(allow_none=None)
    due = fields.Float(allow_none=None)
