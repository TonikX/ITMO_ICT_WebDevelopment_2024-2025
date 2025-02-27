// src/store/slices/aircraftMaintenanceSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_URL = 'http://localhost:8080/backend_war/api';

// Асинхронные действия
export const fetchMaintenances = createAsyncThunk(
    'aircraftMaintenances/fetchAll',
    async (_, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_URL}/aircraft-maintenances`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            return response.data; // список AircraftMaintenance
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Fetch maintenances failed');
        }
    }
);

export const createMaintenance = createAsyncThunk(
    'aircraftMaintenances/create',
    async (maintenanceData, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post(`${API_URL}/aircraft-maintenances`, maintenanceData, {
                headers: { Authorization: `Bearer ${token}` },
            });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Create maintenance failed');
        }
    }
);

export const updateMaintenance = createAsyncThunk(
    'aircraftMaintenances/update',
    async ({ id, data }, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.put(`${API_URL}/aircraft-maintenances/${id}`, data, {
                headers: { Authorization: `Bearer ${token}` },
            });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Update maintenance failed');
        }
    }
);

export const deleteMaintenance = createAsyncThunk(
    'aircraftMaintenances/delete',
    async (id, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            await axios.delete(`${API_URL}/aircraft-maintenances/${id}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            return id;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Delete maintenance failed');
        }
    }
);

// Слайс
const aircraftMaintenanceSlice = createSlice({
    name: 'aircraftMaintenances',
    initialState: {
        maintenances: [],
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
            .addCase(fetchMaintenances.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchMaintenances.fulfilled, (state, action) => {
                state.loading = false;
                state.maintenances = action.payload;
            })
            .addCase(fetchMaintenances.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload?.error || 'Fetch maintenances failed';
            })
            .addCase(createMaintenance.fulfilled, (state, action) => {
                state.maintenances.push(action.payload);
            })
            .addCase(createMaintenance.rejected, (state, action) => {
                state.error = action.payload?.error || 'Create maintenance failed';
            })
            .addCase(updateMaintenance.fulfilled, (state, action) => {
                const index = state.maintenances.findIndex(m => m.maintenanceID === action.payload.maintenanceID);
                if (index !== -1) {
                    state.maintenances[index] = action.payload;
                }
            })
            .addCase(updateMaintenance.rejected, (state, action) => {
                state.error = action.payload?.error || 'Update maintenance failed';
            })
            .addCase(deleteMaintenance.fulfilled, (state, action) => {
                state.maintenances = state.maintenances.filter(m => m.maintenanceID !== action.payload);
            })
            .addCase(deleteMaintenance.rejected, (state, action) => {
                state.error = action.payload?.error || 'Delete maintenance failed';
            });
    },
});

export const { clearError } = aircraftMaintenanceSlice.actions;
export default aircraftMaintenanceSlice.reducer;
