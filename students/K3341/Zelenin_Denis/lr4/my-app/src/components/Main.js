import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from './api';
import './Main.css';

function MainMenu() {
    const [showLogoutPanel, setShowLogoutPanel] = useState(false);
    const navigate = useNavigate();

    const handleLogout = () => {
        api.post('/auth/token/logout/')
            .then(() => {
                localStorage.removeItem('authToken');
                navigate('/');
            })
            .catch(error => console.error('Error during logout:', error));
    };

    return (
        <nav className="main-menu">
            <ul>
                <li><Link to="/agents">Агенты</Link></li>
                <li><Link to="/collective-contracts">Контракты</Link></li>
                <li><Link to="/organizations">Организации</Link></li>
                <li><Link to="/insurance-cases">Страховые случаи</Link></li>
                <li><Link to="/employees">Работники</Link></li>
                <li>
                    <button className="logout-button" onClick={() => setShowLogoutPanel(!showLogoutPanel)}>
                        Выйти
                    </button>
                    {showLogoutPanel && (
                        <div className="logout-panel">
                            <button onClick={handleLogout}>Подтвердить выход</button>
                        </div>
                    )}
                </li>
            </ul>
        </nav>
    );
}

export default MainMenu;
