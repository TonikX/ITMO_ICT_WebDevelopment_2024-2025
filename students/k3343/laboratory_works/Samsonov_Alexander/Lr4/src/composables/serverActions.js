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

export const postComment = async (recipeId, rating, header, content) => {
    try {
        const response = await axiosInstance.post(`comments/?recipe_id=${recipeId}`,
            {"rating": rating, 'header': header, 'content_text': content},)
        console.log(response.data)
        return response.data
    } catch (error) {
        console.log(error)
        return null
    }
}

export const canEdit = async (recipeId) => {
    try {
        const response = await axiosInstance.get(`recipes/${recipeId}/canEdit/`, {},)
        return await response.data
    } catch (error) {
        return error.code === "ERR_BAD_REQUEST";
    }
}