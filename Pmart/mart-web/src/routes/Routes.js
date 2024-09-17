// Routes.js
import React, {Suspense, useEffect} from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Loader from "../components/Loader";
import { useDispatch, useSelector } from "react-redux";
import useAxios from "../useAxios";
import { getUserDetailsService } from "../pages/auth/SignIn/Signin.service";
import { checkAuthStatus, setUserDetails } from "../redux/authSlice";


const SignInPage = React.lazy(() => import('../pages/auth/SignIn/Signin'));
const SignUpPage = React.lazy(() => import('../pages/auth/SignUp/SignUp'));
const ExternalRoutes = React.lazy(() => import('../pages/external/ExternalRoutes'));
const InternalRoutes = React.lazy(() => import('../pages/internal/InternalRoutes'));


const AppRoutes = () => {

    const dispatch = useDispatch();
    const {isLoggedIn} = useSelector(store => store.authReducer);

    const [userDetailsData, userDetailsError, userDetailsLoading, fetchUserDetails] = useAxios();

    useEffect(() => {
        if (userDetailsData?.success){
            dispatch(setUserDetails(userDetailsData?.user_details))
        }
    }, [userDetailsData, dispatch])

    useEffect(() => {
        dispatch(checkAuthStatus())
        if (isLoggedIn) {
            fetchUserDetails(getUserDetailsService())
        }
    }, [isLoggedIn])

    
    const PrivateRoute = () => {
        if (!isLoggedIn){
            return <Navigate to="/signin" />
        } 
        if (userDetailsData?.user_details?.roles.length) {
            return <InternalRoutes />
        }
        return <ExternalRoutes />
    };
    
    const PublicRoute = ({ children }) => {
        return isLoggedIn ? <Navigate to="/" /> : children;
    };

    return (
        <Router>
            <Suspense fallback={<Loader />}>
                <Routes>
                    <Route path="/signin" element={<PublicRoute><SignInPage /></PublicRoute>} />
                    <Route path="/signup" element={<PublicRoute><SignUpPage /></PublicRoute>} />

                    <Route path="/*" element={<PrivateRoute></PrivateRoute>} />

                    <Route path="*" element={isLoggedIn ? <Navigate to="/" /> : <Navigate to="/signin" />} />
                </Routes>
            </Suspense>
        </Router>
    );
};

export default AppRoutes;