import { ref } from 'vue';
import axiosInstance from "@/services/axios.js";

export const isHR = ref(null);
export const company = ref(null);

export const update = async () => {
  try {
    const response = await axiosInstance.get('isHR/');
    isHR.value = response.data[0];
    company.value = response.data[1];
  } catch (error) {
    console.error('Error fetching isHR flag:', error);
  }
};

await update();