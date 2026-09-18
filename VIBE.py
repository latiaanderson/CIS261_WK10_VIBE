"""Student Grade Calculator."""

FILE_NAME = "student_grades.txt"


class Student:
	"""Store a student's identifying information and calculated grade."""

	def __init__(self, name, student_id, test_scores):
		self.name = name
		self.student_id = student_id
		self.test_scores = test_scores
		self.average = sum(test_scores) / len(test_scores)
		self.grade = calculate_letter_grade(self.average)

	def to_file_line(self):
		scores = "|".join(f"{score:.2f}" for score in self.test_scores)
		return f"{self.name}|{self.student_id}|{scores}|{self.average:.2f}|{self.grade}\n"


def calculate_letter_grade(average):
	if average >= 90:
		return "A"
	if average >= 80:
		return "B"
	if average >= 70:
		return "C"
	if average >= 60:
		return "D"
	return "F"


def load_students():
	students = []
	try:
		with open(FILE_NAME, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				parts = line.rstrip("\n").split("|")
				if len(parts) != 7:
					print(f"Skipping invalid record on line {line_number}.")
					continue
				try:
					scores = [float(parts[index]) for index in range(2, 5)]
					students.append(Student(parts[0], parts[1], scores))
				except ValueError:
					print(f"Skipping invalid scores on line {line_number}.")
	except FileNotFoundError:
		return students
	except OSError as error:
		print(f"Could not load student records: {error}")
	return students


def save_students(students):
	try:
		with open(FILE_NAME, "w", encoding="utf-8") as file:
			for student in students:
				file.write(student.to_file_line())
		return True
	except OSError as error:
		print(f"Could not save student records: {error}")
		return False


def get_score(test_number):
	while True:
		value = input(f"Enter Test {test_number} score (0-100): ").strip()
		try:
			score = float(value)
			if 0 <= score <= 100:
				return score
			print("Score must be between 0 and 100.")
		except ValueError:
			print("Please enter a valid number.")


def add_student(students):
	print("\nAdd Student")
	name = input("Enter student name: ").strip()
	student_id = input("Enter student ID: ").strip()
	if not name or not student_id:
		print("Name and student ID are required.")
		return
	scores = [get_score(number) for number in range(1, 4)]
	student = Student(name, student_id, scores)
	students.append(student)
	print(f"Added {student.name}. Average: {student.average:.2f}, Grade: {student.grade}")


def display_students(students):
	if not students:
		print("No student records found.")
		return
	print("\nStudent Records")
	print("-" * 96)
	print(f"{'Name':<22}{'ID':<14}{'Test 1':>10}{'Test 2':>10}{'Test 3':>10}{'Average':>11}{'Grade':>8}")
	print("-" * 96)
	for student in students:
		print(
			f"{student.name:<22.22}{student.student_id:<14.14}"
			f"{student.test_scores[0]:>10.2f}{student.test_scores[1]:>10.2f}"
			f"{student.test_scores[2]:>10.2f}{student.average:>11.2f}{student.grade:>8}"
		)
	print("-" * 96)


def display_statistics(students):
	if not students:
		print("No student records available for statistics.")
		return
	averages = [student.average for student in students]
	print("\nClass Statistics")
	print(f"Highest average: {max(averages):.2f}")
	print(f"Lowest average:  {min(averages):.2f}")
	print(f"Class average:   {sum(averages) / len(averages):.2f}")


def search_students(students):
	search_name = input("Enter a name to search for: ").strip().casefold()
	matches = [student for student in students if search_name in student.name.casefold()]
	if matches:
		display_students(matches)
	else:
		print("No matching student found.")


def show_menu():
	print("\nStudent Grade Calculator")
	print("1. Add student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search for a student")
	print("5. Save records")
	print("Press ESC or type 'ESC' to exit")


def main():
	students = load_students()
	print(f"Loaded {len(students)} student record(s).")

	while True:
		show_menu()
		choice = input("Select an option: ")
		if choice == "\x1b" or choice.strip().casefold() in {"esc", "exit"}:
			save_students(students)
			print("Records saved. Goodbye!")
			break
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_students(students)
		elif choice == "5":
			if save_students(students):
				print("Student records saved successfully.")
		else:
			print("Invalid option. Please choose 1-5 or ESC.")


if __name__ == "__main__":
	main()


