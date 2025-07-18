import csv

class ResultManager:
    def __init__(self, filename):
        self.filename = filename
        self.subjects = {
            "223601": ["Probability Distribution", 4],
            "223603": ["Sampling Technique", 4],
            "223605": ["Linear Algebra", 4],
            "223606": ["Lab-3: Probability Distribution and Sampling Technique", 2],
            "223608": ["Lab-4: Linear algebra", 2],
            "223707": ["Calculus- II", 4],
            "223708": ["Math Lab (Practical)", 2],
            "222211": ["Money, Banking and Public finance", 4],
            "222213": ["Bangladesh Economy", 2],
            "221109": ["English (Compulsory)", 0],
        }
        self.grade_points = {
            'A+': 4.0, 'A': 3.75, 'A-': 3.5,
            'B+': 3.25, 'B': 3.0, 'B-': 2.75,
            'C+': 2.5, 'C': 2.25, 'D': 2.0,
            'Fail': 0.0, 'F': 0.0, 'Pass': 0.0
        }
        self.students = self.load_data()

    def load_data(self):
        students = {}
        with open(self.filename, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                reg = row['Registration']
                students[reg] = row
        return students

    def save_data(self):
        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Roll', 'Registration', 'Name'] + list(self.subjects.keys())
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for student in self.students.values():
                writer.writerow(student)

    def view_result(self, reg_input):
        student = self.students.get(reg_input)
        if not student:
            print("Student not found.")
            return

        name = student['Name']
        roll = student['Roll']

        print(f"\nName: {name}")
        print(f"Roll: {roll}")
        print(f"Registration: {reg_input}\n")
        print(f"{'Subject Code':<12} {'Subject Name':<50} {'Grade':<6} {'Credit':<6}")
        print("-" * 80)

        total_credits = 0
        earned_credits = 0
        weighted_grade_points = 0
        fail_count = 0

        for code in self.subjects:
            subject_name, credit = self.subjects[code]
            grade = student.get(code, 'N/A').strip()

            grade_point = self.grade_points.get(grade, 0.0 if grade == 'Fail' else None)
            if grade_point is None:
                continue

            print(f"{code:<12} {subject_name:<50} {grade:<6} {credit:<6}")

            total_credits += credit
            if grade != 'Fail':
                earned_credits += credit
                weighted_grade_points += grade_point * credit
            else:
                fail_count += 1

        cgpa = round(weighted_grade_points / total_credits, 2) if total_credits else 0.0

        if cgpa >= 3.00:
            classification = "1st"
        elif cgpa >= 2.50:
            classification = "2nd"
        elif cgpa >= 2.00:
            classification = "3rd"
        else:
            classification = "Fail"

        promoted = "Yes" if fail_count <= 5 else "No"

        print("\nSummary:")
        print(f"Total Credits Attempted: {total_credits}")
        print(f"Credits Earned        : {earned_credits}")
        print(f"CGPA                  : {cgpa}")
        print(f"Class                 : {classification}")
        print(f"Failed Subjects       : {fail_count}")
        print(f"Promoted              : {promoted}")

    def update_result(self, update_str):
        try:
            parts = [x.strip() for x in update_str.split(',')]
            reg = parts[0]
            if reg not in self.students:
                print("Registration not found.")
                return

            student = self.students[reg]
            for part in parts[1:]:
                if '=' in part:
                    code, grade = part.strip().split('=')
                    code, grade = code.strip(), grade.strip()
                    if code in self.subjects:
                        student[code] = grade
                    else:
                        print(f"Ignored unknown subject code: {code}")
            print("\n✅ Result Updated Successfully.\n")
            self.view_result(reg)
            self.save_data()
        except Exception as e:
            print(f"Error updating result: {e}")


# ---------------- MAIN LOOP ----------------
manager = ResultManager('result.csv')

while True:
    choice = input("\nChoose option:\n1. View Result\n2. Update Result\nType 'quit' to exit\nEnter choice: ").strip()

    if choice == 'quit':
        print("Exiting program.")
        break

    elif choice == '1':
        reg = input("Enter registration number: ").strip()
        manager.view_result(reg)

    elif choice == '2':
        print("\nExample input:\n22236054372, 213601=A+, 213603=C+, 213709=B")
        update_input = input("Enter update in format shown above:\n> ")
        manager.update_result(update_input)

    else:
        print("Invalid choice. Please enter 1, 2, or 'quit'.")
