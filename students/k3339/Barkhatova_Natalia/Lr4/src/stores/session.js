import { defineStore } from 'pinia';
import api from '@/api/api.js';

export const useSessionStore = defineStore({
    id: 'session',
    state: () => ({
        sessions: [],
    }),
    actions: {
        async fetchSessions() {
            try {
                const response = await api.get('/rest/sessions');
                this.sessions = response.data;
            } catch (error) {
                console.error('Failed to fetch sessions:', error.response?.data);
            }
        },
        async addSession(session) {
            const response = await api.post('/rest/admin/sessions', session);
            this.sessions.push(response.data);
        },
        async updateSession(session) {
            const response = await api.put(`/rest/admin/sessions/${session.id}`, session);
            const index = this.sessions.findIndex((s) => s.id === session.id);
            this.sessions[index] = response.data;
        },
        async deleteSession(sessionId) {
            try {
                await api.delete('/rest/admin/sessions', { data: { id: sessionId }});
                this.sessions = this.sessions.filter((session) => session.id !== sessionId);
            } catch (error) {
                console.error('Failed to delete session:', error.response?.data);
            }
        }
    },
});
