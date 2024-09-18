import { createSlice } from "@reduxjs/toolkit";
import { getAccessToken } from "../authHelper";

const initialState = {
    isLoggedIn: false,
    userDetails: null
}

export const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        login: (state, action) => {
            state.isLoggedIn = action.payload;
        },

        logout: (state, action) => {
            state.isLoggedIn = false;
            state.userDetails = null;
        },

        setUserDetails: (state, action) => {
            state.userDetails = action.payload;
        }
    }
})

export const {login, logout, setUserDetails} = authSlice.actions

export const checkAuthStatus = () => async (dispatch) => {
    const token = await getAccessToken();
    dispatch(login(!!token));
  };

export default authSlice.reducer