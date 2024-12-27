import React, { ReactElement, useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

type PrivateRouteProps = {
    children: ReactElement;
};

const PrivateRoute: React.FC<PrivateRouteProps> = ({ children }) => {
    const authContext = useContext(AuthContext);
    console.log(authContext);

    if (!authContext || !authContext.token) {
        return <Navigate to="/login" />;
    }

    return children;
};

export default PrivateRoute;
