import {defineStore} from "pinia";
import axios from "axios";

export const useFilmsStore = defineStore("films", {
    state: () => ({
        films: [],
        genres: [],
        decades: [],
        ratings: [],
        isLoading: false,
        error: null,
    }),
    actions: {
        async fetchFilms(filters = {}) {
            this.isLoading = true;
            this.error = null;

            try {
                const response = await axios.get("/movies/", {params: filters});
                this.films = response.data.results || response.data; // Populate films
            } catch (error) {
                console.error("Error fetching films:", error.response?.data || error.message);
                this.error = error.response?.data?.detail || "Failed to fetch films.";
                throw new Error(this.error);
            } finally {
                this.isLoading = false;
            }
        },

        async fetchFilters() {
            this.isLoading = true;
            this.error = null;

            try {
                const response = await axios.get("/movies/filters/");
                const {genres, decades, ratings} = response.data;

                this.genres = genres || [];
                this.decades = decades || [];
                this.ratings = ratings || [];
            } catch (error) {
                console.error("Error fetching filters:", error.response?.data || error.message);
                this.error = error.response?.data?.detail || "Failed to fetch filters.";
                throw new Error(this.error);
            } finally {
                this.isLoading = false;
            }
        },
    },
    getters: {
        hasFilms: (state) => state.films.length > 0,

        filteredFilmsByGenre: (state) => (genre) => {
            return state.films.filter((film) => film.genres.includes(genre));
        },

        filteredFilmsByDecade: (state) => (decade) => {
            const [startYear] = decade.match(/\d+/g).map(Number); // Extract starting year from "1990s"
            return state.films.filter(
                (film) => film.year >= startYear && film.year < startYear + 10
            );
        },

        filteredFilmsByRating: (state) => (minRating, maxRating) => {
            return state.films.filter(
                (film) => film.rating >= minRating && film.rating <= maxRating
            );
        },
    },
});