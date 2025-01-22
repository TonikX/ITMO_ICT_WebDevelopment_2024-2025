import React from 'react';
import './Footer.css';

function Footer() {
    return (
        <footer className="footer">
            <div className="footer-content">
                <p>&copy; 2025 Страховая Система. Все права защищены.</p>
                <div className="footer-links">
                    <a href="/about">О нас</a>
                    <a href="/contact">Контакты</a>
                    <a href="/privacy">Политика конфиденциальности</a>
                </div>
            </div>
        </footer>
    );
}

export default Footer;
