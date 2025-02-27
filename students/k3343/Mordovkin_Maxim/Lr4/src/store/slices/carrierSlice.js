// src/store/slices/carrierSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_URL = 'http://localhost:8080/backend_war/api';

// Асинхронные действия
export const fetchCarriers = createAsyncThunk(
    'carriers/fetchAll',
    async (_, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_URL}/carriers`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            return response.data; // список Carrier
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Fetch carriers failed');
        }
    }
);

export const createCarrier = createAsyncThunk(
    'carriers/create',
    async (carrierData, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post(`${API_URL}/carriers`, carrierData, {
                headers: { Authorization: `Bearer ${token}` },
            });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Create carrier failed');
        }
    }
);

export const updateCarrier = createAsyncThunk(
    'carriers/update',
    async ({ id, data }, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.put(`${API_URL}/carriers/${id}`, data, {
                headers: { Authorization: `Bearer ${token}` },
            });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Update carrier failed');
        }
    }
);

export const deleteCarrier = createAsyncThunk(
    'carriers/delete',
    async (id, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            await axios.delete(`${API_URL}/carriers/${id}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            return id;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Delete carrier failed');
        }
    }
);

// Слайс
const carrierSlice = createSlice({
    name: 'carriers',
    initialState: {
        carriers: [],
        loading: false,
        error: null,
    },
    reducers: {
        clearError: (state) => {
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchCarriers.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchCarriers.fulfilled, (state, action) => {
                state.loading = false;
                state.carriers = action.payload;
            })
            .addCase(fetchCarriers.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload?.error || 'Fetch carriers failed';
            })
            .addCase(createCarrier.fulfilled, (state, action) => {
                state.carriers.push(action.payload);
            })
            .addCase(createCarrier.rejected, (state, action) => {
                state.error = action.payload?.error || 'Create carrier failed';
            })
            .addCase(updateCarrier.fulfilled, (state, action) => {
                const index = state.carriers.findIndex(c => c.carrierID === action.payload.carrierID);
                if (index !== -1) {
                    state.carriers[index] = action.payload;
                }
            })
            .addCase(updateCarrier.rejected, (state, action) => {
                state.error = action.payload?.error || 'Update carrier failed';
            })
            .addCase(deleteCarrier.fulfilled, (state, action) => {
                state.carriers = state.carriers.filter(c => c.carrierID !== action.payload);
            })
            .addCase(deleteCarrier.rejected, (state, action) => {
                state.error = action.payload?.error || 'Delete carrier failed';
            });
    },
});

export const { clearError } = carrierSlice.actions;
export default carrierSlice.reducer;
