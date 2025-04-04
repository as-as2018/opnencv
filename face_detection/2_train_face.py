import cv2
import numpy as np
import os
from PIL import Image

# Paths
dataset_path = "face_detection/face_dataset"  # Folder where images are stored
model_file = "face_detection/face_recognizer.yml"

# Initialize Recognizer
#  It is an OpenCV function that creates a Local Binary Patterns Histogram (LBPH) Face Recognizer. 
#  It is one of the most effective face recognition algorithms in
recognizer = cv2.face.LBPHFaceRecognizer_create()
# cv2.CascadeClassifier is a class in OpenCV used for object detection, mainly for detecting faces, eyes, and other objects using Haar cascades or LBP cascades.
#  It is commonly used for real-time face detection.
#  cv2.data.haarcascades is a predefined directory path in OpenCV that contains pre-trained Haar cascade XML files for object detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

if not os.path.exists(dataset_path):
    print(f"Error: Dataset folder '{dataset_path}' not found.")
    exit()

image_paths = [os.path.join(dataset_path, f) for f in os.listdir(dataset_path) if f.endswith(".jpg")]

faces = []
labels = []

print("Training model with collected face images...")

for image_path in image_paths:
    img = Image.open(image_path).convert("L")  # Convert to grayscale
    img_np = np.array(img, "uint8")

    label = int(os.path.basename(image_path).split("_")[0])  # Extract label from filename
    faces.append(img_np)
    labels.append(label)

    print(f"Processed: {image_path} (Label: {label})")

if len(faces) == 0:
    print("No face images found in dataset. Please collect images first.")
    exit()

recognizer.train(faces, np.array(labels))
recognizer.save(model_file)
print(f"Training complete. Model saved as '{model_file}'.")
