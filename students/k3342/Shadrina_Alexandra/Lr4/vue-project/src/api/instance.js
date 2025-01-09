import axios from 'axios'


const apiURL = 'http://127.0.0.1:8000'


const instance = axios.create({
 baseURL: apiURL
})

axios.interceptors.request.use((config) => {
  const token = localStorage.getItem("auth_token");
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});



export default instance
