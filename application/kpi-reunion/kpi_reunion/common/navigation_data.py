from kpi_reunion.common.kpir_auth_util import KPIRAuthUtil


class NavigationData:

    @staticmethod
    def get_nav_item(url, name, icon):
        return {
            "url": url,
            "name": name,
            "icon": icon,
        }

    @staticmethod
    def get_left_nav():
        navigation_list = []
        navigation_list.append(NavigationData.get_nav_item("member_controller.dashboard", "Dashboard", "fas fa-chart-pie"))
        navigation_list.append(NavigationData.get_nav_item("member_controller.my_event", "My Event", "fa-regular fa-calendar-check"))
        navigation_list.append(NavigationData.get_nav_item("member_controller.profile", "Profile", "fa-brands fa-canadian-maple-leaf"))
        navigation_list.append(NavigationData.get_nav_item("member_controller.my_invitation", "Invitation", "fa-solid fa-envelopes-bulk"))
        navigation_list.append(NavigationData.get_nav_item("member_controller.support", "Support", "fa-solid fa-headset"))

        if KPIRAuthUtil.is_admin() or KPIRAuthUtil.is_manager():
            navigation_list.append(NavigationData.get_nav_item("report_controller.report", "Report", "fa-solid fa-receipt"))
            navigation_list.append(NavigationData.get_nav_item("volunteer_controller.scan", "Scan", "fa-solid fa-qrcode"))

        if KPIRAuthUtil.is_volunteer():
            navigation_list.append(NavigationData.get_nav_item("volunteer_controller.scan", "Scan", "fa-solid fa-qrcode"))

        if KPIRAuthUtil.is_admin():
            navigation_list.append(NavigationData.get_nav_item("admin_controller.member_list", "Members", "fa-solid fa-envelopes-bulk"))
            navigation_list.append(NavigationData.get_nav_item("admin_controller.event_list", "Event Registration", "fa-solid fa-envelopes-bulk"))
        return navigation_list
