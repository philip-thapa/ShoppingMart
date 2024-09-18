import React from 'react';
import Category from "./Category";
import HomeIcon from '@mui/icons-material/Home';
import CategoryIcon from '@mui/icons-material/Category';
import SupervisedUserCircleIcon from '@mui/icons-material/SupervisedUserCircle';


const UserRoutes = React.lazy(() => import('./usermanagement/UserRoutes'));

export const INTERNAL_MODULES = [
    { name: 'Home', path: '/', additionalPath: '/', icon: <HomeIcon />},
    { name: 'User Management', path: '/users/*', additionalPath: '/users/customers', component: <UserRoutes />, icon: <SupervisedUserCircleIcon />},
    { name: 'Categories', path: '/category-management', additionalPath: '', component: <Category />, icon: <CategoryIcon /> },
  ];
