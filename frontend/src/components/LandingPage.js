import React from 'react';
// import './LandingPage.css';

const LandingPage = ({ setCurrentPage }) => {
    return (
        <div className="landing-page">
            <h2>Welcome to Our Bank</h2>
            <p>Choose an option to continue:</p>
            <div className="button-group">
                <button onClick={() => setCurrentPage('register')}>Register with Face</button>
                <button onClick={() => setCurrentPage('login')}>Login with Face</button>
            </div>
        </div>
    );
};

export default LandingPage;
