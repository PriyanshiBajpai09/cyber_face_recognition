import cv2
import numpy as np

# Detect face using OpenCV's Haar cascade classifier
def detect_face(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        return None

    x, y, w, h = faces[0]
    return gray[y:y + h, x:x + w]

# Compare two faces using normalized cross-correlation
def compare_faces(face1, face2):
    try:
        return cv2.matchTemplate(face1, face2, cv2.TM_CCOEFF_NORMED)[0][0] > 0.8
    except Exception as e:
        print(f"Comparison error: {e}")
        return False
