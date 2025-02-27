// src/store/slices/authSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// Подставьте ваш реальный URL
const API_URL = 'http://localhost:8080/backend_war/api';

export const login = createAsyncThunk(
    'auth/login',
    async ({ username, password }, { rejectWithValue }) => {
        try {
            const response = await axios.post(`${API_URL}/auth/login`, { username, password });
            localStorage.setItem('token', response.data.token);
            return response.data; // будет { token: "..." }
        } catch (error) {
            // Предположим, что сервер отвечает вида { error: "Some message" }
            return rejectWithValue(error.response?.data);
        }
    }
);

export const register = createAsyncThunk(
    'auth/register',
    async ({ username, password, role }, { rejectWithValue }) => {
        try {
            const response = await axios.post(`${API_URL}/auth/register`, { username, password, role });
            localStorage.setItem('token', response.data.token);
            return response.data; // { token: "..." }
        } catch (error) {
            return rejectWithValue(error.response?.data);
        }
    }
);

export const fetchUserProfile = createAsyncThunk(
    'auth/fetchProfile',
    async (_, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_URL}/auth/me`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            return response.data; // { userId: 1, username: "...", ... }
        } catch (error) {
            return rejectWithValue(error.response?.data);
        }
    }
);

const initialState = {
    user: null,
    token: localStorage.getItem('token'),
    loading: false,
    error: null, // Стараемся хранить тут только строку
};

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        logout: (state) => {
            state.user = null;
            state.token = null;
            localStorage.removeItem('token');
        },
        clearError: (state) => {
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        builder
            // ============== LOGIN ==============
            .addCase(login.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(login.fulfilled, (state, action) => {
                state.loading = false;
                state.token = action.payload.token;
            })
            .addCase(login.rejected, (state, action) => {
                state.loading = false;
                // проверяем, что пришло в action.payload
                if (action.payload && typeof action.payload === 'object' && action.payload.error) {
                    // если это объект { error: "..." }
                    state.error = action.payload.error;
                } else if (typeof action.payload === 'string') {
                    state.error = action.payload;
                } else {
                    state.error = 'Login failed (unknown error)';
                }
            })

            // ============== REGISTER ==============
            .addCase(register.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(register.fulfilled, (state, action) => {
                state.loading = false;
                state.token = action.payload.token;
            })
            .addCase(register.rejected, (state, action) => {
                state.loading = false;
                if (action.payload && typeof action.payload === 'object' && action.payload.error) {
                    state.error = action.payload.error;
                } else if (typeof action.payload === 'string') {
                    state.error = action.payload;
                } else {
                    state.error = 'Registration failed (unknown error)';
                }
            })

            // ============== FETCH USER PROFILE ==============
            .addCase(fetchUserProfile.fulfilled, (state, action) => {
                state.user = action.payload;
            });
    },
});

export const { logout, clearError } = authSlice.actions;
export default authSlice.reducer;
