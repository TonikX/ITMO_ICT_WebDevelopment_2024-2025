import React from "react";
import "./Footer.css";

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-left">
                <form>
                    <div className="form-group">
                        <label htmlFor="name">First Name:</label>
                        <input type="text" id="name" placeholder="Your first name*" />
                    </div>
                    <div className="form-group">
                        <label htmlFor="lastName">Last Name:</label>
                        <input type="text" id="lastName" placeholder="Your last name*" />
                    </div>
                    <div className="form-group">
                        <label htmlFor="email">Email Address:</label>
                        <input type="email" id="email" placeholder="Your email address*" />
                    </div>
                    <div className="form-group">
                        <label htmlFor="contact">Contact:</label>
                        <input type="text" id="contact" placeholder="Your phone number*" />
                    </div>
                </form>
            </div>
            <div className="footer-right">
                <h3>Opening Hours</h3>
                <div className="hours">
                    <p>Monday - Friday: 8:00 AM - 5:00 PM</p>
                    <p>Saturday - Sunday: 8:00 AM - 3:00 PM</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
