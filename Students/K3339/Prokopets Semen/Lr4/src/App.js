import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { TokenProvider } from './stores/token';
import AppRoutes from './utils/router';

const App = () => {
    return (
        <TokenProvider>
            <Router>
                <AppRoutes />
            </Router>
        </TokenProvider>
    );
};

export default App;
