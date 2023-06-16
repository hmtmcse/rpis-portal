from pf_flask_rest_com.common.pffrc_enum_helper import BaseEnum


class MemberTypeEnum(BaseEnum):
    Admin = "Admin"
    Student = "Student"
    Register = "Register"
    RegisterAssistant = "RegisterAssistant"


class Technology(BaseEnum):
    Electrical = "Electrical"
    Electronics = "Electronics"
    Computer = "Computer"
    Mechanical = "Mechanical"
    Civil = "Civil"
    Power = "Power"
    ElectroMedical = "ElectroMedical"


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


class MarkSheetStatus(BaseEnum):
    NotReceived = "NotReceived"
    Received = "Received"
    Processing = "Processing"
    NotFound = "NotFound"


class DataGroupEnum(BaseEnum):
    Sheet = "Sheet"
    Certificate = "Certificate"
