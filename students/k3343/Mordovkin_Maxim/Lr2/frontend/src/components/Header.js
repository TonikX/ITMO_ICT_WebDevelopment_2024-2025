import React from 'react';
import './css/Header.css';

export function Header() {
    const handleLogout = () => {
        localStorage.removeItem('token');
        window.location.href = '/';
    };

    return (
        <header className="app-header">
            <div className="header-content">
                <h1>Лабораторная работа 2. Домашние задания</h1>
                <button onClick={handleLogout} className="logout-button">
                    Выйти
                </button>
            </div>
        </header>
    );
}