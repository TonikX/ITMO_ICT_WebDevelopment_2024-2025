import axiosInstance from "@/services/axios.js";

export const fetchAndReturn = async (path, dataRef, loadingRef, errorRef) => {
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
