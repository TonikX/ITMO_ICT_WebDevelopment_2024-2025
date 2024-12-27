import React, { createContext, useState, ReactNode } from 'react';

type AuthContextType = {
    token: string | null;
    login: (username: string, password: string) => Promise<void>;
    register: (username: string, password: string) => Promise<void>;
    logout: () => void;
};

export const AuthContext = createContext<AuthContextType>({
    token: null,
    login: async () => {},
    register: async () => {},
    logout: () => {},
});

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));

    const login = async (username: string, password: string) => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/auth/token/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                throw new Error('Ошибка при входе. Проверьте логин/пароль.');
            }

            const data = await response.json();
            const { auth_token } = data;

            setToken(auth_token);
            localStorage.setItem('token', auth_token);
            localStorage.setItem('username', username);

        } catch (error) {
            console.error(error);
            throw error;
        }
    };

    const register = async (username: string, password: string) => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/auth/users/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Ошибка при регистрации.');
            }

            await login(username, password);

        } catch (error) {
            console.error(error);
            throw error;
        }
    };

    const logout = () => {
        setToken(null);
        localStorage.removeItem('token');
        localStorage.removeItem('username');
    };

    return (
        <AuthContext.Provider value={{ token, login, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
