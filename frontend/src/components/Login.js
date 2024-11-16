import React, { useState, useRef } from 'react';
import axios from 'axios';

const Login = ({ setUserId }) => {
    const [image, setImage] = useState(null);
    const [loginMessage, setLoginMessage] = useState('');
    const videoRef = useRef(null);
    const canvasRef = useRef(null);

    // Start webcam when the component mounts
    const startWebcam = () => {
        navigator.mediaDevices
            .getUserMedia({ video: true })
            .then((stream) => {
                videoRef.current.srcObject = stream;
            })
            .catch((err) => {
                console.error('Error accessing webcam:', err);
            });
    };

    // Capture image from the webcam and convert to base64
    const captureImage = () => {
        const canvas = canvasRef.current;
        const video = videoRef.current;

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);

        // Convert the image to base64
        const base64Image = canvas.toDataURL('image/jpeg');
        setImage(base64Image);
    };

    // Handle the login process by sending the captured image to the backend
    const handleLogin = async () => {
        if (!image) {
            setLoginMessage('Please capture your face first!');
            return;
        }

        try {
            // Send the captured base64 image to the backend for face recognition
            const response = await axios.post('http://localhost:5000/login', {
                image_data: image.split(',')[1], // Remove data URL prefix
            });

            // Handle the response from the backend
            if (response.status === 200) {
                const userId = response.data.user_id; // Assuming the backend sends a user ID upon successful login
                setUserId(userId);
                setLoginMessage(`Login successful! Welcome ${response.data.name}.`);
            } else {
                setLoginMessage('Login failed. Face not recognized.');
            }
        } catch (error) {
            console.error('Error during login:', error);
            setLoginMessage('Login failed. Please try again.');
        }
    };

    return (
        <div className="login-page">
            <h2>Login with Face</h2>
            <div>
                <video ref={videoRef} autoPlay width="320" height="240" />
                <canvas ref={canvasRef} style={{ display: 'none' }} />
            </div>
            <button onClick={startWebcam}>Start Webcam</button>
            <button onClick={captureImage}>Capture Face</button>
            <button onClick={handleLogin}>Login</button>
            <p>{loginMessage}</p>
        </div>
    );
};

export default Login;
