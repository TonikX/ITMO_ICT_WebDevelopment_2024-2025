/* eslint-disable @typescript-eslint/no-unused-vars */

"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import { toast } from "react-hot-toast";
import authService from "../services/authService";

interface User {
  id: number;
  username: string;
  role: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<{ message: string }>;
  register: (
    name: string,
    email: string,
    password: string
  ) => Promise<{ message: string }>;
  logout: () => Promise<Response | undefined>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const profile = await authService.getProfile();
        console.log(profile);

        setUser(profile);
      } catch (error) {
        setUser(null);
      }
    };
    fetchUser();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const res = await authService.login(email, password);
      const profile = await authService.getProfile();
      setUser(profile);
      toast.success("Вход выполнен успешно!");
      return res;
    } catch (error) {
      toast.error("Ошибка при входе. Проверьте свои данные.");
      return error;
    }
  };

  const register = async (name: string, email: string, password: string) => {
    try {
      const res = await authService.register(name, email, password);
      toast.success("Регистрация прошла успешно! Войдите в систему.");
      router.push("/");
      return res;
    } catch (error) {
      toast.error("Ошибка при регистрации. Попробуйте снова.");
      return error;
    }
  };

  const logout = async () => {
    try {
      const res = await authService.logout();
      setUser(null);
      toast.success("Вы успешно вышли из системы.");
      return res;
    } catch (error) {
      toast.error("Ошибка при выходе из системы.");
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
