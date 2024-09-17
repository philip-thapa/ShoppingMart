import { Box } from '@mui/material'
import React, { Suspense } from 'react'
import ModuleCard from '../../components/Modules'
import { Route, Routes } from 'react-router-dom';
import Loader from '../../components/Loader';


const HomePage = React.lazy(() => import('./Home'));

const ExternalRoutes = () => (
  <Suspense fallback={<Loader />}>
    <Routes>
      <Route index element={<HomePage />} />
      {/* <Route path="create" element={<CreateCategory />} /> */}
    </Routes>
  </Suspense>
);

export default ExternalRoutes;