from rpi_portal.common.rpi_auth_util import RPIAuthUtil


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
        navigation_list.append(NavigationData.get_nav_item("member_controller.profile", "Profile", "fa-brands fa-canadian-maple-leaf"))
        navigation_list.append(NavigationData.get_nav_item("member_controller.support", "Support", "fa-solid fa-headset"))

        if RPIAuthUtil.is_admin():
            pass

        return navigation_list
