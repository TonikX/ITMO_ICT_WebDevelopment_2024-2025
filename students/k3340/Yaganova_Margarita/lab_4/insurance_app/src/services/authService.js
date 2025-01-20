import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export const login = async (username, password) => {
    try {
        axios.post(`${API_URL}/auth/token/login/`, {
            username,
            password,
        }).then(response => { console.log(response); localStorage.setItem('token', response.data.auth_token); });
    } catch (error) {
        console.error('Error during login:', error);
        throw error;
    }
};
