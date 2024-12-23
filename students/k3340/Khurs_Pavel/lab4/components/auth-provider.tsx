'use client';
import { api, getToken, removeToken, setToken } from '@/api/api';
import { useRouter } from 'next/navigation';
import React, { createContext, useState, useContext, useEffect } from 'react';

interface User {
  username: string;
  email?: string;
}

interface AuthContextValue {
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  setToken: (token: string | null) => void;
  error: string | null;
}

const AuthContext = createContext<AuthContextValue>({
  user: null,
  login: async () => {},
  logout: () => {},
  setToken: () => {},
  error: null,
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(null);
  const navigate = useRouter();

  useEffect(() => {
    const token = getToken();

    if (token) {
      fetchUserData()
        .then((usr) => {
          setUser(usr);
          setError(null);
        })
        .catch(() => {
          removeToken();
          setUser(null);
        });
    } else {
      setUser(null);
    }
  }, []);

  async function fetchUserData() {
    const res = await api.get('/auth/users/me/');
    return res.data as User;
  }

  async function login(username: string, password: string) {
    try {
      const res = await api.post('/auth/token/login/', { username, password });
      const { auth_token: newToken } = res.data;

      setToken(newToken);
      const fetchedUser = await fetchUserData();
      setUser(fetchedUser);
      setError(null);
      navigate.push('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed');
    }
  }

  function logout() {
    removeToken();
    setUser(null);
    navigate.push('/login');
  }

  function handleSetToken(newToken: string | null) {
    if (newToken) {
      setToken(newToken);
      fetchUserData()
        .then((usr) => {
          setUser(usr);
          setError(null);
        })
        .catch(() => {
          removeToken();
          setUser(null);
        });
    } else {
      removeToken();
      setUser(null);
    }
  }

  const value: AuthContextValue = {
    user,
    login,
    logout,
    setToken: handleSetToken,
    error,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
