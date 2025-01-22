import {defineStore} from 'pinia';
import axios from 'axios';
import {useAuthStore} from "@/stores/auth";

export const useFriendsStore = defineStore("friends", {
    state: () => ({
        friends: [],
        isLoading: false,
        error: null,
    }),
    actions: {
        async fetchFriends() {
            this.isLoading = true;
            this.error = null;

            try {
                const authStore = useAuthStore();

                if (!authStore.user || !authStore.user.id) {
                    throw new Error("User is not authenticated or user data is missing.");
                }

                const response = await axios.get(`/friends/${authStore.user.id}/list/`);

                this.friends = response.data;
            } catch (error) {
                console.error("Error fetching friends:", error.response?.data || error.message);
                this.error = error.response?.data?.detail || "Failed to fetch friends.";
            } finally {
                this.isLoading = false;
            }
        },
    },
    getters: {
        friendsCount: (state) => state.friends.length,
        hasFriends: (state) => state.friends.length > 0,
    },
});