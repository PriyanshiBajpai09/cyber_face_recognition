import React from 'react';

const UserDashboard = ({ userId }) => {
    return (
        <div className="dashboard-page">
            <h2>User Dashboard</h2>
            <p>Welcome, User {userId}</p>
            <p>Account Number: 1234567890</p>
            <p>Balance: $10,000</p>
            <p>Other Important Account Details...</p>
        </div>
    );
};

export default UserDashboard;
