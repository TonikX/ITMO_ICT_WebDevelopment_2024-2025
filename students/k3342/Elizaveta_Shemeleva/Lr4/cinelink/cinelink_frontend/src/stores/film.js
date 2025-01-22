import {defineStore} from "pinia";
import axios from "axios";

export const useFilmStore = defineStore("film", {
    state: () => ({
        film: null,
        isLoading: false,
        error: null,
    }),
    actions: {
        async fetchFilmDetails(id) {
            this.isLoading = true;
            this.error = null;
            try {
                const response = await axios.get(`/movies/${id}/`)
                this.film = response.data;
            } catch (error) {
                console.error("Failed to fetch film details:", error.response?.data || error.message);
                this.error = error.response?.data?.detail || "Failed to fetch film details.";
            } finally {
                this.isLoading = false;
            }
        },
    },
});