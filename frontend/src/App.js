// App.js
import React, { useState } from 'react';

import './styles.css';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import LandingPage from './components/LandingPage';
import Register from './components/Register';
import LoginWithFace from './components/LoginWithFace'; // Importing the correct component
import UserDashboard from './components/UserDashboard';

const App = () => {
    const [userId, setUserId] = useState(null);
    const [currentPage, setCurrentPage] = useState('landing');

    return (
        <div className="app-container">
            <Navbar />
            <div className="main-content">
                {currentPage === 'landing' && <LandingPage setCurrentPage={setCurrentPage} />}
                {currentPage === 'register' && <Register setCurrentPage={setCurrentPage} />}
                {currentPage === 'login' && <LoginWithFace setUserId={setUserId} />} {/* Use LoginWithFace */}
                {userId && <UserDashboard userId={userId} />}
            </div>
            <Footer />
        </div>
    );
};

export default App;