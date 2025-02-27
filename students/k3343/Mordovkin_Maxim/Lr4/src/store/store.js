// src/store/store.js
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import flightReducer from './slices/flightSlice';
import reportReducer from './slices/reportSlice';
import crewReducer from './slices/crewSlice';
import aircraftReducer from './slices/aircraftSlice';
import carrierReducer from './slices/carrierSlice';
import transitStopReducer from './slices/transitStopSlice';
import aircraftMaintenanceReducer from './slices/aircraftMaintenanceSlice';

export const store = configureStore({
    reducer: {
        auth: authReducer,
        flights: flightReducer,
        reports: reportReducer,
        crew: crewReducer,
        aircrafts: aircraftReducer,
        carriers: carrierReducer,
        transitStops: transitStopReducer,
        aircraftMaintenances: aircraftMaintenanceReducer,
    },
});
