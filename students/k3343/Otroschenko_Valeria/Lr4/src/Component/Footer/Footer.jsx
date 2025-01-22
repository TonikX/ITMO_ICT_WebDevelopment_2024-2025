import React from "react";
import "./Footer.css";

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-left">
                <h3>Quick Links</h3>
                <ul>
                    <li><a href="/services">Services</a></li>
                    <li><a href="/patients">Patients</a></li>
                    <li><a href="/doctors">Doctors</a></li>
                    <li><a href="/medical-cards">Medical Cards</a></li>
                </ul>
            </div>
            <div className="footer-right">
                <div className="footer-about">
                    <h3>About Us</h3>
                    <p>We are committed to providing the best healthcare services with a team of experienced
                        professionals. Your health and comfort are our priorities.</p>
                </div>
                <div className="footer-contact">
                    <h3>Contact Us</h3>
                    <p>Email: info@clinic.com</p>
                    <p>Phone: +123 456 7890</p>
                    <p>Address: 123 Health Street, Wellness City</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;