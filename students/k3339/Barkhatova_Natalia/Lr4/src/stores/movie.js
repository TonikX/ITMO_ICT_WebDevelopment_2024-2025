// src/stores/movie.js
import {defineStore} from 'pinia';
import api from "@/api/api.js";

export const useMovieStore = defineStore({
    id: 'movie',
    state: () => ({
        movies: [],
    }),
    actions: {
        async fetchMovies() {
            try {
                const response = await api.get('/rest/movies');
                this.movies = response.data;
            } catch (error) {
                console.error('Failed to fetch movies:', error.response.data);
            }
        },

        async addMovie(movie) {
            const response = await api.post('/rest/admin/movies', movie);
            this.movies.push(response.data);
        },

        async updateMovie(movie) {
            const response = await api.put(`/rest/admin/movies/${movie.id}`, movie);
            const index = this.movies.findIndex((m) => m.id === movie.id);
            this.movies[index] = response.data;
        },

        async deleteMovie(movieId) {
            try {
                await api.delete('/rest/admin/movies', { data: { id: movieId } });
                this.movies = this.movies.filter((movie) => movie.id !== movieId);
            } catch (error) {
                console.error('Failed to delete movie:', error.response.data);
            }
        }
    },
});
