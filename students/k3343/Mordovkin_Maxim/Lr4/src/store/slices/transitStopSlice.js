// src/store/slices/transitStopSlice.js

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_URL = 'http://localhost:8080/backend_war/api';

// 1) fetchTransitStops
export const fetchTransitStops = createAsyncThunk(
    'transitStops/fetchByFlight',
    async (flightId, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_URL}/transit-stops/flight/${flightId}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || { error: 'Fetch transit stops failed' });
        }
    }
);

// 2) addTransitStop
export const addTransitStop = createAsyncThunk(
    'transitStops/add',
    async ({ flightId, transitStop }, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post(`${API_URL}/transit-stops/flight/${flightId}`, transitStop, {
                headers: { Authorization: `Bearer ${token}` },
            });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || { error: 'Add transit stop failed' });
        }
    }
);

// 3) removeTransitStop
export const removeTransitStop = createAsyncThunk(
    'transitStops/remove',
    async ({ transitStopId }, { rejectWithValue }) => { // Убрано flightId
        try {
            const token = localStorage.getItem('token');
            await axios.delete(`${API_URL}/transit-stops/${transitStopId}`, { // Исправлено URL
                headers: { Authorization: `Bearer ${token}` },
            });
            return transitStopId;
            // transitStopId
        } catch (error) {
            return rejectWithValue(error.response?.data || { error: 'Remove transit stop failed' });
        }
    }
);

const initialState = {
    transitStops: [],
    loading: false,
    error: null,
};

const transitStopSlice = createSlice({
    name: 'transitStops',
    initialState,
    reducers: {
        clearError: (state) => {
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchTransitStops.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchTransitStops.fulfilled, (state, action) => {
                state.loading = false;
                state.transitStops = action.payload;
            })
            .addCase(fetchTransitStops.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload?.error || 'Fetch transit stops failed';
            })
            .addCase(addTransitStop.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(addTransitStop.fulfilled, (state, action) => {
                state.loading = false;
                state.transitStops.push(action.payload);
            })
            .addCase(addTransitStop.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload?.error || 'Add transit stop failed';
            })
            .addCase(removeTransitStop.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(removeTransitStop.fulfilled, (state, action) => {
                state.loading = false;
                state.transitStops = state.transitStops.filter(ts => ts.transitStopId !== action.payload);
            })
            .addCase(removeTransitStop.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload?.error || 'Remove transit stop failed';
            });
    },
});

export const { clearError } = transitStopSlice.actions;
export default transitStopSlice.reducer;
