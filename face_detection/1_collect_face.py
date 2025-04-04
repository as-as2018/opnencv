import cv2
import os

# Initialize camera and face detector
camera = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Dataset directory
dataset_path = "face_detection/face_dataset"
os.makedirs(dataset_path, exist_ok=True)

# Get user details
user_id = input("Enter your ID (numeric): ")
user_name = input("Enter your name: ")

# Angles required for face collection
angles = ["Front", "Left", "Right", "Up", "Down"]
captured_faces = []

print("\nFollow the instructions to capture your face from different angles.")

for angle in angles:
    print(f"\nLook {angle} and press 'c' to capture...")

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture image. Exiting...")
            camera.release()
            cv2.destroyAllWindows()
            exit()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{angle} - Press 'c' to capture", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Face Capture", frame)

        # Wait for user confirmation to capture the image
        if cv2.waitKey(1) & 0xFF == ord('c'):
            for (x, y, w, h) in faces:
                face = gray[y:y + h, x:x + w]
                captured_faces.append((face, angle))
                print(f"Captured {angle} image.")
            break

# Save images with proper labeling
if len(captured_faces) == len(angles):
    for i, (face, angle) in enumerate(captured_faces):
        file_name = os.path.join(dataset_path, f"user_{user_id}_{angle}_{i}.jpg")
        cv2.imwrite(file_name, face)
    print(f"\n✅ All angles collected! Data saved successfully for user: {user_name} ({user_id})")
else:
    print("\n⚠️ Not all angles were collected. Please try again.")

camera.release()
cv2.destroyAllWindows()
