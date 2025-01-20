// src/components/Header.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../images/logo.png';
import '../Css/Header.css'; // Импортируем стили

const Header = () => {
    return (
        <header className="d-flex justify-content-between align-items-center p-3">
            <div className="logo">
                <img src={logo} alt="Логотип" />
            </div>
            <nav>
                <ul className="d-flex list-unstyled mb-0">
                    <li className="mx-3">
                        <Link to="/bus" className="btn btn-link">Bus</Link>
                    </li>
                    <li className="mx-3">
                        <Link to="/bustype" className="btn btn-link">BusType</Link>
                    </li>
                    <li className="mx-3">
                        <Link to="/driver" className="btn btn-link">Driver</Link>
                    </li>
                    <li className="mx-3">
                        <Link to="/route" className="btn btn-link">Route</Link>
                    </li>
                    <li className="mx-3">
                        <Link to="/work-shifts" className="btn btn-link">Work Shifts</Link>
                    </li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;
