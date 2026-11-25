📚 StudentHub

A clean, lightweight student record management system built with Python and Streamlit. StudentHub allows teachers and administrators to manage student profiles, track daily attendance, and calculate exam marks and grades automatically using local JSON storage.

✨ Features

📊 Dashboard Overview: View key metrics at a glance—total enrolled students, students with recorded marks, today's attendance summary, and a list of recently added students.

👨‍🎓 Student Management:

Add new students with full name, unique roll number, age, and class (Class 6 to Class 12).

Search students instantly by name or roll number.

View individual student profile cards summarizing their overall marks, percentage, grade, and attendance rate.

Edit student details or delete records (automatically cleans up associated marks and attendance).

📝 Marks & Grading:

Enter subject-wise marks (English, Mathematics, Science — out of 100 each).

Automatically calculates total score, percentage, and letter grade (A+, A, B, C, D, F).

Displays a complete results table with color-coded grade badges.

✅ Attendance Tracking:

Mark daily attendance (Present / Absent) for all students on any selected date.

View overall attendance percentages per student with color-coded status pills.

Inspect day-by-day attendance history for individual students.

🗂️ Project Structure

Student_hub/
├── app.py              # Main Streamlit web application & UI layout
├── students.py         # Student CRUD operations and search logic
├── marks.py            # Marks storage, percentage, and grade calculation
├── attendance.py       # Daily attendance tracking and summary statistics
├── assets/
│   └── style.css       # Custom CSS styling (optional; app includes fallback styles)
├── data/               # Auto-generated folder storing JSON records
│   ├── students.json
│   ├── marks.json
│   └── attendance.json
├── LICENSE             # MIT License
└── README.md           # Project documentation


🚀 Getting Started

Prerequisites

Python 3.8 or higher

pip (Python package manager)

Installation

Clone the repository:

git clone https://github.com/your-username/Student_hub.git
cd Student_hub


Create and activate a virtual environment (optional but recommended):

python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate


Install Streamlit:

pip install streamlit


Running the Application

Launch the app using the Streamlit CLI:

streamlit run app.py


Once started, open your browser and navigate to http://localhost:8501.

🛠️ Tech Stack

Frontend / UI: Streamlit, Custom HTML & CSS

Backend: Python Standard Library (json, os, datetime, html)

Database: Local JSON file storage (zero external database setup required)

📄 License

This project is licensed under the MIT License — see the LICENSE file for details.
