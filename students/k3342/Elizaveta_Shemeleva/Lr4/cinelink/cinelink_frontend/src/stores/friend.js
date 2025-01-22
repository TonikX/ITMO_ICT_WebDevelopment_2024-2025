import {defineStore} from "pinia";
import axios from "axios";

export const useFriendStore = defineStore("friend", {
    state: () => ({
        friend: null,
        favoriteMovies: [],
        isFriend: false,
        isLoading: false,
        error: null,
    }),

    actions: {
        async fetchFriendData(friendId) {
            this.isLoading = true;
            this.error = null;

            try {
                const response = await axios.get(`/friends/${friendId}/details/`);
                const {friend, favorite_movies, is_friend} = response.data;

                console.log("IS FRIEND", is_friend);

                this.friend = friend || null;
                this.favoriteMovies = favorite_movies || [];
                this.isFriend = is_friend || false;

                console.log("Friend data loaded:", this.friend, this.favoriteMovies, this.isFriend);
            } catch (error) {
                console.error("Error fetching friend data:", error);
                this.error = error.response?.data?.detail || "Failed to fetch friend details.";
                throw new Error(this.error);
            } finally {
                this.isLoading = false;
            }
        },

        async toggleFriendship(friendId) {
            this.isLoading = true;
            this.error = null;

            try {
                const response = await axios.post(`/friends/${friendId}/toggle/`);
                this.isFriend = !!response.data.is_friend; // Ensure boolean value
                console.log("Friendship status updated:", response.data.is_friend);
            } catch (error) {
                console.error("Error toggling friendship:", error);
                this.error = error.response?.data?.detail || "Failed to update friendship status.";
                throw new Error(this.error);
            } finally {
                this.isLoading = false;
            }
        },
    },

    getters: {
        favoriteMoviesCount: (state) => state.favoriteMovies.length,

        isFriendDataLoaded: (state) => !!state.friend,
    },
});