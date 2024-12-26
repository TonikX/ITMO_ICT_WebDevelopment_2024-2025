"use client";
import Cookies from "js-cookie";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

const authService = {
  login: async (email: string, password: string) => {
    console.log(email, password);

    const res = await fetch(`api/auth`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
      credentials: "include",
    });
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.message);
    }

    return res.json();
  },

  register: async (name: string, email: string, password: string) => {
    const res = await fetch("api/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, password }),
    });

    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.message);
    }

    return res.json();
  },

  logout: async () => {
    const res = await fetch(`${API_URL}/auth/logout`, {
      method: "POST",
      credentials: "include",
    });
    Cookies.remove("authToken");

    if (!res.ok) {
      throw new Error("Ошибка при выходе");
    }
    return res;
  },

  getProfile: async () => {
    const res = await fetch(`${API_URL}/auth/profile`, {
      method: "GET",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!res.ok) {
      throw new Error("Не удалось получить профиль");
    }

    return res.json();
  },
};

export default authService;
