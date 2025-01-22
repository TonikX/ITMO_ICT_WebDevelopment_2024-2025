import axiosInstance from "@/services/axios.js";

export const fetchWithLoading = async (path, dataRef, loadingRef, errorRef) => {
    try {
        const response = await axiosInstance.get(path)
        dataRef.value = response.data
    } catch (error) {
        console.log(error)
        errorRef.value = error;
    } finally {
        loadingRef.value = false
    }
}

export async function CreateWorkout(workoutData) {
    const response = await axiosInstance.post('workouts/', workoutData)
    if (response.status === 201) {
        return response.data.id
    }
    return false
}