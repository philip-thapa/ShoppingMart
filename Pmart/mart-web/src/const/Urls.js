export class Urls {
    static API_PREFIX = '/api';

    static SEND_SIGN_UP_OTP = Urls.API_PREFIX +'/user/send-signup-otp';
    static SIGN_UP = Urls.API_PREFIX + '/user/sign-up';
    static SEND_SIGN_IN_OTP = Urls.API_PREFIX + '/user/send-signin-otp';
    static SIGN_IN = Urls.API_PREFIX + '/user/sign-in';
    static VERIFY_OTP = Urls.API_PREFIX + '/user/verify-otp';

    static GET_USER_DETAILS = Urls.API_PREFIX + '/user/get-user-details';
}