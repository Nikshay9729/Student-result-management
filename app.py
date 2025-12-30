from flask import Flask, request, render_template_string

app = Flask(__name__)

students = {}

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Result Management System</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Montserrat', sans-serif;
            background: linear-gradient(135deg, #c3ecf8, #e7f0fd);
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 900px;
            margin: 40px auto;
            background: #fff;
            padding: 35px 50px;
            border-radius: 25px;
            box-shadow: 0 12px 35px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }
        .container:hover {
            transform: translateY(-5px);
        }
        h2, h3 {
            text-align: center;
            color: #333;
        }
        form {
            margin-bottom: 35px;
        }
        input[type=text], input[type=number] {
            width: 95%;
            padding: 14px;
            margin: 10px 0 18px 0;
            border: 1px solid #ccc;
            border-radius: 12px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        input[type=text]:focus, input[type=number]:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 8px rgba(76, 175, 80, 0.3);
            outline: none;
        }
        input[type=submit] {
            background: linear-gradient(45deg, #4CAF50, #2e7d32);
            color: white;
            padding: 14px 30px;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        input[type=submit]:hover {
            background: linear-gradient(45deg, #2e7d32, #4CAF50);
            transform: scale(1.05);
        }
        hr {
            margin: 35px 0;
            border: 0;
            height: 1px;
            background: #ccc;
        }
        .report {
            background: #f0f8ff;
            padding: 25px 30px;
            border-radius: 20px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }
        .report h3 {
            background: linear-gradient(90deg, #4CAF50, #81c784);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 28px;
        }
        .report table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 10px;
            margin-top: 20px;
        }
        th, td {
            padding: 14px;
            text-align: center;
            border-radius: 12px;
            font-weight: 500;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        td {
            background-color: #e6f7ff;
        }
        td.grade-A { background-color: #c8e6c9; font-weight: bold; color: #2e7d32; }
        td.grade-B { background-color: #bbdefb; font-weight: bold; color: #1565c0; }
        td.grade-C { background-color: #ffe0b2; font-weight: bold; color: #ef6c00; }
        td.grade-F { background-color: #ffcdd2; font-weight: bold; color: #b71c1c; }
        tr:hover td {
            transform: scale(1.02);
            transition: all 0.3s ease;
        }
        .summary {
            margin-top: 22px;
            font-size: 18px;
        }
        .summary b {
            color: #333;
        }
        @media(max-width: 650px) {
            input[type=text], input[type=number] { width: 90%; }
            .container { padding: 25px 20px; }
            .report h3 { font-size: 24px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Student Result Management System</h2>

        <h3>Enter Student Details</h3>
        <form method="post">
            Roll No: <br><input type="text" name="roll" required><br>
            Name: <br><input type="text" name="name" required><br>
            Class: <br><input type="text" name="cls" required><br>
            Subject: <br><input type="text" name="subject" required><br>
            Marks: <br><input type="number" name="marks" required><br>
            <input type="submit" value="Save Result">
        </form>

        <hr>

        <h3>View Student Result</h3>
        <form method="get">
            Roll No: <input type="text" name="view" required>
            <input type="submit" value="View Result">
        </form>

        {% if student %}
        <div class="report">
            <h3>Report Card</h3>
            <p><b>Name:</b> {{ student.name }}</p>
            <p><b>Class:</b> {{ student.cls }}</p>

            <table>
                <tr>
                    <th>Subject</th>
                    <th>Marks</th>
                    <th>Grade</th>
                </tr>
                {% for sub in student.subjects %}
                <tr>
                    <td>{{ sub.subject }}</td>
                    <td>{{ sub.marks }}</td>
                    <td class="grade-{{ sub.grade }}">{{ sub.grade }}</td>
                </tr>
                {% endfor %}
            </table>

            <div class="summary">
                <p><b>Total Marks:</b> {{ student.total }}</p>
                <p><b>Percentage:</b> {{ student.percentage }}%</p>
                <p><b>Overall Grade:</b> {{ student.overall_grade }}</p>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def calculate_overall_grade(percentage):
    if percentage >= 80:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 40:
        return "C"
    else:
        return "F"

@app.route("/", methods=["GET", "POST"])
def index():
    student = None

    if request.method == "POST":
        roll = request.form["roll"]
        name = request.form["name"]
        cls = request.form["cls"]
        subject = request.form["subject"]
        marks = int(request.form["marks"])

        if marks >= 80:
            grade = "A"
        elif marks >= 60:
            grade = "B"
        elif marks >= 40:
            grade = "C"
        else:
            grade = "F"

        if roll in students:
            students[roll]["subjects"].append({"subject": subject, "marks": marks, "grade": grade})
        else:
            students[roll] = {
                "name": name,
                "cls": cls,
                "subjects": [{"subject": subject, "marks": marks, "grade": grade}]
            }

    view = request.args.get("view")
    if view in students:
        student = students[view]
        total = sum(sub["marks"] for sub in student["subjects"])
        count = len(student["subjects"])
        percentage = round(total / count, 2)
        overall_grade = calculate_overall_grade(percentage)
        student["total"] = total
        student["percentage"] = percentage
        student["overall_grade"] = overall_grade

    return render_template_string(html, student=student)

if __name__ == "__main__":
    app.run(debug=True)
