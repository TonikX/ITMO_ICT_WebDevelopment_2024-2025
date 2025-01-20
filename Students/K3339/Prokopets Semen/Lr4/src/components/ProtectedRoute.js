// src/components/ProtectedRoute.jsx
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useToken } from '../stores/token'; // Импортируйте ваш контекст токена

const ProtectedRoute = ({ element }) => {
    const { token } = useToken(); // Проверяем наличие токена

    return token ? element : <Navigate to="/login" />;
};

export default ProtectedRoute;
