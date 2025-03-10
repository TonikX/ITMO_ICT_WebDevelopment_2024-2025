import api from "@/services/axios.ts";

export interface ProgressEntry {
    date: string;
    weight: number;
    notes: string;
}


export async function getProgress(): Promise<ProgressEntry[]> {
    try {
        const response = await api.get<ProgressEntry[]>("/fitness/progress/");
        return response.data;
    } catch (error) {
        console.error("Failed to fetch progress entries:", error);
        return []
    }
}

export async function postProgress (newProgress: ProgressEntry) {
    try {
        const response = await api.post("/fitness/progress/", newProgress);
        if (response.status === 201) {
            alert("Progress entry added successfully!");
        }
    } catch (error) {
        console.error("Failed to add progress entry:", error);
        alert("Failed to add progress entry. Please try again.");
        throw error;
    }
}