import { BASE_URL } from "../../../config/environment.config";
import { Urls } from "../../../const/Urls";
import { HttpAxiosService } from "../../../HttpAxiosService";


const authService = new HttpAxiosService(BASE_URL);

export const signInService = (payload) => {
    return authService.post(Urls.SIGN_IN, payload);
};

export const sendSignInOtpService = (payload) => {
    return authService.post(Urls.SEND_SIGN_IN_OTP, payload);
}
