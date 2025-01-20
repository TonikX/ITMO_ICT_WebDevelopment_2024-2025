import {defineStore} from 'pinia';
import api from '@/api/api.js';

export const useTicketStore = defineStore({
    id: 'ticket',
    state: () => ({
        tickets: [],
        selectedSeats: [],
    }),
    actions: {
        async fetchCurrentUserTickets() {
            try {
                const response = await api.get('rest/tickets/user');
                this.tickets = response.data;
            } catch (error) {
                console.error('Failed to fetch tickets:', error.response?.data);
            }
        },

        async fetchTickets() {
            try {
                const response = await api.get('/rest/admin/tickets');
                this.tickets = response.data;

            } catch (error) {
                console.error('Failed to fetch tickets:', error.response?.data);
            }
        },

        async addTicket(ticket) {
            try {
                const response = await api.post('/rest/tickets', ticket);
                this.tickets.push(response.data);
            } catch (error) {
                console.error('Failed to add ticket:', error.response?.data);
            }
        },

        addSeat(seat) {
            if (!this.selectedSeats.some(s => s.id === seat.id)) {
                this.selectedSeats.push(seat);
            }
        },

        removeSeat(seat) {
            this.selectedSeats = this.selectedSeats.filter(s => s.id !== seat.id);
        },

        clearSelectedSeats() {
            this.selectedSeats = [];
        },

        updateSelectedSeats(seat) {
            if (this.selectedSeats.some(s => s.id === seat.id)) {
                this.removeSeat(seat);
            } else {
                this.addSeat(seat);
            }
        },
    },
});
