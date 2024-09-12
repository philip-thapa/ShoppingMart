export const storeToken = (accessToken, refreshToken) => {
    localStorage.setItem('token', accessToken);
    localStorage.setItem('refesh', refreshToken);
}

export const clearToken = () => {
    if (localStorage.getItem('token')){
        localStorage.removeItem('token');
    }
    if (localStorage.getItem('refresh')){
        localStorage.removeItem('refresh');
    }
}

export const getToken = () => {
    if (localStorage.getItem('token')){
        return localStorage.getItem('token');
    }
    return null;
}