import React, { useState, useEffect } from 'react';

import InteractiveBackground from './InteractiveBackground';
import { Header } from './Header';
import './css/MainPage.css';

function MainPage() {

    const API_URL = 'http://localhost:8080/backend_war/api';

    return (
        <div className="main-page">
            <InteractiveBackground />
            <div className="main-content">
                <Header />
                <div className="content-grid">

                </div>
            </div>
        </div>
    );
}

export default MainPage;