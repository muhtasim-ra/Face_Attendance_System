Face Recognition Attendance System: A smart, real-time attendance system that uses computer vision to recognize faces and mark attendance automatically. Built with Python, OpenCV, and a local SQLite database for privacy and speed.🚀 FeaturesReal-Time Face Recognition: Detects and identifies students instantly using a webcam.Smart Attendance Logging: Automatically marks attendance and prevents "double marking" within a 30-second window.Local Database: Uses SQLite for instant data fetching (no internet required).Robust Image Handling: Supports PNG, JPG, and JPEG formats and auto-resizes images to fit the UI.Performance Optimized: Uses frame-skipping logic to run smoothly on standard laptops without lag.Graphical UI: Displays student details (Name, Major, Year) and a dynamic status dashboard (Active, Marked, Already Marked).🛠️ Tech 


StackLanguage: Python 3.10Libraries: opencv-python, face_recognition, cvzone, sqlite3Database: SQLite (Local file)📂 Project StructureBashFaceRecog/
│
├── Resources/              # Graphics for the UI
│   ├── background.png      # Main background template
│   └── Modes/              # Status cards (Active, Marked, etc.)
│
├── Images/                 # Student profile photos (File name = Student ID)
│   ├── 2231205042.png
│   └── ...
│
├── main.py                 # The main application script
├── AddDatatoDatabase.py    # Script to add/update student info in DB
├── EncodeGenerator.py      # Script to train the AI on faces
├── database.db             # The local database file (Auto-generated)
├── EncodeFile.p            # The trained face data (Auto-generated)
└── requirements.txt        # List of dependencies


Installation & Setup Prerequisite: Ensure you have Python 3.10 installed. (Newer versions like 3.11/3.12 may cause issues with the dlib library).

1. Clone the Repository:
   Bash:
   git clone https://github.com/your-username/face-attendance-system.git
   cd face-attendance-system

2. Create a Virtual EnvironmentBash# Windows
  # Windows
  Bash:
  py -3.10 -m venv venv
  .\venv\Scripts\activate
  
  # Mac/Linux
  python3.10 -m venv venv
  source venv/bin/activate

3. Install Dependencies: Install dlib and cmake first to avoid errors.
   Bash
   pip install cmake
   pip install dlib
   pip install opencv-python face_recognition cvzone numpy==1.24.3

How to Run
Step 1: Add Student Data
i. Put student photos in the Images/ folder. Name the files with the Student ID (e.g., 123456.png).

ii. Open AddDatatoDatabase.py and edit the data list with student details.

iii. Run the script to create the database:
Bash:
python AddDatatoDatabase.py

Step 2: Train the Model
Run the generator to scan the images and create the encoding file.
Bash:
python EncodeGenerator.py

Step 3: Start the System
Run the main application.
Bash:
python main.py


