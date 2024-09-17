import axios from "axios";
import { getAccessToken } from './authHelper';

export class HttpAxiosService {
  axiosInstance;
  axiosMuliPartInstance;

  constructor(baseURL) {
    this.baseURL = baseURL;
    this.createAxiosInstances();
  }

  createAxiosInstances() {
    this.axiosInstance = axios.create({
      baseURL: this.baseURL,
      withCredentials: true,
      xsrfHeaderName: 'X-CSRFToken',
      xsrfCookieName: 'csrftoken',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });

    this.axiosMuliPartInstance = axios.create({
      baseURL: this.baseURL,
      withCredentials: true,
      xsrfHeaderName: 'X-CSRFToken',
      xsrfCookieName: 'csrftoken',
      headers: {
        'Content-Type': 'multipart/form-data',
        'Accept': 'application/json',
      },
    });

    // Add request interceptor for handling the token asynchronously
    this.axiosInstance.interceptors.request.use(async (config) => {
      const token = await getAccessToken(); // Get the token asynchronously
      if (token) {
        config.headers['Authorization'] = 'Bearer ' + token; // Add token to the Authorization header
      }
      return config;
    }, (error) => {
      return Promise.reject(error);
    });

    // Add request interceptor for the multipart instance as well
    this.axiosMuliPartInstance.interceptors.request.use(async (config) => {
      const token = await getAccessToken(); // Get the token asynchronously
      if (token) {
        config.headers['Authorization'] = 'Bearer ' + token; // Add token to the Authorization header
      }
      return config;
    }, (error) => {
      return Promise.reject(error);
    });
  }

  get(url, params) {
    return {
      axiosInstance: this.axiosInstance,
      method: "get",
      url: url,
      requestConfig: {
        params: params,
      },
    };
  }

  fileDownload(url, params) {
    return {
      axiosInstance: this.axiosInstance,
      method: "get",
      url: url,
      requestConfig:  {params, responseType: "blob" },
    };
  }

  post(url, data) {
    return {
      axiosInstance: this.axiosInstance,
      method: "post",
      url: url,
      requestConfig: data
    };
  }

  multiPartFormData(url, data) {
    return {
      axiosInstance: this.axiosMuliPartInstance,
      method: "post",
      url: url,
      requestConfig: data
    };
  }
}
