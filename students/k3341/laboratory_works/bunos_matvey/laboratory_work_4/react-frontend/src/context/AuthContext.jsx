import React, { createContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [authToken, setAuthToken] = useState(() => localStorage.getItem('authToken') || null);
  const navigate = useNavigate();

  useEffect(() => {
    if (authToken) {
      localStorage.setItem('authToken', authToken);
    } else {
      localStorage.removeItem('authToken');
    }
  }, [authToken]);

  const login = async (username, password) => {
    const response = await api.post('/auth/token/login/', { username, password });
    const token = response.data.auth_token;
    setAuthToken(token);
    navigate('/');
  };

  const logout = async () => {
    try {
      await api.post('/auth/token/logout/', null, {
        headers: { Authorization: `Token ${authToken}` }
      });
    } catch (error) {
      console.error('Ошибка при выходе:', error);
    } finally {
      setAuthToken(null);
      navigate('/login');
    }
  };

  const registerUser = async (username, password, email) => {
    await api.post('/auth/users/', { username, password, email });
    await login(username, password);
  };

  return (
    <AuthContext.Provider
      value={{
        authToken,
        login,
        logout,
        registerUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
