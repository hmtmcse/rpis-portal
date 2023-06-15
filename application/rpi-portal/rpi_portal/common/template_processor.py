from pf_flask_rest.form.pf_app_form_def import FormBaseDef
from pf_flask_rest.helper.pf_flask_template_helper import TemplateHelper
from rpi_portal.common.navigation_data import NavigationData
from rpi_portal.template.template_util import TemplateUtil


class Helper:

    def pending(self, expected, actual, default=0):
        if expected is None or actual is None:
            return default
        if actual > expected:
            return default
        return expected - actual


class TemplateProcessor(TemplateHelper):

    def render(self, name, params={}, form: FormBaseDef = None):
        system = {
            "left_nav": NavigationData.get_left_nav(),
            "helper": Helper(),
            "tutil": TemplateUtil()
        }
        params.update(system)
        return super().render(name, params, form=form)


def render(name, params={}, form: FormBaseDef = None):
    template = TemplateProcessor()
    return template.render(name, params, form)
