from bdash.bdash_registry import BDashRegistry
from kpi_reunion.kpi_reunion_registry import KpiReunionRegistry
from pf_flask_web.system12.pweb_interfaces import PWebRegisterModule
from region.region_registry import RegionRegistry


class Register(PWebRegisterModule):

    def get_module_list(self) -> list:
        return [
            KpiReunionRegistry,
            BDashRegistry,
            RegionRegistry,
        ]
