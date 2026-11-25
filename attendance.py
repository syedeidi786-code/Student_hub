"""attendance.py - mark Present/Absent and work out attendance percentage."""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "attendance.json")


def load_attendance():
    """Read all records. The file looks like {roll_no: {date: status}}."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}


def save_all_attendance(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def save_day(day, statuses):
    """Save one day for many students. statuses = {roll_no: 'Present'/'Absent'}."""
    data = load_attendance()
    for roll_no in statuses:
        if roll_no not in data:
            data[roll_no] = {}
        data[roll_no][day] = statuses[roll_no]
    save_all_attendance(data)


def get_status(roll_no, day):
    """'Present', 'Absent' or None if that day was not marked."""
    return load_attendance().get(roll_no, {}).get(day)


def get_records(roll_no):
    """All days of one student, newest first."""
    records = load_attendance().get(roll_no, {})
    days = sorted(records.keys(), reverse=True)
    result = []
    for day in days:
        result.append((day, records[day]))
    return result


def calculate_summary(roll_no):
    """Present days, absent days, total days and attendance percentage."""
    present = 0
    absent = 0
    for day, status in get_records(roll_no):
        if status == "Present":
            present += 1
        else:
            absent += 1

    total = present + absent
    percentage = None
    if total > 0:
        percentage = round(present / total * 100, 1)
    return {"present": present, "absent": absent,
            "total": total, "percentage": percentage}


def today_summary(day):
    """How many students were marked on this day, and how many were present."""
    marked = 0
    present = 0
    for records in load_attendance().values():
        if day in records:
            marked += 1
            if records[day] == "Present":
                present += 1
    return present, marked


def delete_attendance(roll_no):
    data = load_attendance()
    if roll_no in data:
        del data[roll_no]
        save_all_attendance(data)
