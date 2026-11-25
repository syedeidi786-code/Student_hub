"""students.py - everything about students: add, view, search, edit, delete."""

import json
import os
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "students.json")

CLASS_LIST = ["Class 6", "Class 7", "Class 8", "Class 9",
              "Class 10", "Class 11", "Class 12"]


def load_students():
    """Read all students from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_students(student_list):
    """Write all students to the JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(student_list, file, indent=4)


def find_student(roll_no):
    """Return one student by roll number, or None if not found."""
    for student in load_students():
        if student["roll_no"].lower() == roll_no.strip().lower():
            return student
    return None


def add_student(name, roll_no, age, class_name):
    """Add a new student. Returns (True/False, message)."""
    name = name.strip()
    roll_no = roll_no.strip()

    if name == "" or roll_no == "":
        return False, "Please enter both the name and the roll number."
    if find_student(roll_no) is not None:
        return False, "Roll number " + roll_no + " is already used."

    student_list = load_students()
    student_list.append({
        "roll_no": roll_no,
        "name": name,
        "age": int(age),
        "class_name": class_name,
        "added_on": date.today().isoformat(),
    })
    save_students(student_list)
    return True, name + " was added."


def search_students(query):
    """Find students whose name or roll number contains the text."""
    query = query.strip().lower()
    if query == "":
        return load_students()

    results = []
    for student in load_students():
        if query in student["name"].lower() or query in student["roll_no"].lower():
            results.append(student)
    return results


def update_student(roll_no, name, age, class_name):
    """Change a student's details. The roll number stays the same."""
    student_list = load_students()
    for student in student_list:
        if student["roll_no"] == roll_no:
            student["name"] = name.strip()
            student["age"] = int(age)
            student["class_name"] = class_name
            save_students(student_list)
            return True
    return False


def delete_student(roll_no):
    """Remove a student from the list."""
    remaining = []
    for student in load_students():
        if student["roll_no"] != roll_no:
            remaining.append(student)
    save_students(remaining)


def recent_students(count=5):
    """The newest students first."""
    return load_students()[::-1][:count]
