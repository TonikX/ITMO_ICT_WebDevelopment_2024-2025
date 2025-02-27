// src/store/slices/crewSlice.js

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_URL = 'http://localhost:8080/backend_war/api';

// 1) applyForCrew
export const applyForCrew = createAsyncThunk(
    'crew/applyForCrew',
    async ({ userId, fullName, age, education, workExperience, passportData, role }, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post(
                `${API_URL}/crew/apply`,
                {
                    userId,
                    fullName,
                    age,
                    education,
                    workExperience,
                    passportData,
                    role,
                },
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
            return response.data; // { "success": true }
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Apply for crew failed');
        }
    }
);

// 2) fetchPendingCrew (список PENDING-заявок, для ADMIN)
export const fetchPendingCrew = createAsyncThunk(
    'crew/fetchPendingCrew',
    async (_, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_URL}/crew/pending`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            // response.data — это List<CrewMemberDTO> (JSON)
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Fetch pending crew failed');
        }
    }
);

// 3) approveCrew (одобрить заявку)
export const approveCrew = createAsyncThunk(
    'crew/approveCrew',
    async (crewMemberId, { rejectWithValue }) => { // crewMemberId вместо crewMemberID
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post(
                `${API_URL}/crew/approve`,
                { crewMemberId }, // crewMemberId вместо crewMemberID
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
            return crewMemberId;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Approve crew failed');
        }
    }
);

// 4) rejectCrew (отклонить заявку)
export const rejectCrew = createAsyncThunk(
    'crew/rejectCrew',
    async (crewMemberId, { rejectWithValue }) => { // crewMemberId вместо crewMemberID
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post(
                `${API_URL}/crew/reject`,
                { crewMemberId }, // crewMemberId вместо crewMemberID
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
            return crewMemberId;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Reject crew failed');
        }
    }
);

// 5) fetchMyCrewApplications (заявки конкретного пользователя)
export const fetchMyCrewApplications = createAsyncThunk(
    'crew/fetchMyCrewApplications',
    async (userId, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_URL}/crew/my?userId=${userId}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            // вернём массив CrewMemberDTO
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Fetch my crew apps failed');
        }
    }
);

export const fetchAllCrewMembers = createAsyncThunk(
    'crew/fetchAllCrewMembers',
    async (_, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_URL}/crew-members`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            return response.data; // список CrewMemberDTO
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Fetch all crew members failed');
        }
    }
);

export const assignCrewMember = createAsyncThunk(
    'crew/assignCrewMember',
    async ({ flightId, crewMemberId }, { rejectWithValue }) => { // crewMemberId вместо crewMemberID
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post(
                `${API_URL}/flights/${flightId}/crew-members/${crewMemberId}`,
                {},
                { headers: { Authorization: `Bearer ${token}` } }
            );
            return response.data; // обновлённый CrewMemberDTO
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Assign crew member failed');
        }
    }
);

export const removeCrewMember = createAsyncThunk(
    'crew/removeCrewMember',
    async ({ flightId, crewMemberId }, { rejectWithValue }) => { // crewMemberId вместо crewMemberID
        try {
            const token = localStorage.getItem('token');
            const response = await axios.delete(
                `${API_URL}/flights/${flightId}/crew-members/${crewMemberId}`,
                { headers: { Authorization: `Bearer ${token}` } }
            );
            return response.data; // обновлённый CrewMemberDTO
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Remove crew member failed');
        }
    }
);

// Начальное состояние
const initialState = {
    loading: false,
    error: null,
    members: [], // список всех членов экипажа
    myApplications: [], // список заявок текущего юзера
};

const crewSlice = createSlice({
    name: 'crew',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            // ---------- applyForCrew ----------
            .addCase(applyForCrew.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(applyForCrew.fulfilled, (state, action) => {
                state.loading = false;
                // Можно добавить логики для myApplications, если необходимо
            })
            .addCase(applyForCrew.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload?.error || 'Apply for crew failed';
            })

            // ---------- fetchPendingCrew ----------
            .addCase(fetchPendingCrew.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchPendingCrew.fulfilled, (state, action) => {
                state.loading = false;
                state.members = action.payload;
            })
            .addCase(fetchPendingCrew.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload?.error || 'Fetch pending crew failed';
            })

            // ---------- approveCrew ----------
            .addCase(approveCrew.fulfilled, (state, action) => {
                const id = action.payload;
                state.members = state.members.filter((m) => m.crewMemberId !== id); // Изменено crewMemberId
            })
            .addCase(approveCrew.rejected, (state, action) => {
                state.error = action.payload?.error || 'Approve crew failed';
            })

            // ---------- rejectCrew ----------
            .addCase(rejectCrew.fulfilled, (state, action) => {
                const id = action.payload;
                state.members = state.members.filter((m) => m.crewMemberId !== id); // Изменено crewMemberId
            })
            .addCase(rejectCrew.rejected, (state, action) => {
                state.error = action.payload?.error || 'Reject crew failed';
            })

            // ---------- fetchMyCrewApplications ----------
            .addCase(fetchMyCrewApplications.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchMyCrewApplications.fulfilled, (state, action) => {
                state.loading = false;
                state.myApplications = action.payload;
            })
            .addCase(fetchMyCrewApplications.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload?.error || 'Fetch my crew apps failed';
            })

            // ---------- fetchAllCrewMembers ----------
            .addCase(fetchAllCrewMembers.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchAllCrewMembers.fulfilled, (state, action) => {
                state.loading = false;
                state.members = action.payload;
            })
            .addCase(fetchAllCrewMembers.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload?.error || 'Fetch all crew members failed';
            })

            // ---------- assignCrewMember ----------
            .addCase(assignCrewMember.fulfilled, (state, action) => {
                const updatedMember = action.payload;
                // Обновляем список членов экипажа
                const index = state.members.findIndex(cm => cm.crewMemberId === updatedMember.crewMemberId);
                if (index !== -1) {
                    state.members[index] = updatedMember;
                }
                // Можно также обновить список myApplications, если нужно
            })
            .addCase(assignCrewMember.rejected, (state, action) => {
                state.error = action.payload?.error || 'Assign crew member failed';
            })

            // ---------- removeCrewMember ----------
            .addCase(removeCrewMember.fulfilled, (state, action) => {
                const updatedMember = action.payload;
                const index = state.members.findIndex(cm => cm.crewMemberId === updatedMember.crewMemberId);
                if (index !== -1) {
                    state.members[index] = updatedMember;
                }
            })
            .addCase(removeCrewMember.rejected, (state, action) => {
                state.error = action.payload?.error || 'Remove crew member failed';
            });
    },
});

// По умолчанию экспортируем сам reducer
export default crewSlice.reducer;
