// Routes.js
import React, {Suspense} from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import CategroyRoutes from "../pages/category/category.routes";
import Loader from "../components/Loader";
import { useSelector } from "react-redux";


const SignInPage = React.lazy(() => import('../pages/auth/SignIn/Signin'));
const SignUpPage = React.lazy(() => import('../pages/auth/SignUp/SignUp'));
const HomePage = React.lazy(() => import('../pages/home/Home'));


const AppRoutes = () => {
    const {isLoggedIn} = useSelector(store => store.authReducer);

    const isAuthenticated = () => {
        return !!isLoggedIn;
    };
    
    const PrivateRoute = ({ children }) => {
        return isAuthenticated() ? children : <Navigate to="/signin" />;
    };
    
    const PublicRoute = ({ children }) => {
        return isAuthenticated() ? <Navigate to="/" /> : children;
    };

    return (
        <Router>
            <Suspense fallback={<Loader />}>
                <Routes>
                    <Route path="/signin" element={<PublicRoute><SignInPage /></PublicRoute>} />
                    <Route path="/signup" element={<PublicRoute><SignUpPage /></PublicRoute>} />

                    <Route path="/" element={<PrivateRoute><HomePage /></PrivateRoute>} />

                    <Route path="/category/*" element={
                        <PrivateRoute>
                            <CategroyRoutes />
                        </PrivateRoute>
                    } />

                    <Route path="*" element={isAuthenticated() ? <Navigate to="/" /> : <Navigate to="/signin" />} />
                </Routes>
            </Suspense>
        </Router>
    );
};

export default AppRoutes;