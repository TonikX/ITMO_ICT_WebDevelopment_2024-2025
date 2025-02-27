// src/store/slices/flightSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_URL = 'http://localhost:8080/backend_war/api';

// Асинхронные действия
export const fetchFlights = createAsyncThunk(
    'flights/fetchAll',
    async (_, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_URL}/flights`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            return response.data; // Данные содержат crews и crewMembers
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Fetch flights failed');
        }
    }
);

export const fetchFlightById = createAsyncThunk(
    'flights/fetchById',
    async (id, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_URL}/flights/${id}`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            return response.data; // Данные содержат crews и crewMembers
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Fetch flight by ID failed');
        }
    }
);

export const createFlight = createAsyncThunk(
    'flights/create',
    async (flightData, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post(`${API_URL}/flights`, flightData, {
                headers: { Authorization: `Bearer ${token}` }
            });
            return response.data; // Новая Flight с crews и crewMembers
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Create flight failed');
        }
    }
);

export const updateFlight = createAsyncThunk(
    'flights/update',
    async ({ id, data }, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.put(`${API_URL}/flights/${id}`, data, {
                headers: { Authorization: `Bearer ${token}` }
            });
            return response.data; // Обновлённая Flight с crews и crewMembers
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Update flight failed');
        }
    }
);

export const deleteFlight = createAsyncThunk(
    'flights/delete',
    async (id, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            await axios.delete(`${API_URL}/flights/${id}`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            return id;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Delete flight failed');
        }
    }
);

// Слайс
const flightSlice = createSlice({
    name: 'flights',
    initialState: {
        flights: [],
        loading: false,
        error: null,
        currentFlight: null,
    },
    reducers: {
        setCurrentFlight: (state, action) => {
            state.currentFlight = action.payload;
        },
        clearError: (state) => {
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchFlights.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchFlights.fulfilled, (state, action) => {
                state.loading = false;
                state.flights = action.payload;
            })
            .addCase(fetchFlights.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            .addCase(fetchFlightById.pending, (state) => {
                state.loading = true;
                state.error = null;
                state.currentFlight = null;
            })
            .addCase(fetchFlightById.fulfilled, (state, action) => {
                state.loading = false;
                state.currentFlight = action.payload;
            })
            .addCase(fetchFlightById.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            .addCase(createFlight.fulfilled, (state, action) => {
                state.flights.push(action.payload);
            })
            .addCase(createFlight.rejected, (state, action) => {
                state.error = action.payload;
            })
            .addCase(updateFlight.fulfilled, (state, action) => {
                const index = state.flights.findIndex(f => f.flightId === action.payload.flightId);
                if (index !== -1) {
                    state.flights[index] = action.payload;
                }
                if (state.currentFlight && state.currentFlight.flightId === action.payload.flightId) {
                    state.currentFlight = action.payload;
                }
            })
            .addCase(updateFlight.rejected, (state, action) => {
                state.error = action.payload;
            })
            .addCase(deleteFlight.fulfilled, (state, action) => {
                state.flights = state.flights.filter(f => f.flightId !== action.payload);
                if (state.currentFlight && state.currentFlight.flightId === action.payload) {
                    state.currentFlight = null;
                }
            })
            .addCase(deleteFlight.rejected, (state, action) => {
                state.error = action.payload;
            });
    },
});

export const { setCurrentFlight, clearError } = flightSlice.actions;
export default flightSlice.reducer;
