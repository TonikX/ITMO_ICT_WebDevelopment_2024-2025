import React, { useState } from 'react';

const Login = () => {
    const [username, setUsername] = useState('Andrucrut42');
    const [password, setPassword] = useState('Misha1221');
    const [token, setToken] = useState(null);
    const [error, setError] = useState(null);

    const handleLogin = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/auth/token/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username,
                    password,
                }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            setToken(data.token); // Предполагается, что сервер возвращает токен в поле `token`
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div>
            <h1>Login</h1>
            <button onClick={handleLogin}>Login</button>
            {token && <div>Token: {token}</div>}
            {error && <div>Error: {error}</div>}
        </div>
    );
};

export default Login;
