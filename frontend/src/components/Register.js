import React, { useState } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';

const Register = ({ setCurrentPage }) => {
    const [name, setName] = useState('');
    const [accountNumber, setAccountNumber] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const webcamRef = React.useRef(null);

    const handleCaptureAndRegister = async () => {
        const imageSrc = webcamRef.current.getScreenshot();

        // Log the captured image for debugging
        console.log("Captured Image:", imageSrc); // Check if this logs a valid base64 string

        // Check if the image was captured
        if (!imageSrc) {
            setErrorMessage("Please capture an image.");
            return;
        }

        // Check if all fields are filled out
        if (!name.trim() || !accountNumber.trim()) {
            setErrorMessage("All fields must be filled out.");
            return;
        }

        try {
            // Sending data to the backend
            const response = await axios.post('http://127.0.0.1:5000/register', {
                name,
                image: imageSrc.split(',')[1], // Send base64 string without prefix
                account_number: accountNumber,
            });

            if (response.status === 201) {
                alert('Registered successfully! Please proceed to login.');
                setCurrentPage('login');
            }
        } catch (error) {
            console.error("Error registering user:", error);
            setErrorMessage("Registration failed. Please try again.");
            console.error("Response data:", error.response.data); // Log response data for more insight.
            console.error("Response status:", error.response.status); // Log response status.
            console.error("Response headers:", error.response.headers); // Log response headers.
        }
    };

    return (
        <div className="register-page">
            <h2>Register Your Account</h2>
            
            {/* Display error message */}
            {errorMessage && <p className="error-message">{errorMessage}</p>}

            <input
                type="text"
                placeholder="Enter your name"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />
            <input
                type="text"
                placeholder="Enter your account number"
                value={accountNumber}
                onChange={(e) => setAccountNumber(e.target.value)}
            />
            
            {/* Webcam Component */}
            <Webcam ref={webcamRef} screenshotFormat="image/jpeg" />
            <button onClick={handleCaptureAndRegister}>Capture Image and Register</button>
        </div>
    );
};

export default Register;