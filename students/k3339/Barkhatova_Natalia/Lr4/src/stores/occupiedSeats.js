import {defineStore} from "pinia";
import api from "@/api/api.js";

export const useOccupiedSeatsStore = defineStore("seats", {
    state: () => ({
        occupiedSeats: new Set(),
    }),
    actions: {
        async fetchSeatStatus(sessionId, seatId) {
            try {
                const {data} = await api.get(`/rest/seats/${sessionId}/${seatId}/status`);
                if (data) {
                    this.occupiedSeats.add(`${sessionId}-${seatId}`);
                } else {
                    this.occupiedSeats.delete(`${sessionId}-${seatId}`);
                }
            } catch (error) {
                console.error("Ошибка при получении статуса места:", error);
            }
        },
        async occupySeat(sessionId, seatId) {
            try {
                await api.post(`/rest/seats/${sessionId}/${seatId}/occupy`);
                this.occupiedSeats.add(`${sessionId}-${seatId}`);
            } catch (error) {
                console.error("Ошибка при занятии места:", error);
            }
        },
        async freeSeat(sessionId, seatId) {
            try {
                await api.post(`/rest/seats/${sessionId}/${seatId}/free`);
                this.occupiedSeats.delete(`${sessionId}-${seatId}`);
            } catch (error) {
                console.error("Ошибка при освобождении места:", error);
            }
        },
    },
});
