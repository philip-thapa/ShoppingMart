import { Box } from '@mui/material'
import React, { Suspense } from 'react'
import ModuleCard from '../../components/Modules'
import { Route, Routes } from 'react-router-dom';
import Loader from '../../components/Loader';
import { INTERNAL_MODULES } from './constants';


const HomePage = React.lazy(() => import('./Home'));

const InternalRoutes = () => (
  <Suspense fallback={<Loader />}>
    <Routes>
      <Route index element={<HomePage />} />
      {
        INTERNAL_MODULES.map(module=>(
          <Route path={module.path} element={module.component} />
        ))
      }
    </Routes>
  </Suspense>
);

export default InternalRoutes;