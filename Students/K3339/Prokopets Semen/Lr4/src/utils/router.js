import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import BusPage from '../page/BusPage';
import BusTypesPage from '../page/BusTypesPage';
import DriverPage from '../page/DriverPage';
import RoutePage from '../page/RoutePage';
import WorkShiftsPage from '../page/WorkShiftsPage';
import LoginPage from '../page/LoginPage';
import RegisterPage from '../page/RegisterPage';
import ProtectedRoute from '../components/ProtectedRoute';
// BusType
const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/" element={<ProtectedRoute element={<BusPage />} />} />
            <Route path="/bus" element={<ProtectedRoute element={<BusPage />} />} />
            <Route path="/driver" element={<ProtectedRoute element={<DriverPage />} />} />
            <Route path="/route" element={<ProtectedRoute element={<RoutePage />} />} />
            <Route path="/work-shifts" element={<ProtectedRoute element={<WorkShiftsPage />} />} />
            <Route path="/bustype" element={<ProtectedRoute element={<BusTypesPage />} />} />
            <Route path="*" element={<LoginPage />} />
        </Routes>
    );
};

export default AppRoutes;
