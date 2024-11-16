import os
import cv2
import numpy as np
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = 'users.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                image_path TEXT NOT NULL,
                account_number TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Bank Website API!'}), 200

@app.route('/register', methods=['POST'])
def register_user():
    try:
        name = request.json['name']
        image_data = request.json['image']  # Base64 image string
        account_number = request.json['account_number']

        if not all([name, image_data, account_number]):
            return jsonify({'message': 'All fields are required!'}), 400

        # Save the user image locally
        user_image_path = os.path.join('static/images', f'{name}.jpg')

        os.makedirs(os.path.dirname(user_image_path), exist_ok=True)

        with open(user_image_path, 'wb') as f:
            f.write(base64.b64decode(image_data))

        with sqlite3.connect(DATABASE) as conn:
            conn.execute('INSERT INTO users (name, image_path, account_number) VALUES (?, ?, ?)', 
                         (name, user_image_path, account_number))
            conn.commit()

        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'message': 'Registration failed. Please try again.'}), 500

@app.route('/login', methods=['POST'])
def login_user():
    try:
        image_data = request.json['image_data']  # Base64 image string
        
        # Debug: Log the size of the incoming image data
        print(f"Received image data of size: {len(image_data)}")

        # Decode the image data from base64
        np_image = np.frombuffer(base64.b64decode(image_data), np.uint8)
        img = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

        # Ensure image was loaded
        if img is None:
            print("Failed to load image")
            return jsonify({'message': 'Failed to load image'}), 400

        # Load Haar Cascade for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Debug: Log the number of faces detected
        print(f"Detected faces: {len(faces)}")

        if len(faces) == 0:
            return jsonify({'message': 'No face detected!'}), 400

        x, y, w, h = faces[0]
        detected_face = img[y:y+h, x:x+w]

        # Initialize the LBPH face recognizer
        recognizer = cv2.face_LBPHFaceRecognizer_create()

        if os.path.exists('face_model.xml'):
            recognizer.read('face_model.xml')
        else:
            recognizer = cv2.face_LBPHFaceRecognizer_create()

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.execute('SELECT name, image_path FROM users')
            for row in cursor.fetchall():
                user_name, user_image_path = row
                stored_image = cv2.imread(user_image_path)
                stored_image_gray = cv2.cvtColor(stored_image, cv2.COLOR_BGR2GRAY)

                stored_faces = face_cascade.detectMultiScale(stored_image_gray)
                if len(stored_faces) > 0:
                    sx, sy, sw, sh = stored_faces[0]
                    stored_face = stored_image[sy:sy+sh, sx:sx+sw]

                    # Train the recognizer with the stored face image
                    label = 0  # Assuming label 0 for all faces
                    recognizer.update([stored_face], np.array([label]))

                    # Debug: Log training process
                    print(f"Trained recognizer with {user_name}'s face")

                    # Predict the label of the detected face
                    label, confidence = recognizer.predict(detected_face)
                    print(f"Prediction - Label: {label}, Confidence: {confidence}")

                    if confidence < 100:
                        recognizer.save('face_model.xml')
                        return jsonify({'message': f'Login successful! Welcome {user_name}.'}), 200

        return jsonify({'message': 'Login failed. Face not recognized.'}), 401

    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'message': 'An error occurred. Please try again.'}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
