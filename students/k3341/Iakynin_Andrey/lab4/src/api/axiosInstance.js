import axios from 'axios';


const getAuthToken = () => localStorage.getItem("authToken");


const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
    headers: {
        'Authorization': `Token ${getAuthToken()}`,
    },
});


export default axiosInstance;
