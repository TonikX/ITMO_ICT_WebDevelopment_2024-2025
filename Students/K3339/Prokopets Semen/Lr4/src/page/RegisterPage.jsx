import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../utils/axiosConfig';
import { useToken } from '../stores/token';
import '../Css/RegisterPage.css';
const RegisterPage = () => {
    const [form, setForm] = useState({
        email: '',
        username: '',
        password: '',
        re_password: ''
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

    const register = async () => {
        try {
            const response = await axios.post('/auth/users/', {
                email: form.email,
                username: form.username,
                password: form.password,
                re_password: form.re_password
            });

            if (response.status === 201) {
                const token = await getToken(form.username, form.password);
                if (token) {
                    setToken(token);
                    navigate('/');
                }
            }
        } catch (error) {
            console.error('Ошибка регистрации:', error.response?.data || error.message);
        }
    };

    const getToken = async (username, password) => {
        try {
            const response = await axios.post('/auth/token/login/', { username, password });
            if (response.status === 200) return response.data.auth_token;
        } catch (error) {
            console.error('Ошибка получения токена:', error.response?.data || error.message);
            return null;
        }
    };

    const login = () => navigate('/login');
    return (
        <div className="register-container">
            <h2>Регистрация</h2>
            <input
                type="email"
                name="email"
                placeholder="Почта"
                value={form.email}
                onChange={handleChange}
                required
            />
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
            <input
                type="password"
                name="re_password"
                placeholder="Повторите пароль"
                value={form.re_password}
                onChange={handleChange}
                required
            />
            <div className="button-container">
                <button onClick={register}>Зарегистрироваться</button>
                <button onClick={login}>Войти</button>
            </div>
        </div>
    );
};

export default RegisterPage;
