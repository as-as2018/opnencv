import cv2
import numpy as np
import os

# Load Recognizer
model_file = "face_detection/face_recognizer.yml"
if not os.path.exists(model_file):
    print(f"Error: Recognizer file '{model_file}' not found. Please run the training script first.")
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(model_file)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Start video capture
camera = cv2.VideoCapture(0)

print("Starting face recognition. Press 'q' to quit.")

while True:
    ret, frame = camera.read()
    if not ret:
        print("Failed to capture image. Exiting...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

    for (x, y, w, h) in faces:
        face = gray[y:y + h, x:x + w]
        label, confidence = recognizer.predict(face)

        if confidence < 50:  # Lower value = higher confidence
            text = f"User {label} ({confidence:.2f}%)"
            color = (0, 255, 0)
        else:
            text = "Unknown"
            color = (0, 0, 255)

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
print("Face recognition ended.")
