import axios from "axios";

const instance = axios.create({
    baseURL: 'http://127.0.0.1:9000',
    timeout: 5000,
    // headers: {
        //     "Authorization": "Token 4bb98782c004a9d5e54fec9432120144dade3a56"
        // },
});

export default instance