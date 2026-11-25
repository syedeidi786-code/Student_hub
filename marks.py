"""marks.py - enter marks, then work out total, percentage and grade."""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "marks.json")

SUBJECTS = ["English", "Mathematics", "Science"]
MAX_MARKS = 100  # each subject is out of 100


def load_marks():
    """Read all marks. The file looks like {roll_no: {subject: marks}}."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}


def save_all_marks(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def save_marks(roll_no, subject_marks):
    """Save (or replace) the marks of one student."""
    data = load_marks()
    data[roll_no] = subject_marks
    save_all_marks(data)


def get_marks(roll_no):
    """Marks of one student, or None if not entered yet."""
    return load_marks().get(roll_no)


def delete_marks(roll_no):
    data = load_marks()
    if roll_no in data:
        del data[roll_no]
        save_all_marks(data)


def get_grade(percentage):
    if percentage >= 90:
        return "A+"
    if percentage >= 80:
        return "A"
    if percentage >= 70:
        return "B"
    if percentage >= 60:
        return "C"
    if percentage >= 50:
        return "D"
    return "F"


def calculate_result(subject_marks):
    """Return total, percentage and grade for one student's marks."""
    total = 0
    for subject in SUBJECTS:
        total += subject_marks.get(subject, 0)

    percentage = round(total / (MAX_MARKS * len(SUBJECTS)) * 100, 2)
    return {
        "total": total,
        "percentage": percentage,
        "grade": get_grade(percentage),
    }
