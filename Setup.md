# Python Setup and OpenCV Installation on Windows

This guide will walk you through:

1. Installing Python
2. Setting up Environment Variables
3. Creating and Using a Virtual Environment
4. Installing OpenCV

---

## 1. Install Python on Windows

1. Go to the official Python website: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2. Download the latest stable release for Windows.
3. Run the installer.
4. **Important**: Check the box that says **"Add Python to PATH"**.
5. Choose "Customize installation" if you want to select specific features.
6. Click **Install Now** and wait for the installation to complete.

---

## 2. Set Up Environment Variables (if not set automatically)

If you forgot to check "Add Python to PATH" during installation:

1. Press `Win + S` and search for **Environment Variables**.
2. Click **Edit the system environment variables**.
3. In the System Properties window, click **Environment Variables**.
4. Under **System Variables**, find the `Path` variable and click **Edit**.
5. Click **New** and add the following paths:
6. copy python path from:
C:\Users<YourUsername>\AppData\Local\Programs\Python\Python<version>\lib
C:\Users<YourUsername>\AppData\Local\Programs\Python\Python<version>\Scripts\
7. create virtual environment:```python -m venv venv```
8. Activate virtual environment:```.\venv\Scripts\activate```
9. install openCV:```pip install opencv-python```
10. 
   
