import cv2
import mediapipe as mp
import serial
import time
import numpy as np

# Initialize Serial communication with Arduino
try:
    ser = serial.Serial('COM5', 9600)  # Replace COM5 with your Arduino port
    time.sleep(2)  # Wait for Serial connection to establish
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

# Mediapipe face mesh setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

# Indices for the eyes (based on Mediapipe's face mesh landmarks)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# Tracking variables
movement_threshold = 3  # Reduced threshold for more sensitivity
look_left = False
look_right = False
last_left_eye_center = None
last_right_eye_center = None
command_sent_time = time.time()
command_interval = 0.1  # Small delay to avoid flooding serial port

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB for Mediapipe
    frame = cv2.flip(frame, 1)  # Mirror effect
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = np.array([[lm.x, lm.y] for lm in face_landmarks.landmark])

            # Get eye landmarks
            h, w, _ = frame.shape
            left_eye = np.array([(int(landmarks[i][0] * w), int(landmarks[i][1] * h)) for i in LEFT_EYE])
            right_eye = np.array([(int(landmarks[i][0] * w), int(landmarks[i][1] * h)) for i in RIGHT_EYE])

            # Calculate the centroid of each eye
            left_eye_center = np.mean(left_eye, axis=0).astype("int")
            right_eye_center = np.mean(right_eye, axis=0).astype("int")

            # Movement detection logic
            if last_left_eye_center is not None and last_right_eye_center is not None:
                # Calculate horizontal movement (x-axis difference)
                left_movement_x = left_eye_center[0] - last_left_eye_center[0]
                right_movement_x = right_eye_center[0] - last_right_eye_center[0]

                current_time = time.time()

                # Detect movement direction and maintain state
                if left_movement_x < -movement_threshold and right_movement_x < -movement_threshold:
                    look_left = True
                    look_right = False
                    if current_time - command_sent_time >= command_interval:
                        print(f"Looking Left! Turning on LEFT LED. {left_movement_x}")
                        try:
                            ser.write(b'L')  # Send 'L' to turn on left LED
                            command_sent_time = current_time
                        except serial.SerialException as e:
                            print(f"Error writing to serial port: {e}")
                elif left_movement_x > movement_threshold and right_movement_x > movement_threshold:
                    look_right = True
                    look_left = False
                    if current_time - command_sent_time >= command_interval:
                        print(f"Looking Right! Turning on RIGHT LED. {right_movement_x}")
                        try:
                            ser.write(b'R')  # Send 'R' to turn on right LED
                            command_sent_time = current_time
                        except serial.SerialException as e:
                            print(f"Error writing to serial port: {e}")
                elif not look_left and not look_right:
                    if current_time - command_sent_time >= command_interval:
                        try:
                            ser.write(b'O')  # Turn off both LEDs
                            command_sent_time = current_time
                        except serial.SerialException as e:
                            print(f"Error writing to serial port: {e}")
                # Maintain the 'looking' state even if there's no significant movement in the current frame
                elif look_left and abs(left_movement_x) <= movement_threshold and abs(right_movement_x) <= movement_threshold:
                    if current_time - command_sent_time >= command_interval:
                        try:
                            ser.write(b'L')
                            command_sent_time = current_time
                        except serial.SerialException as e:
                            print(f"Error writing to serial port: {e}")
                elif look_right and abs(left_movement_x) <= movement_threshold and abs(right_movement_x) <= movement_threshold:
                    if current_time - command_sent_time >= command_interval:
                        try:
                            ser.write(b'R')
                            command_sent_time = current_time
                        except serial.SerialException as e:
                            print(f"Error writing to serial port: {e}")
                elif abs(left_movement_x) <= movement_threshold and abs(right_movement_x) <= movement_threshold:
                    look_left = False
                    look_right = False
                    if current_time - command_sent_time >= command_interval:
                        try:
                            ser.write(b'O')
                            command_sent_time = current_time
                        except serial.SerialException as e:
                            print(f"Error writing to serial port: {e}")


            # Update last positions
            last_left_eye_center = left_eye_center
            last_right_eye_center = right_eye_center

            # Draw eye contours and centers
            cv2.polylines(frame, [left_eye], True, (0, 255, 0), 1)
            cv2.polylines(frame, [right_eye], True, (0, 255, 0), 1)
            cv2.circle(frame, tuple(left_eye_center), 3, (255, 0, 0), -1)
            cv2.circle(frame, tuple(right_eye_center), 3, (255, 0, 0), -1)

    cv2.imshow('Eye Movement Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
if 'ser' in locals() and ser.is_open:
    ser.close()