import React from 'react';
import '../styles.css';

const Home = ({ onPageChange }) => {
    return (
        <div className="home-container">
            <h2>Bank User Authentication</h2>
            <button onClick={() => onPageChange('register')}>Register</button>
            <button onClick={() => onPageChange('login')}>Login with Face</button>
        </div>
    );
};

export default Home;
