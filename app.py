"""app.py - the web pages. Run with:  streamlit run app.py"""

import html
import os
from datetime import date, datetime

import streamlit as st

import attendance
import marks
import students

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="StudentHub", layout="wide")

PAGES = ["Dashboard", "Manage Students", "Marks", "Attendance"]

# ---------- SVG icons (simple line icons) ----------
ICONS = {
    "book": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "award": '<circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>',
    "check": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
    "percent": '<line x1="19" y1="5" x2="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
}


def icon(name, size=22):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="' + str(size) + '" height="' + str(size) +
            '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round">' + ICONS[name] + '</svg>')


# ---------- Small helpers to build the screen ----------
class Html(str):
    """Marks a piece of text as ready-made HTML (so it is not escaped)."""


def load_css():
    css_path = os.path.join(BASE_DIR, "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as file:
            st.markdown("<style>" + file.read() + "</style>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .page-header h1 { margin-bottom: 0.2rem; }
        .page-header p { color: #888; margin-bottom: 1.5rem; }
        .stat-card {
            display: flex; align-items: center; gap: 14px;
            padding: 16px; border-radius: 10px;
            border: 1px solid rgba(128,128,128,0.2);
            margin-bottom: 1rem;
        }
        .stat-value { font-size: 1.4rem; font-weight: 700; }
        .stat-label { font-size: 0.85rem; opacity: 0.75; }
        .table-wrap { overflow-x: auto; margin: 1rem 0; }
        .clean-table { width: 100%; border-collapse: collapse; }
        .clean-table th, .clean-table td {
            padding: 10px 12px; text-align: left;
            border-bottom: 1px solid rgba(128,128,128,0.2);
        }
        .pill { padding: 3px 10px; border-radius: 999px; font-size: 0.8rem; font-weight: 600; }
        .pill-good { background: rgba(34,197,94,0.15); color: #22c55e; }
        .pill-mid { background: rgba(234,179,8,0.15); color: #eab308; }
        .pill-bad { background: rgba(239,68,68,0.15); color: #ef4444; }
        .profile { display: flex; align-items: center; gap: 16px; margin: 1rem 0; }
        .avatar {
            width: 48px; height: 48px; border-radius: 50%;
            background: #3b82f6; color: white; font-weight: bold;
            display: flex; align-items: center; justify-content: center;
        }
        .profile-name { font-size: 1.2rem; font-weight: 600; }
        .profile-meta { display: flex; gap: 12px; font-size: 0.85rem; opacity: 0.75; }
        .brand { display: flex; align-items: center; gap: 10px; font-size: 1.25rem; font-weight: 700; margin-bottom: 1rem; }
        </style>
        """, unsafe_allow_html=True)

def page_header(title, subtitle):
    st.markdown('<div class="page-header"><h1>' + html.escape(title) + '</h1><p>' +
                html.escape(subtitle) + '</p></div>', unsafe_allow_html=True)


def stat_card(icon_name, label, value):
    st.markdown('<div class="stat-card"><div class="stat-chip">' + icon(icon_name) +
                '</div><div><div class="stat-value">' + html.escape(str(value)) +
                '</div><div class="stat-label">' + html.escape(label) + '</div></div></div>',
                unsafe_allow_html=True)


def pill(text, kind):
    """A small coloured label. kind is good, mid or bad."""
    return Html('<span class="pill pill-' + kind + '">' + html.escape(text) + '</span>')


def grade_pill(grade):
    if grade in ("A+", "A", "B"):
        return pill(grade, "good")
    if grade in ("C", "D"):
        return pill(grade, "mid")
    return pill(grade, "bad")


def attendance_pill(percentage):
    if percentage is None:
        return "-"
    text = str(percentage) + "%"
    if percentage >= 75:
        return pill(text, "good")
    if percentage >= 50:
        return pill(text, "mid")
    return pill(text, "bad")


def html_table(headers, rows):
    head = ""
    for header in headers:
        head += "<th>" + html.escape(header) + "</th>"

    body = ""
    for row in rows:
        body += "<tr>"
        for cell in row:
            if not isinstance(cell, Html):
                cell = html.escape(str(cell))
            body += "<td>" + cell + "</td>"
        body += "</tr>"

    st.markdown('<div class="table-wrap"><table class="clean-table"><thead><tr>' + head +
                '</tr></thead><tbody>' + body + '</tbody></table></div>',
                unsafe_allow_html=True)


def format_date(iso_text):
    try:
        return datetime.strptime(iso_text, "%Y-%m-%d").strftime("%d %b %Y")
    except ValueError:
        return iso_text


def initials(name):
    letters = ""
    for part in name.split()[:2]:
        letters += part[0].upper()
    return letters or "?"


def pick_student(label, key, all_students):
    """A drop-down that returns the roll number of the chosen student."""
    rolls = []
    names = {}
    for student in all_students:
        rolls.append(student["roll_no"])
        names[student["roll_no"]] = student["name"]

    def show(roll_no):
        return roll_no + " - " + names[roll_no]

    return st.selectbox(label, rolls, format_func=show, key=key)


def flash(kind, text):
    """Keep a message for after the page refreshes."""
    st.session_state["flash"] = (kind, text)


def show_flash():
    if "flash" in st.session_state:
        kind, text = st.session_state.pop("flash")
        if kind == "success":
            st.success(text)
        else:
            st.error(text)


def no_students_message():
    st.info("There are no students yet. Add one in Manage Students first.")


# ---------- Page 1: Dashboard ----------
def dashboard_page():
    page_header("Dashboard", "A quick look at your students today.")

    all_students = students.load_students()
    marks_data = marks.load_marks()
    present_today, marked_today = attendance.today_summary(date.today().isoformat())

    students_with_marks = 0
    for student in all_students:
        if student["roll_no"] in marks_data:
            students_with_marks += 1

    if marked_today == 0:
        attendance_value = "Not marked"
    else:
        attendance_value = str(present_today) + " of " + str(marked_today)

    col1, col2, col3 = st.columns(3)
    with col1:
        stat_card("users", "Total students", len(all_students))
    with col2:
        stat_card("award", "Students with marks", students_with_marks)
    with col3:
        stat_card("check", "Present today", attendance_value)

    st.subheader("Recently added students")
    recent = students.recent_students(5)
    if len(recent) == 0:
        st.info("No students yet. Add your first student in Manage Students.")
        return

    rows = []
    for student in recent:
        rows.append([student["roll_no"], student["name"], student["class_name"],
                     student["age"], format_date(student["added_on"])])
    html_table(["Roll no.", "Name", "Class", "Age", "Added on"], rows)


# ---------- Page 2: Manage Students ----------
def manage_students_page():
    page_header("Manage Students", "Add, find, view, edit or remove students.")
    show_flash()

    all_students = students.load_students()
    tab_all, tab_add, tab_view, tab_edit = st.tabs(
        ["All students", "Add student", "Student details", "Edit or delete"])

    # --- View all + search ---
    with tab_all:
        query = st.text_input("Search", placeholder="Type a name or roll number",
                              label_visibility="collapsed")
        results = students.search_students(query)
        if len(results) == 0:
            st.info("No students found.")
        else:
            rows = []
            for student in results:
                rows.append([student["roll_no"], student["name"], student["class_name"],
                             student["age"], format_date(student["added_on"])])
            html_table(["Roll no.", "Name", "Class", "Age", "Added on"], rows)
            st.caption(str(len(results)) + " student(s) shown")

    # --- Add ---
    with tab_add:
        # The form number changes after each save, so the boxes start empty again.
        v = st.session_state.get("add_version", 0)
        with st.form("add_form_" + str(v)):
            name = st.text_input("Full name", key="add_name_" + str(v))
            roll_no = st.text_input("Roll number", key="add_roll_" + str(v))
            col_a, col_b = st.columns(2)
            age = col_a.number_input("Age", min_value=3, max_value=100, value=15,
                                     key="add_age_" + str(v))
            class_name = col_b.selectbox("Class", students.CLASS_LIST, key="add_class_" + str(v))
            submitted = st.form_submit_button("Add student")

        if submitted:
            ok, message = students.add_student(name, roll_no, age, class_name)
            if ok:
                st.session_state["add_version"] = v + 1
                flash("success", message)
                st.rerun()
            else:
                st.error(message)

    # --- Details of one student ---
    with tab_view:
        if len(all_students) == 0:
            no_students_message()
        else:
            roll = pick_student("Choose a student", "details_pick", all_students)
            student = students.find_student(roll)

            st.markdown('<div class="profile"><div class="avatar">' + html.escape(initials(student["name"])) +
                        '</div><div><div class="profile-name">' + html.escape(student["name"]) +
                        '</div><div class="profile-meta"><span>Roll no. ' + html.escape(student["roll_no"]) +
                        '</span><span>' + html.escape(student["class_name"]) +
                        '</span><span>Age ' + str(student["age"]) +
                        '</span><span>Added ' + format_date(student["added_on"]) +
                        '</span></div></div></div>', unsafe_allow_html=True)

            saved_marks = marks.get_marks(roll)
            summary = attendance.calculate_summary(roll)
            if saved_marks is None:
                total, percentage, grade = "-", "-", "-"
            else:
                result = marks.calculate_result(saved_marks)
                total = str(result["total"]) + " / " + str(marks.MAX_MARKS * len(marks.SUBJECTS))
                percentage = str(result["percentage"]) + "%"
                grade = result["grade"]
            if summary["percentage"] is None:
                attendance_text = "-"
            else:
                attendance_text = str(summary["percentage"]) + "%"

            c1, c2 = st.columns(2)
            with c1:
                stat_card("book", "Total marks", total)
            with c2:
                stat_card("percent", "Percentage", percentage)
            c3, c4 = st.columns(2)
            with c3:
                stat_card("award", "Grade", grade)
            with c4:
                stat_card("check", "Attendance", attendance_text)

    # --- Edit or delete ---
    with tab_edit:
        if len(all_students) == 0:
            no_students_message()
        else:
            roll = pick_student("Choose a student", "edit_pick", all_students)
            student = students.find_student(roll)

            with st.form("edit_form_" + roll):
                new_name = st.text_input("Full name", value=student["name"], key="edit_name_" + roll)
                st.text_input("Roll number (cannot be changed)", value=student["roll_no"],
                              disabled=True, key="edit_roll_" + roll)
                col_a, col_b = st.columns(2)
                new_age = col_a.number_input("Age", min_value=3, max_value=100,
                                             value=int(student["age"]), key="edit_age_" + roll)
                if student["class_name"] in students.CLASS_LIST:
                    class_index = students.CLASS_LIST.index(student["class_name"])
                else:
                    class_index = 0
                new_class = col_b.selectbox("Class", students.CLASS_LIST, index=class_index,
                                            key="edit_class_" + roll)
                saved = st.form_submit_button("Save changes")

            if saved:
                if new_name.strip() == "":
                    st.error("The name cannot be empty.")
                else:
                    students.update_student(roll, new_name, new_age, new_class)
                    flash("success", "Details updated.")
                    st.rerun()

            st.subheader("Delete student")
            st.caption("This also removes their marks and attendance.")
            confirm = st.checkbox("Yes, I want to delete " + student["name"],
                                  key="confirm_" + roll)
            if st.button("Delete student", disabled=not confirm, key="delete_" + roll):
                students.delete_student(roll)
                marks.delete_marks(roll)
                attendance.delete_attendance(roll)
                st.session_state.pop("edit_pick", None)
                st.session_state.pop("details_pick", None)
                flash("success", student["name"] + " was deleted.")
                st.rerun()


# ---------- Page 3: Marks ----------
def marks_page():
    page_header("Marks", "Enter marks. Total, percentage and grade are worked out for you.")
    show_flash()

    all_students = students.load_students()
    if len(all_students) == 0:
        no_students_message()
        return

    roll = pick_student("Student", "marks_pick", all_students)
    saved_marks = marks.get_marks(roll)
    if saved_marks is None:
        saved_marks = {}

    with st.form("marks_form"):
        columns = st.columns(len(marks.SUBJECTS))
        entered = {}
        for column, subject in zip(columns, marks.SUBJECTS):
            entered[subject] = column.number_input(
                subject + " (out of " + str(marks.MAX_MARKS) + ")",
                min_value=0, max_value=marks.MAX_MARKS,
                value=int(saved_marks.get(subject, 0)),
                key=subject + "_" + roll)
        submitted = st.form_submit_button("Save marks")

    if submitted:
        marks.save_marks(roll, entered)
        flash("success", "Marks saved.")
        st.rerun()

    current = marks.get_marks(roll)
    if current is not None:
        result = marks.calculate_result(current)
        c1, c2, c3 = st.columns(3)
        with c1:
            stat_card("book", "Total marks",
                      str(result["total"]) + " / " + str(marks.MAX_MARKS * len(marks.SUBJECTS)))
        with c2:
            stat_card("percent", "Percentage", str(result["percentage"]) + "%")
        with c3:
            stat_card("award", "Grade", result["grade"])

    st.subheader("All results")
    rows = []
    for student in all_students:
        student_marks = marks.get_marks(student["roll_no"])
        if student_marks is None:
            continue
        result = marks.calculate_result(student_marks)
        row = [student["roll_no"], student["name"]]
        for subject in marks.SUBJECTS:
            row.append(student_marks.get(subject, 0))
        row += [result["total"], str(result["percentage"]) + "%", grade_pill(result["grade"])]
        rows.append(row)

    if len(rows) == 0:
        st.info("No marks have been entered yet.")
    else:
        html_table(["Roll no.", "Name"] + marks.SUBJECTS + ["Total", "Percentage", "Grade"], rows)


# ---------- Page 4: Attendance ----------
def attendance_page():
    page_header("Attendance", "Mark who is present or absent and see attendance records.")
    show_flash()

    all_students = students.load_students()
    if len(all_students) == 0:
        no_students_message()
        return

    tab_mark, tab_records = st.tabs(["Mark attendance", "Records"])

    with tab_mark:
        day = st.date_input("Date", value=date.today(), max_value=date.today(), key="att_date")
        day_text = day.isoformat()

        with st.form("attendance_form"):
            choices = {}
            for student in all_students:
                left, right = st.columns([3, 2])
                left.markdown("**" + student["name"] + "**  \nRoll no. " + student["roll_no"])
                saved_status = attendance.get_status(student["roll_no"], day_text)
                if saved_status == "Absent":
                    index = 1
                else:
                    index = 0
                choices[student["roll_no"]] = right.radio(
                    "Status", ["Present", "Absent"], index=index, horizontal=True,
                    key="att_" + day_text + "_" + student["roll_no"],
                    label_visibility="collapsed")
            submitted = st.form_submit_button("Save attendance")

        if submitted:
            attendance.save_day(day_text, choices)
            flash("success", "Attendance saved for " + format_date(day_text) + ".")
            st.rerun()

    with tab_records:
        rows = []
        for student in all_students:
            summary = attendance.calculate_summary(student["roll_no"])
            rows.append([student["roll_no"], student["name"], summary["present"],
                         summary["absent"], summary["total"],
                         attendance_pill(summary["percentage"])])
        html_table(["Roll no.", "Name", "Present", "Absent", "Total days", "Attendance"], rows)

        st.subheader("Day-by-day record")
        roll = pick_student("Student", "records_pick", all_students)
        records = attendance.get_records(roll)
        if len(records) == 0:
            st.info("No attendance has been marked for this student yet.")
        else:
            day_rows = []
            for record_day, status in records:
                if status == "Present":
                    day_rows.append([format_date(record_day), pill("Present", "good")])
                else:
                    day_rows.append([format_date(record_day), pill("Absent", "bad")])
            html_table(["Date", "Status"], day_rows)


# ---------- Main ----------
def main():
    load_css()

    with st.sidebar:
        st.markdown('<div class="brand"><span class="brand-logo">' + icon("book", 22) +
                    '</span><span class="brand-name">StudentHub</span></div>',
                    unsafe_allow_html=True)
        page = st.radio("Menu", PAGES, label_visibility="collapsed")

    if page == "Dashboard":
        dashboard_page()
    elif page == "Manage Students":
        manage_students_page()
    elif page == "Marks":
        marks_page()
    else:
        attendance_page()


main()
