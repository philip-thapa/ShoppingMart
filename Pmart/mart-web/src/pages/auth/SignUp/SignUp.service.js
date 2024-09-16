import { BASE_URL } from "../../../config/environment.config";
import { Urls } from "../../../const/Urls";
import { HttpAxiosService } from "../../../HttpAxiosService";


const authService = new HttpAxiosService(BASE_URL);

export const sendSignUpOtpService = (payload) => {
    return authService.post(Urls.SEND_SIGN_UP_OTP, payload);
}

export const verifyOtpService = (payload) => {
    return authService.post(Urls.VERIFY_OTP, payload);
}

export const signUpService = (payload) => {
    return authService.post(Urls.SIGN_UP, payload);
}
