import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { ThemeProvider } from '@mui/material/styles'; // Import ThemeProvider
import CssBaseline from '@mui/material/CssBaseline'; // Import CssBaseline for consistent global styles
import theme from './theme'; // Import your custom theme

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);

root.render(
    <React.StrictMode>
        <ThemeProvider theme={theme}> {/* Apply your custom theme */}
            <CssBaseline /> {/* Ensures consistent baseline styles */}
            <App />
        </ThemeProvider>
    </React.StrictMode>
);

reportWebVitals();