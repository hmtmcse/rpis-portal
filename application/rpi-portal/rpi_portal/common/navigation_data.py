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

        if RPIAuthUtil.is_student():
            navigation_list.append(NavigationData.get_nav_item("member_controller.mark_sheet", "My Mark Sheet", "fa-solid fa-file-lines"))
            navigation_list.append(NavigationData.get_nav_item("member_controller.certificate", "My Certificate", "fa-solid fa-certificate"))
            navigation_list.append(NavigationData.get_nav_item("member_controller.protoyon_potro", "প্রত্যয়ন পত্র","fa-solid fa-file"))

        if RPIAuthUtil.is_admin():
            navigation_list.append(NavigationData.get_nav_item("admin_controller.student_list", "Student", "fa-solid fa-rectangle-list"))
            navigation_list.append(NavigationData.get_nav_item("admin_controller.operator_list", "Operator", "fa-solid fa-rectangle-list"))

        if RPIAuthUtil.is_register():
            navigation_list.append(NavigationData.get_nav_item("register_controller.registration_approval", "Registration", "fa-solid fa-rectangle-list"))
            navigation_list.append(NavigationData.get_nav_item("register_controller.registration_approval", "প্রত্যয়ন পত্র", "fa-solid fa-rectangle-list"))
            navigation_list.append(NavigationData.get_nav_item("register_controller.mark_sheet", "Mark Sheet", "fa-solid fa-rectangle-list"))
            navigation_list.append(NavigationData.get_nav_item("register_controller.registration_approval", "Certificate", "fa-solid fa-rectangle-list"))

        navigation_list.append(NavigationData.get_nav_item("member_controller.profile", "Profile", "fa-brands fa-canadian-maple-leaf"))
        navigation_list.append(NavigationData.get_nav_item("member_controller.support", "Support", "fa-solid fa-headset"))

        return navigation_list
