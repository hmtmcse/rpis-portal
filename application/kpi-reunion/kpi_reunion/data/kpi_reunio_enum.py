from pf_flask_rest_com.common.pffrc_enum_helper import BaseEnum


class MemberTypeEnum(BaseEnum):
    Admin = "Admin"
    Manager = "Manager"
    Member = "Member"
    Volunteer = "Volunteer"


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


class SessionEnum(BaseEnum):
    S_2005_2006 = "2005-2006"
    S_2006_2007 = "2006-2007"
    S_2007_2008 = "2007-2008"
    S_2008_2009 = "2008-2009"
    S_2009_2010 = "2009-2010"
    S_2010_2011 = "2010-2011"
    S_2011_2012 = "2011-2012"
    S_2012_2013 = "2012-2013"
    S_2013_2014 = "2013-2014"
    S_2014_2015 = "2014-2015"
    S_2015_2016 = "2015-2016"
    S_2016_2017 = "2016-2017"
    S_2017_2018 = "2017-2018"
    S_2018_2019 = "2018-2019"
    S_2019_2020 = "2019-2020"


class PassingYear(BaseEnum):
    S_2009 = "2009"
    S_2010 = "2010"
    S_2011 = "2011"
    S_2012 = "2012"
    S_2013 = "2013"
    S_2014 = "2014"
    S_2015 = "2015"
    S_2016 = "2016"
    S_2017 = "2017"
    S_2018 = "2018"
    S_2019 = "2019"
    S_2020 = "2020"
    S_2021 = "2021"
    S_2022 = "2022"


class BloodGroup(BaseEnum):
    O_Positive = "O+"
    O_Negative = "O-"
    A_Positive = "A+"
    A_Negative = "A-"
    B_Positive = "B+"
    B_Negative = "B-"
    AB_Positive = "AB+"
    AB_Negative = "AB-"
