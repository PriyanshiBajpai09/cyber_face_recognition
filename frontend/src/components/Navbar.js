import React from 'react';
import './Navbar.css';

const Navbar = () => (
    <nav className="navbar">
        <div className="navbar-logo">Bank Website</div>
        <ul className="navbar-menu">
            <li>Home</li>
            <li>Services</li>
            <li>About Us</li>
            <li>Contact</li>
        </ul>
    </nav>
);

export default Navbar;
