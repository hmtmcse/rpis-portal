from pf_flask_rest_com.common.pffrc_enum_helper import BaseEnum


class MemberTypeEnum(BaseEnum):
    Admin = "Admin"
    Student = "Student"
    Register = "Register"
    Department = "Department"
    Principle = "Principle"
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
    ReceivedRequest = "Received Request"
    PaymentPending = "Payment Pending"
    Processing = "Processing"
    PrincipleApproved = "Principle Approved"
    NotFound = "NotFound"


class DataGroupEnum(BaseEnum):
    Attestation = "Attestation"
    Sheet = "Sheet"
    Certificate = "Certificate"
