import cv2
import mediapipe as mp
import serial
import time
import numpy as np

# Initialize serial communication with Arduino
arduino = serial.Serial('COM5', 9600, timeout=1)  # Replace COM6 with your actual port
time.sleep(2)  # Wait for the connection to initialize

# EAR calculation function
def calculate_ear(eye):
    A = np.linalg.norm(eye[1] - eye[5])  # Vertical distance 1
    B = np.linalg.norm(eye[2] - eye[4])  # Vertical distance 2
    C = np.linalg.norm(eye[0] - eye[3])  # Horizontal distance
    ear = (A + B) / (2.0 * C)
    return ear

# Mediapipe face mesh setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)
EAR_THRESHOLD = 0.2  # Adjust based on your testing
CONSECUTIVE_FRAMES = 3

# Indices for the eyes (based on Mediapipe's face mesh landmarks)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

blink_count = 0
frame_counter = 0

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB for Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = np.array([[lm.x, lm.y] for lm in face_landmarks.landmark])

            # Get eye landmarks
            left_eye = landmarks[LEFT_EYE]
            right_eye = landmarks[RIGHT_EYE]

            # Convert normalized coordinates to pixel values
            h, w, _ = frame.shape
            left_eye = np.array([(int(x * w), int(y * h)) for x, y in left_eye])
            right_eye = np.array([(int(x * w), int(y * h)) for x, y in right_eye])

            # Calculate EAR
            left_ear = calculate_ear(left_eye)
            right_ear = calculate_ear(right_eye)
            avg_ear = (left_ear + right_ear) / 2.0

            # Blink detection logic
            if avg_ear < EAR_THRESHOLD:
                frame_counter += 1
            else:
                if frame_counter >= CONSECUTIVE_FRAMES:
                    blink_count += 1
                    print(f"Blink detected! Total: {blink_count}")
                    arduino.write(b'1')  # Send '1' to turn on LED
                    time.sleep(2)  # Keep LED on for a moment
                    arduino.write(b'0')  # Send '0' to turn off LED
                frame_counter = 0

            # Draw eye contours
            cv2.polylines(frame, [left_eye], True, (0, 255, 0), 1)
            cv2.polylines(frame, [right_eye], True, (0, 255, 0), 1)

    cv2.imshow('Eye Blink Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
arduino.close()
