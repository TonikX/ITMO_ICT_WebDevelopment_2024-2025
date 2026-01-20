import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from './api';
import './Auth.css';

function Auth() {
    const [isLogin, setIsLogin] = useState(true);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const endpoint = isLogin ? '/auth/token/login/' : '/auth/users/';

        const data = isLogin
            ? { username, password }
            : { username, password, email };

        try {
            const response = await api.post(endpoint, data);
            if (isLogin) {
                const token = response.data.auth_token;
                localStorage.setItem('authToken', token);
                api.defaults.headers.common['Authorization'] = `Token ${token}`;
                navigate('/collective-contracts');
            } else {
                alert('Registration successful!');
            }
        } catch (error) {
            console.error('Error:', error.response ? error.response.data : error.message);
            alert('An error occurred. Please try again.');
        }
    };

    const toggleAuthMode = () => {
        setIsLogin(!isLogin);
        setEmail('');
    };

    return (
        <div className="auth-container">
            <form className="auth-form" onSubmit={handleSubmit}>
                <h2>{isLogin ? 'Login' : 'Register'}</h2>
                <div className="form-group">
                    <label>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                {!isLogin && (
                    <div className="form-group">
                        <label>Email:</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                )}
                <div className="form-group">
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="auth-button">
                    {isLogin ? 'Login' : 'Register'}
                </button>
                <button type="button" className="toggle-button" onClick={toggleAuthMode}>
                    {isLogin ? 'Switch to Register' : 'Switch to Login'}
                </button>
            </form>

        </div>
    );
}

export default Auth;
