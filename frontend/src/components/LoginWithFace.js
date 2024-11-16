import React, { useRef } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';

const LoginWithFace = ({ setUserId }) => {
    const webcamRef = useRef(null);

    const handleLogin = async () => {
        const imageSrc = webcamRef.current.getScreenshot();

        // Log the captured image for debugging
        console.log("Captured Image for Login:", imageSrc); // Check if this logs a valid base64 string

        if (!imageSrc) {
            alert("Please capture an image.");
            return;
        }

        try {
            const response = await axios.post('http://127.0.0.1:5000/login', { 
                image_data: imageSrc.split(',')[1] // Send base64 string without prefix
            });
            alert(response.data.message);
            if (response.data.message.includes('successful')) {
                setUserId(1); // Replace with actual user ID logic if available.
            }
        } catch (error) {
            console.error("Error logging in:", error);
            alert("Login failed.");
        }
    };

    return (
        <div className="login-container">
            <h2>Login with Face</h2>
            <Webcam ref={webcamRef} screenshotFormat="image/jpeg" />
            <button onClick={handleLogin}>Capture Face to Login</button>
        </div>
    );
};

export default LoginWithFace;