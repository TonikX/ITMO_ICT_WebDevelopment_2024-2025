import {defineStore} from "pinia";
import axios from "axios";

export const useFriendsActivityStore = defineStore("friendsActivity", {
    state: () => ({
        activities: [],
        isLoading: false,
        error: null,
    }),
    actions: {
        async loadFriendsActivity() {
            this.isLoading = true;
            this.error = null;

            try {
                const response = await axios.get("/friends-activity/");
                this.activities = response.data; // Directly use the API response as the activities
            } catch (error) {
                console.error("Error fetching friends' activity:", error.response?.data || error.message);
                this.error = error.response?.data?.detail || "Failed to fetch friends' activity.";
            } finally {
                this.isLoading = false;
            }
        },
    },
});