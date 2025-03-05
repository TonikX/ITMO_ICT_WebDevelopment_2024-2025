import {ref, computed} from 'vue';
import axiosInstance from "@/services/AxiosService.ts";

export const authToken = ref(localStorage.getItem('authToken'));

export const isAuthenticated = computed(() => !!authToken.value);

export const setAuthToken = (token: string) => {
    authToken.value = token;
    localStorage.setItem('authToken', token);
};

export const logout = () => {
    authToken.value = null;
    localStorage.removeItem('authToken');
};

export async function login(username: string, password: string) {
    const response = await axiosInstance.post('/auth/token/login/', { username, password })
    setAuthToken(response.data.auth_token);
}