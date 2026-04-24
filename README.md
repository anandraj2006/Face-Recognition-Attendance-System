# Face Recognition Attendance System

A comprehensive desktop application built with Python and Tkinter for managing student attendance using facial recognition.

## Features
- **Student Registration**: Register students with their details.
- **Face Dataset Capture**: Capture images to train the facial recognition model.
- **Model Training**: Train the model using LBPH (Local Binary Patterns Histograms) Face Recognizer.
- **Automated Attendance**: Mark attendance automatically when a face is recognized.
- **Database Integration**: Store student details and attendance records securely using MySQL.

## Requirements

Ensure you have Python installed. You can install all dependencies via `pip`:

```bash
pip install -r requirements.txt
```

## Database Setup

1. Make sure you have MySQL installed and running on your local machine.
2. The default credentials in the code expect `localhost` with the respective username and password (you may need to configure these in `student.py` and other modules).
3. Create the database and required tables (e.g., `student` and `attendance`) before running the application.

## How to Run

1. Clone the repository to your local machine.
2. Install the required dependencies using the command above.
3. Start the application by running the main script:

```bash
python main.py
```

## Directory Structure

- `data/`: Contains sample datasets (user face captures) for model training.
- `pictures/`: Contains UI assets (images/icons) for the application interface.
- `*.py`: The source code files for the application logic and UI screens.
- `*.xml`: Haar cascade and trained classifier models for face detection and recognition.

## Notes

- Make sure your webcam is connected and accessible by OpenCV.
- You can train your own model by navigating to the "Train Data" section in the application after registering new faces.