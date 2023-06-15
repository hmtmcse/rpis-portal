from bdash.bdash_registry import BDashRegistry
from pf_flask_web.system12.pweb_interfaces import PWebRegisterModule
from region.region_registry import RegionRegistry
from rpi_portal.rpi_portal_registry import RPIPortalRegistry


class Register(PWebRegisterModule):

    def get_module_list(self) -> list:
        return [
            RPIPortalRegistry,
            BDashRegistry,
            RegionRegistry,
        ]
