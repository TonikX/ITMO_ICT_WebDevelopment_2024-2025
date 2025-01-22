import {defineStore} from "pinia";
import axios from "axios";
import router from "@/router"; // Import the router

export const useAuthStore = defineStore("auth", {
    state: () => ({
        token: localStorage.getItem("authToken") || null,
        user: null, // The user data will be fetched after authentication
    }),

    actions: {
        setToken(token) {
            this.token = token;
            localStorage.setItem("authToken", token); // Persist the token in localStorage
            axios.defaults.headers.common["Authorization"] = `Token ${token}`; // Set default Axios headers
        },

        initializeAuth() {
            const storedToken = localStorage.getItem("authToken");
            if (storedToken) {
                this.setToken(storedToken);
                this.fetchUser(); // Fetch user data after setting token
            }
        },

        async login(email, password) {
            try {
                const response = await axios.post("/auth/token/login/", {
                    email: email.trim(),
                    password: password.trim(),
                });
                this.setToken(response.data.auth_token);
                await this.fetchUser();
            } catch (error) {
                console.error("Login failed:", error.response?.data || error.message);
                throw error.response?.data || new Error("Login failed");
            }
        },

        async register(email, password, rePassword) {
            try {
                const response = await axios.post("/auth/users/", {
                    email: email.trim(),
                    password: password.trim(),
                    re_password: rePassword.trim(),
                });
                console.log("Registration successful:", response.data);
                return response.data;
            } catch (error) {
                console.error("Registration failed:", error.response?.data || error.message);
                throw error.response?.data || new Error("Registration failed");
            }
        },

        async fetchUser() {
            if (!this.token) return;

            try {
                const response = await axios.get("/auth/users/me/");
                this.user = response.data;
            } catch (error) {
                console.error("Failed to fetch user details:", error.response?.data || error.message);
                this.clearAuth();
                throw error.response?.data || new Error("Failed to fetch user details");
            }
        },

        clearAuth() {
            this.token = null;
            this.user = null;
            localStorage.removeItem("authToken");
            delete axios.defaults.headers.common["Authorization"];
        },

        async logout() {
            try {
                await axios.post("/auth/token/logout/"); // Inform the backend to invalidate the token
            } catch (error) {
                console.error("Error during logout:", error.response?.data || error.message);
            }
            this.clearAuth();
            router.push("/"); // Redirect to the root page
        },
    },

    getters: {
        isAuthenticated: (state) => !!state.token && !!state.user,
    },
});