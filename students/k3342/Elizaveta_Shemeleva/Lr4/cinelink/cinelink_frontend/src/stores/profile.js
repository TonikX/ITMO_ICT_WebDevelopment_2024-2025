import {defineStore} from "pinia";
import axios from "axios";

export const useProfileStore = defineStore("profile", {
    state: () => ({
        username: "",
        avatar_url: "",
        favorites: [],
        topMovies: [],
        userLists: [],
    }),

    actions: {
        handleError(error, context) {
            const message = error.response?.data?.detail || error.message || "An unknown error occurred.";
            console.error(`Error in ${context}:`, message);
            throw new Error(message);
        },

        async loadProfile() {
            try {
                const response = await axios.get("/profile/");
                this.username = response.data.username || "Default User";
                // this.avatar_url = response.data.avatar_url || "";
                this.avatar = response.data.avatar || ""; // Fetch and store avatar
                this.favorites = response.data.favorites || [];
                // console.log(this.favorites);
                console.log("Profile loaded successfully:", response.data);
            } catch (error) {
                this.handleError(error, "loading profile");
            }
        },

        async loadTopMovies() {
            if (!this.favorites.length) {
                console.log("No favorites available to load.");
                this.topMovies = [];
                return;
            }

            try {
                const movieRequests = this.favorites.map((id) =>
                    axios.get(`/movies/${id}/`)
                );

                const movieResponses = await Promise.allSettled(movieRequests);

                this.topMovies = movieResponses
                    .filter((res) => res.status === "fulfilled")
                    .map((res) => res.value.data)
                    .slice(0, 5); // Limit to top 5 movies

                console.log("Top movies loaded successfully:", this.topMovies);
            } catch (error) {
                this.handleError(error, "loading top movies");
            }
        },

        async loadUserLists() {
            try {
                const response = await axios.get("/lists/");
                this.userLists = response.data || [];
                console.log("User lists loaded successfully:", this.userLists);
            } catch (error) {
                this.handleError(error, "loading user lists");
            }
        },

        async addNewList(name) {
            if (!name.trim()) {
                throw new Error("List name cannot be empty.");
            }

            try {
                const response = await axios.post("/lists/", {name});
                this.userLists.push(response.data);
                console.log("New list added successfully:", response.data);
            } catch (error) {
                this.handleError(error, "adding a new list");
            }
        },

        async saveProfile(profileData) {
            const payload = {
                username: profileData.username,
                avatar_url: profileData.avatar_url,
                favorites: profileData.favorites
                    .split(",")
                    .map((fav) => fav.trim())
                    .filter(Boolean),
            };

            try {
                await axios.put("/profile/", payload);
                this.username = profileData.username;
                this.avatar_url = profileData.avatar_url;
                this.favorites = payload.favorites;
                console.log("Profile updated successfully:", payload);
            } catch (error) {
                this.handleError(error, "updating profile");
            }
        },
    },
});