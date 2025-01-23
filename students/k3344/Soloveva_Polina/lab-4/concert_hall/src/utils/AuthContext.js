import React, { createContext, useState, useEffect } from "react";
import axios from "axios";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [userRole, setUserRole] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem("token"));

  useEffect(() => {
    const fetchUserRole = async () => {
      if (!isAuthenticated) return;

      try {
        const response = await axios.get("http://localhost:8000/user-info/", {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` },
        });
        setUserRole(response.data.is_admin ? "admin" : "user");
      } catch (error) {
        console.error("Ошибка при загрузке пользователя:", error);
        setUserRole(null);
      }
    };

    fetchUserRole();
  }, [isAuthenticated]);

  const login = (token) => {
    localStorage.setItem("token", token);
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUserRole(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ userRole, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
