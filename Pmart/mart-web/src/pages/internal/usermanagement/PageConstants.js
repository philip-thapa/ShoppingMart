import React from 'react';
import CategoryIcon from '@mui/icons-material/Category';
import SupervisedUserCircleIcon from '@mui/icons-material/SupervisedUserCircle';


export const USERS_PAGES = [
    { name: 'Customers', path: '/users/customers', icon: <SupervisedUserCircleIcon />},
    { name: 'Internal Users', path: '/users/internal/users', icon: <CategoryIcon /> },
  ];
