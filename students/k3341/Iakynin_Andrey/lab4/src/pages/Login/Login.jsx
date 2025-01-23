import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./Login.css";

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError("");
        setSuccess("");

        try {
            const response = await axios.post("http://127.0.0.1:8000/api/auth/token/login", {
                username,
                password,
            });

            const token = response.data.auth_token;

            // Сохраняем токен и имя пользователя в localStorage
            localStorage.setItem("authToken", token);
            localStorage.setItem("username", username);

            setSuccess("Login successful!");

            // Перенаправляем на главную страницу
            navigate("/");
        } catch (err) {
            setError("Invalid username or password.");
        }
    };

    return (
        <div className="login-container">
            <form className="login-form" onSubmit={handleLogin}>
                <h2>Login</h2>
                {error && <p className="error-message">{error}</p>}
                {success && <p className="success-message">{success}</p>}

                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Enter your username"
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter your password"
                        required
                    />
                </div>

                <button type="submit" className="btn-login">
                    Login
                </button>
            </form>
        </div>
    );
};

export default Login;
