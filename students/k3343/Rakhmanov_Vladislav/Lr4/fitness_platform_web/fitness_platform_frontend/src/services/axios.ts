import axios from "axios";
import {TokenRef} from "@/composables/tokenActions.ts";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000/",
    timeout: 5000,
    headers: {
        "Content-Type": "application/json",
    },
});


api.interceptors.request.use(
    (config) => {
        const token = TokenRef.value;
        if (token && token !== "undefined") {
            config.headers.Authorization = `Token ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);


api.interceptors.response.use(
    (response) => response,
    (error) => {
        console.log(error);
        if (error.response && error.response.status === 401) {
            console.error("Unauthorized!");
        }
        return Promise.reject(error);
    }
);

export default api;
