import React, { Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import Loader from '../../components/Loader';
import CreateCategory from './CreateCategory';

const CategoryPage = React.lazy(() => import('./Category'));

const CategroyRoutes = () => (
  <Suspense fallback={<Loader />}>
    <Routes>
      <Route index element={<CategoryPage />} />
      <Route path="create" element={<CreateCategory />} />
    </Routes>
  </Suspense>
);

export default CategroyRoutes;