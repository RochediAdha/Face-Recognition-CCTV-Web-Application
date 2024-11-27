# Face Recognition CCTV Web Application

A web application for live CCTV monitoring with face recognition functionality, built using **Flask** for the backend and **HTML, CSS, JavaScript** for the frontend.

## Features

- Detect and recognize faces from live CCTV streams.
- Easily manage known faces by uploading images.
- Supports multiple CCTV feeds.
- API-based communication between frontend and backend.
- Cross-Origin Resource Sharing (CORS) enabled.

---

## Prerequisites

Before running the application, make sure you have the following installed:

- **Python 3.7+**
- **pip** (Python package manager)
- **Node.js** (optional, if modifying frontend dependencies)

---

## Project Structure

```plaintext
face_recognition_app/
├── backend/                # Backend folder
│   ├── app.py              # Flask application
│   ├── cctv_list.json      # List of CCTV streams
│   ├── known_faces/        # Folder containing known face images
│   │   ├── person1.jpg     # Example image
│   │   └── person2.jpg     # Example image
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # Frontend folder
│   ├── index.html          # Main HTML page
│   ├── css/                # Folder for stylesheets
│   │   └── styles.css      # Main CSS file
│   └── js/                 # Folder for JavaScript
│       └── app.js          # Main JavaScript file
│
└── README.md               # Documentation
```
