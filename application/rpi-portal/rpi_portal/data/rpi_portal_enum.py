from pf_flask_rest_com.common.pffrc_enum_helper import BaseEnum


class MemberTypeEnum(BaseEnum):
    Admin = "Admin"
    Student = "Student"
    Register = "Register"
    RegisterAssistant = "RegisterAssistant"


class Technology(BaseEnum):
    Construction = "Construction"
    Electronics = "Electronics"
    Computer = "Computer"
    AIDT = "AIDT"
    Electrical = "Electrical"
    Mechanical = "Mechanical"
    Civil = "Civil"


class Shift(BaseEnum):
    First = "First"
    Second = "Second"


class BloodGroup(BaseEnum):
    O_Positive = "O+"
    O_Negative = "O-"
    A_Positive = "A+"
    A_Negative = "A-"
    B_Positive = "B+"
    B_Negative = "B-"
    AB_Positive = "AB+"
    AB_Negative = "AB-"


class MemberStatus(BaseEnum):
    Pending = "Pending"
    Approved = "Approved"
