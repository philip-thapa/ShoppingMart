class GenderConstants:

    MALE = 'MALE'
    FEMALE = 'FEMALE'
    NA = 'N/A'

    ALL = [MALE, FEMALE, NA]


class AUTHENTICATION_MSG:

    ACTIVATE_ACCOUNT_HEADER = 'Activate account'

    ACTIVATE_ACCOUNT_BODY = 'Please use this OTP to activate your account'

    SIGN_IN_HEADER = 'MART Sign In'

    SIGN_IN_BODY = 'Please use this otp to login'


class ERROR_MSG:

    INVALID_OTP = 'Invalid OTP'

    USER_DOESNOT_EXIST = 'User doesnot exists'

    INVALID_CREDENTIALS = 'Invalid Credentails'

    USER_ALREADY_EXIST = 'User already exist'


class ADDRESS_CONSTANTS:

    ADDRESS_TYPES = ["Home", "work", "Other"]