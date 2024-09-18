import React, { Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Loader from '../../../components/Loader';
import BottomTabs from '../../../components/Internal/BottomTabs';
import { USERS_PAGES } from './PageConstants';

const CustomersPage = React.lazy(() => import('./CustomePage'));

const UsersRoutes = () => (
  <Suspense fallback={<Loader />}>
    <Routes>
        <Route index element={<Navigate to="/customers" replace />} />
        <Route path='/customers' element={<CustomersPage />} />
    </Routes>
    <BottomTabs pages={USERS_PAGES} />
  </Suspense>
);

export default UsersRoutes;