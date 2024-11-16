from flask import Blueprint, request, jsonify
import sqlite3
import os
import cv2
import numpy as np
import base64
from utils.face_utils import detect_face, compare_faces

user_routes = Blueprint('user_routes', __name__)

DATABASE = 'users.db'

@user_routes.route('/register', methods=['POST'])
def register_user():
    try:
        name = request.json.get('name')
        image_data = request.json.get('image')
        account_number = request.json.get('account_number')
        balance = request.json.get('balance')

        if not all([name, image_data, account_number, balance]):
            return jsonify({'message': 'All fields are required!'}), 400

        # Save user image
        user_image_path = os.path.join('static/images', f'{name}.jpg')
        os.makedirs(os.path.dirname(user_image_path), exist_ok=True)

        try:
            decoded_image = base64.b64decode(image_data)
            with open(user_image_path, 'wb') as f:
                f.write(decoded_image)
        except Exception as img_error:
            return jsonify({'message': f'Image save error: {img_error}'}), 500

        # Store user details in the database
        try:
            with sqlite3.connect(DATABASE) as conn:
                conn.execute(
                    'INSERT INTO users (name, image_path, account_number, balance) VALUES (?, ?, ?, ?)',
                    (name, user_image_path, account_number, float(balance))
                )
                conn.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except Exception as db_error:
            return jsonify({'message': f'Database error: {db_error}'}), 500

    except Exception as e:
        return jsonify({'message': f'Unexpected error: {e}'}), 500

@user_routes.route('/login', methods=['POST'])
def login_user():
    try:
        image_data = request.json.get('image_data')

        # Decode the image data
        np_image = np.frombuffer(base64.b64decode(image_data), np.uint8)
        img = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

        # Detect face
        detected_face = detect_face(img)

        if detected_face is None:
            return jsonify({'message': 'No face detected. Please try again.'}), 400

        # Compare faces with stored user images
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.execute('SELECT name, image_path FROM users')
            for user_name, user_image_path in cursor.fetchall():
                stored_image = cv2.imread(user_image_path)
                stored_face = detect_face(stored_image)

                if stored_face is not None and compare_faces(detected_face, stored_face):
                    return jsonify({'message': f'Login successful! Welcome {user_name}.'}), 200

        return jsonify({'message': 'Login failed. Face not recognized.'}), 401

    except Exception as e:
        return jsonify({'message': f'Unexpected error: {e}'}), 500
