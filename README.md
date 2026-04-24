# Face Recognition Attendance System

A comprehensive desktop application built with **Python** and **Tkinter** for managing student attendance using real-time facial recognition.

## Features

- **Student Registration** — Register students with their personal and course details.
- **Face Dataset Capture** — Capture face samples via webcam to build the training dataset.
- **Model Training** — Train the LBPH (Local Binary Patterns Histograms) face recognizer model.
- **Automated Attendance** — Mark attendance automatically when a registered face is recognized.
- **Manual Attendance** — Manually mark or update attendance records.
- **CSV Import / Export** — Import and export attendance data as CSV files.
- **Help Desk** — Built-in support system with email and WhatsApp integration.
- **MySQL Integration** — All student and attendance data is stored in a MySQL database.

## Project Structure

```
Face-Recognition-Attendance-System/
├── main.py                  # Entry point — run this to start the application
├── requirements.txt         # Python dependencies
├── .gitignore
├── README.md
│
├── src/                     # All application modules
│   ├── __init__.py
│   ├── student.py           # Student management module
│   ├── attendance.py        # Attendance management module
│   ├── train.py             # Model training module
│   ├── facerecogniton.py    # Face recognition & live camera module
│   ├── helpdesk.py          # Help desk module
│   ├── photos.py            # Photos module
│   └── models/
│       ├── classifier.xml                   # Trained LBPH model (generated after training)
│       └── haarcascade_frontalface_default.xml  # Haar Cascade for face detection
│
├── pictures/                # UI assets (icons, background images)
└── data/                    # Training face images (captured via the app)
```

## Requirements

Ensure you have Python installed. Install all dependencies with:

```bash
pip install -r requirements.txt
```

## Database Setup

1. Install and run **MySQL** on your local machine.
2. Create a database named `mydb`.
3. The application will automatically create the required tables (`students`, `attendance`) on first launch.
4. Update the database credentials in `src/student.py`, `src/attendance.py`, and `src/facerecogniton.py` if needed:

```python
host="localhost"
user="root"
password="your_password"
database="mydb"
```

## How to Run

```bash
python main.py
```

> **Note:** Always run from the project root directory so that relative paths resolve correctly.

## Workflow

1. **Register a student** using the *Student* module.
2. **Capture face samples** by clicking *Take Photo* (saves images to `data/`).
3. **Train the model** using the *Train Data* module (generates `src/models/classifier.xml`).
4. **Take attendance** automatically using the *Face Recognition* module.
5. **View / export** records using the *Attendance* module.

## Notes

- Make sure your webcam is connected and accessible by OpenCV.
- A minimum of ~25 face samples per student is recommended for accurate recognition.