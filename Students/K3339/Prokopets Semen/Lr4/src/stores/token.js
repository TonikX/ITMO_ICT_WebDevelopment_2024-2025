import React, { createContext, useContext, useState } from 'react';
import axios from 'axios';

// Создание контекста
const TokenContext = createContext();

// Провайдер контекста
export const TokenProvider = ({ children }) => {
    const [token, setToken] = useState(null);

    const updateToken = (newToken) => {
        setToken(newToken);
        if (newToken) {
            axios.defaults.headers.common['Authorization'] = 'Token ' + newToken;
        } else {
            delete axios.defaults.headers.common['Authorization'];
        }
    };

    return (
        <TokenContext.Provider value={{ token, setToken: updateToken }}>
            {children}
        </TokenContext.Provider>
    );
};

export const useToken = () => {
    return useContext(TokenContext);
};
