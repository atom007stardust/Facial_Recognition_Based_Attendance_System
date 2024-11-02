# Facial_Recognition_Based_Attendance_System
Face Recognition Attendance System
This project implements a real-time face recognition attendance system using Python, OpenCV, Firebase, and Dlib. The system reads images from a specified folder, generates face encodings, and stores them in Firebase for later retrieval and attendance tracking.

## Table of Contents
Project Overview
Features
Technologies Used
Setup
Project Structure
Usage
Acknowledgments


## Project Overview
The Face Recognition Attendance System uses OpenCV and face_recognition to generate face encodings of student images stored in a local directory. These encodings are uploaded to Firebase for easy storage and access. The system can then use these encodings to match real-time video feeds or new images for attendance purposes.

## Features
Firebase Integration: Store student images and encodings securely in Firebase.
Face Encoding: Convert facial features into encodings for fast and accurate recognition.
Error Handling: Detect images without faces and handle them gracefully.
Encoding Persistence: Save encodings in a file for efficient loading during real-time attendance checking.

## Technologies Used
Python (for scripting)
OpenCV (for image processing)
face_recognition (for generating facial encodings)
Dlib (as a dependency of face_recognition)
Firebase (for image and data storage)

## Setup
Prerequisites
Install Python 3.7 or later.
Install the required Python packages:
pip install opencv-python face_recognition dlib firebase-admin
Set up a Firebase project and generate a serviceAccountKey.json file for Firebase Admin SDK. Add this file to your project folder.
Firebase Configuration
Realtime Database: Initialize a Firebase Realtime Database and update its rules for read/write access as needed.
Storage Bucket: Set up a Firebase Storage bucket to store and retrieve images.
Folder Structure
Add a folder named Images in the root directory. Place student images in this folder; these images will be processed to create face encodings.

## Project Structure
├── Images/                      # Directory containing student images (used to generate face encodings)

├── EncodeFile.p                 # File storing the encodings and student IDs after processing

├── face_recognition_attendance.py   # Main script to process images, encode faces, and upload data to Firebase

├── serviceAccountKey.json       # Firebase Admin SDK credentials (not included for security)

└── README.md                    # Documentation

## Usage
Step 1: Initialize Firebase
Ensure that Firebase is initialized in the script with the serviceAccountKey.json file
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://your-database-url.firebaseio.com/",
    'storageBucket': "your-storage-bucket.appspot.com"
})
Step 2: Run the Main Script
Execute face_recognition_attendance.py to perform the following tasks:

Load Images: Load all images from the Images folder.
Generate Encodings: Encode each image to obtain unique face representations.
Upload to Firebase: Store images in Firebase Storage and save encodings for future reference.
Save Encodings Locally: The script will save the encodings and student IDs in EncodeFile.p.
Run the script:
python face_recognition_attendance.py

Step 3: Attendance Tracking
Once EncodeFile.p is created, you can use this file in a separate script to perform real-time face recognition and check student attendance.

Example Code Snippets
Encoding Function
The function findEncodings converts images to RGB and generates face encodings:

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            print("No face found in the image, skipping...")
    return encodeList
Firebase Upload
Each image is uploaded to Firebase Storage as a blob:

fileName = f'{folderPath}/{path}'
bucket = storage.bucket()
blob = bucket.blob(fileName)
blob.upload_from_filename(fileName)

## Acknowledgments
face_recognition Library: Used for easy implementation of face recognition and encoding generation.
Firebase: Provides secure, scalable storage and database solutions for handling image data.
For more details on how to set up Firebase or install dependencies, please refer to the official documentation for each library or tool.
Special thanks to Murtaza Hassan for his workshop, which provided valuable insights and guidance for this project.

This README provides all the necessary information to understand, set up, and run the face recognition attendance system. Feel free to contribute to or modify the project to suit specific requirements.
