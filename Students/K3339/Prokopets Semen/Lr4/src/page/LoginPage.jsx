import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useToken } from '../stores/token';
import axios from '../utils/axiosConfig';
import '../Css/LoginPage.css';
const LoginPage = () => {
    const [form, setForm] = useState({
        username: '',
        password: ''
    });
    const { setToken } = useToken();
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm({
            ...form,
            [name]: value
        });
    };

    const login = async () => {
        console.log('Login button clicked');
        console.log('Form data:', form);
        try {
            const response = await axios.post('api/auth/token/login/', form);
            if (response.status === 200) {
                setToken(response.data.auth_token);
                navigate('/');
            }
        } catch (error) {
            console.error('Ошибка входа:', error.response?.data || error.message);
        }
    };

    const register = () => {
        navigate('/register');
    };

    return (
        <div className="login-container">
            <h2>Вход</h2>
            <input
                type="text"
                name="username"
                placeholder="Логин"
                value={form.username}
                onChange={handleChange}
                required
            />
            <input
                type="password"
                name="password"
                placeholder="Пароль"
                value={form.password}
                onChange={handleChange}
                required
            />
            <div className="button-container">
                <button onClick={login}>Войти</button>
                <button onClick={register}>Зарегистрироваться</button>
            </div>
        </div>
    );
};

export default LoginPage;
