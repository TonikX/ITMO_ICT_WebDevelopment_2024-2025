import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_URL = 'http://localhost:8080/backend_war/api';

export const getMostFrequentAircraftType = createAsyncThunk(
    'reports/getMostFrequentAircraftType',
    async ({ departure, destination }, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(
                `${API_URL}/reports/most-frequent-aircraft-type?departure=${departure}&destination=${destination}`,
                { headers: { Authorization: `Bearer ${token}` } }
            );
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response.data);
        }
    }
);

export const getRoutesBelowOccupancy = createAsyncThunk(
    'reports/getRoutesBelowOccupancy',
    async (occupancy, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(
                `${API_URL}/reports/routes-below-occupancy?occupancy=${occupancy}`,
                { headers: { Authorization: `Bearer ${token}` } }
            );
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response.data);
        }
    }
);

export const getAircraftsInRepairCount = createAsyncThunk(
    'reports/getAircraftsInRepairCount',
    async (_, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(
                `${API_URL}/reports/aircrafts-in-repair-count`,
                { headers: { Authorization: `Bearer ${token}` } }
            );
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response.data);
        }
    }
);

export const getCarrierWorkersCount = createAsyncThunk(
    'reports/getCarrierWorkersCount',
    async (carrierId, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(
                `${API_URL}/reports/carrier-workers-count/${carrierId}`,
                { headers: { Authorization: `Bearer ${token}` } }
            );
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response.data);
        }
    }
);

export const getAircraftsReportByType = createAsyncThunk(
    'reports/getAircraftsReportByType',
    async (carrierId, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(
                `${API_URL}/reports/aircrafts-report-by-type/${carrierId}`,
                { headers: { Authorization: `Bearer ${token}` } }
            );
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response.data);
        }
    }
);

const initialState = {
    mostFrequentAircraftType: null,
    routesBelowOccupancy: [],
    aircraftsInRepairCount: 0,
    carrierWorkersCount: 0,
    aircraftsReport: null,
    loading: false,
    error: null,
};

const reportSlice = createSlice({
    name: 'reports',
    initialState,
    reducers: {
        clearReportData: (state) => {
            state.mostFrequentAircraftType = null;
            state.routesBelowOccupancy = [];
            state.aircraftsInRepairCount = 0;
            state.carrierWorkersCount = 0;
            state.aircraftsReport = null;
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        builder
            // Most Frequent Aircraft Type
            .addCase(getMostFrequentAircraftType.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(getMostFrequentAircraftType.fulfilled, (state, action) => {
                state.loading = false;
                state.mostFrequentAircraftType = action.payload;
            })
            .addCase(getMostFrequentAircraftType.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Routes Below Occupancy
            .addCase(getRoutesBelowOccupancy.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(getRoutesBelowOccupancy.fulfilled, (state, action) => {
                state.loading = false;
                state.routesBelowOccupancy = action.payload;
            })
            .addCase(getRoutesBelowOccupancy.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Aircrafts in Repair Count
            .addCase(getAircraftsInRepairCount.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(getAircraftsInRepairCount.fulfilled, (state, action) => {
                state.loading = false;
                state.aircraftsInRepairCount = action.payload;
            })
            .addCase(getAircraftsInRepairCount.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Carrier Workers Count
            .addCase(getCarrierWorkersCount.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(getCarrierWorkersCount.fulfilled, (state, action) => {
                state.loading = false;
                state.carrierWorkersCount = action.payload;
            })
            .addCase(getCarrierWorkersCount.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Aircrafts Report by Type
            .addCase(getAircraftsReportByType.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(getAircraftsReportByType.fulfilled, (state, action) => {
                state.loading = false;
                state.aircraftsReport = action.payload;
            })
            .addCase(getAircraftsReportByType.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            });
    },
});

export const { clearReportData } = reportSlice.actions;
export default reportSlice.reducer;