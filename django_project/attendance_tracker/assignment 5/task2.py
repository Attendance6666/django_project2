import json

def process_students():
    with open("students.json", "r", encoding="utf-8") as file:
        students = json.load(file)

    updated_students = []

    for student in students:
        avg_grade = round(sum(student["grades"]) / len(student["grades"]))
        student["average_grade"] = avg_grade
        updated_students.append(student)

    with open("students_with_average.json", "w", encoding="utf-8") as file:
        json.dump(updated_students, file, indent=4)


process_students()
