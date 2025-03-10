import api from "@/services/axios.ts";
import router from "@/router";

export interface workoutData {
    id: number;
    title: string;
    description: string;
    video_url: string;
    level: string;
    workout_type: string;
    duration_minutes: number;
    created_at: string;
}

export interface workoutCreateData{
    title: string;
    description: string;
    video_url: string;
    level: string;
    workout_type: string;
    duration_minutes: number;
}

export async function getAllWorkouts(args?: string) {
    try {
        const response = await api.get<workoutData[]>(`fitness/workouts/?${args}`);
        return response.data;
    } catch (error) {
        console.log(error);
        return []
    }
}

export async function getWorkout(id: string) {
    try {
        const response = await api.get<workoutData>(`fitness/workouts/${id}/`);
        return response.data;
    } catch (error) {
        console.log(error);
        return undefined
    }
}

export async function editWorkout(workout: workoutData) {
    try {
        const response = await api.patch<workoutData>(`/fitness/workouts/${workout.id}/`, workout);
        if (response.status === 200) {
            return true;
        }
    } catch (error) {
        console.error("Failed to update workout:", error);
        return false;
    }
}

export async function createWorkout(workout: workoutCreateData) {
    try {
        const response = await api.post<workoutData>("/fitness/workouts/", workout);
        if (response.status === 201) {
            alert("Workout created successfully!");
            router.push(`/workouts/${response.data.id}/`);
        }
    } catch (error) {
        console.error("Failed to create workout:", error);
        alert("Failed to create workout. Please try again.");
    }
}