import React, { useState, useEffect } from "react";
import "./Header.css";
import { Link, useNavigate } from "react-router-dom";

const Header = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [username, setUsername] = useState("");
    const navigate = useNavigate();

    // Проверяем, авторизован ли пользователь
    useEffect(() => {
        const token = localStorage.getItem("authToken");
        if (token) {
            setIsAuthenticated(true);
            const user = localStorage.getItem("username");
            if (user) {
                setUsername(user);
            }
        }
    }, []);

    // Логика выхода из системы
    const handleLogout = () => {
        localStorage.removeItem("authToken");
        localStorage.removeItem("username");
        setIsAuthenticated(false);
        setUsername("");
        navigate("/"); // Перенаправляем на главную страницу
    };

    return (
        <header className="header">
            <div className="logo">
                <Link to="/">
                    <span className="logo-icon">🏠</span> Medical Clinic
                </Link>
            </div>
            <nav>
                <ul className="nav-links">
                    {isAuthenticated && (
                        <>
                            <li><Link to="/medical-cards">Medical Cards</Link></li>
                            <li><Link to="/patients">Patients</Link></li>
                            <li><Link to="/appointments">Appointments</Link></li> {/* Переход на страницу Appointment */}
                            <li><Link to="/doctors">Doctors</Link></li>
                        </>
                    )}
                </ul>
            </nav>
            <div className="auth-buttons">
                {!isAuthenticated ? (
                    <>
                        <Link to="/signup" className="signup">Sign Up</Link>
                        <Link to="/login" className="login">
                            <span className="user-icon">👤</span> Log In
                        </Link>
                    </>
                ) : (
                    <>
                        <span className="username">{username}</span>
                        <button className="exit" onClick={handleLogout}>Exit</button>
                    </>
                )}
            </div>
        </header>
    );
};

export default Header;
