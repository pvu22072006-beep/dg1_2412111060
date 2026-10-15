from flask import Flask, jsonify, request, render_template
import json
import os

app = Flask(__name__)

MSSV = os.getenv("MSSV", "2412111060")
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "students.json")


def read_students():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def write_students(students):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)


@app.route("/")
def home():
    students = read_students()
    return render_template(
        "index.html",
        students=students,
        mssv=MSSV
    )


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "student": MSSV
    })


@app.route("/api/students")
def get_students():
    students = read_students()
    lop = request.args.get("lop")

    if lop:
        students = [student for student in students if student.get("lop") == lop]

    return jsonify(students)


@app.route("/api/students/<student_id>")
def get_student(student_id):
    students = read_students()

    for student in students:
        if student.get("id") == student_id:
            return jsonify(student)

    return jsonify({
        "error": "Student not found"
    }), 404


@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Invalid JSON"
        }), 400

    required_fields = ["mssv", "ho_ten", "lop", "diem"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing field: {field}"
            }), 400

    try:
        diem = float(data["diem"])
    except (TypeError, ValueError):
        return jsonify({
            "error": "diem must be a number"
        }), 400

    if diem < 0 or diem > 10:
        return jsonify({
            "error": "diem must be between 0 and 10"
        }), 400

    students = read_students()

    max_number = 0
    for student in students:
        student_id = student.get("id", "")
        if student_id.startswith("SV"):
            try:
                number = int(student_id[2:])
                max_number = max(max_number, number)
            except ValueError:
                pass

    new_student = {
        "id": f"SV{max_number + 1:03d}",
        "mssv": str(data["mssv"]),
        "ho_ten": str(data["ho_ten"]),
        "lop": str(data["lop"]),
        "diem": diem
    }

    students.append(new_student)
    write_students(students)

    return jsonify(new_student), 201


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
