import re


class Student:
    """
    Represents a single student with their details, courses, and balance.
    """

    def __init__(self, student_id, name, email):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.courses = {}  # Dictionary to store courses and their fees
        self.balance = 0  # Total balance for registered courses

    def enroll_course(self, course):
        """
        Enroll the student in a course and update the balance.
        """
        if course.course_id in self.courses:
            print(f"{self.name} is already enrolled in {course.name}.")
        else:
            self.courses[course.course_id] = course.name
            self.balance += course.fee
            print(f"{self.name} has been enrolled in {course.name}. Fee: ${course.fee}")

    def __str__(self):
        """
        String representation of the Student.
        """
        courses = ", ".join(self.courses.values()) if self.courses else "None"
        return f"ID: {self.student_id}, Name: {self.name}, Email: {self.email}, Balance: ${self.balance}, Courses: {courses}"


class Course:
    """
    Represents a single course with its details.
    """

    def __init__(self, course_id, name, fee):
        self.course_id = course_id
        self.name = name
        self.fee = fee

    def __str__(self):
        """
        String representation of the Course.
        """
        return f"Course ID: {self.course_id}, Name: {self.name}, Fee: ${self.fee}"


class RegistrationSystem:
    """
    Manages the registration of students and courses.
    """

    def __init__(self):
        self.students = {}  # Dictionary to store Student objects with student_id as the key
        self.courses = []  # List to store Course objects

    def add_course(self):
        """
        Adds a new course to the system.
        """
        while True:
            course_id = input("Enter Course ID (alphanumeric, max 10 characters): ")
            if not re.match("^[a-zA-Z0-9]{1,10}$", course_id):
                print("Course ID must be alphanumeric and up to 10 characters long.")
                continue
            if self.find_course_by_id(course_id):
                print(f"Course ID {course_id} already exists.")
                continue
            break

        course_name = input("Enter Course Name: ")
        while True:
            try:
                course_fee = float(input("Enter Course Fee: "))
                if course_fee < 500:
                    raise ValueError("Fee cannot be less than $500.")
                break
            except ValueError as e:
                print(f"Error: {e}. Please enter a valid course fee.")

        new_course = Course(course_id, course_name, course_fee)
        self.courses.append(new_course)
        print(f"Course '{course_name}' added successfully!")

    def find_course_by_id(self, course_id):
        """
        Finds and returns a course by its ID.
        """
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None

    def show_courses(self):
        """
        Displays all available courses.
        """
        if not self.courses:
            print("No courses available.")
        else:
            print("\nAvailable Courses:")
            for course in self.courses:
                print(course)

    def register_student(self):
        """
        Adds a new student to the system with input validation.
        """
        while True:
            student_id = input("Enter Student ID (alphanumeric, max 15 characters): ")
            if not re.match("^[a-zA-Z0-9]{1,15}$", student_id):
                print("Student ID should be alphanumeric, 15 characters max.")
                continue
            if student_id in self.students:
                print(f"Error: Student ID {student_id} already exists.")
                continue
            break

        while True:
            name = input("Enter Student Name (letters and spaces only, max 50 characters): ")
            if not re.match("^[a-zA-Z ]+$", name):
                print("Error: Name must contain only letters and spaces.")
                continue
            if len(name) > 50:
                print("Error: Name must not exceed 50 characters.")
                continue
            break

        while True:
            email = input("Enter Student Email (valid format, max 30 characters): ")
            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                print("Error: Email must be in a valid format (e.g., user@example.com).")
                continue
            if len(email) > 30:
                print("Error: Email must not exceed 30 characters.")
                continue
            break

        new_student = Student(student_id, name, email)
        self.students[student_id] = new_student
        print(f"Student {name} added successfully!")

    def find_student(self, student_id):
        """
        Finds a student by their ID.
        """
        return self.students.get(student_id)

    def enroll_in_course(self):
        """
        Enrolls a student in a course by their ID.
        """
        student_id = input("Enter Student ID: ")
        student = self.find_student(student_id)
        if not student:
            print(f"Student with ID {student_id} not found.")
            return

        course_id = input("Enter Course ID to Enroll: ")
        course = self.find_course_by_id(course_id)
        if not course:
            print(f"Course ID {course_id} not found. Please add the course first.")
            return
        student.enroll_course(course)

    def show_registered_students(self):
        """
        Displays all students in the system.
        """
        if not self.students:
            print("No students in the system.")
        else:
            print("\nList of Students:")
            for student in self.students.values():
                print(student)

    def list_students_in_course(self):
        """
        Lists all students enrolled in a specific course by Course ID.
        """
        course_id = input("Enter the Course ID: ")
        course = self.find_course_by_id(course_id)

        if not course:
            print(f"Course with ID {course_id} not found.")
            return

        enrolled_students = [
            student for student in self.students.values() if course_id in student.courses
        ]

        if not enrolled_students:
            print(f"No students are enrolled in the course '{course.name}' (ID: {course_id}).")
        else:
            print(f"\nStudents enrolled in '{course.name}' (ID: {course_id}):")
            for student in enrolled_students:
                print(f"- {student.name} (ID: {student.student_id})")

    def check_student_balance(self):
        """
        Displays the current balance of a specific student using their student ID.
        """
        student_id = input("Enter Student ID: ")
        student = self.find_student(student_id)

        if not student:
            print(f"Student with ID {student_id} not found.")
            return

        print(f"\n{student.name}'s Current Balance: ${student.balance:.2f}")

    def calculate_payment(self):
        """
        Processes a student's payment.
        """
        student_id = input("Enter Student ID: ")
        student = self.find_student(student_id)

        if not student:
            print(f"Student with ID {student_id} not found.")
            return

        if student.balance == 0:
            print(f"{student.name} has no outstanding balance.")
            return

        print(f"\n{student.name}'s Current Balance: ${student.balance}")
        required_payment = student.balance * 0.4
        print(f"Minimum payment required to confirm registration: ${required_payment:.2f}")

        while True:
            try:
                payment = float(input("Enter payment amount: "))
                if payment < required_payment:
                    print(f"Payment must be at least ${required_payment:.2f}.")
                elif payment > student.balance:
                    print(f"Payment cannot exceed the outstanding balance of ${student.balance:.2f}.")
                else:
                    break
            except ValueError:
                print("Please enter a valid payment amount.")

        student.balance -= payment
        print(f"Payment of ${payment:.2f} processed. Remaining balance: ${student.balance:.2f}")

        if student.balance == 0:
            print(f"{student.name} has fully paid for their courses. Registration confirmed!")
        else:
            print(f"Registration is partially confirmed. Remaining balance: ${student.balance:.2f}")


# Example of how the system might be run
if __name__ == "__main__":
    regsys = RegistrationSystem()
    while True:
        print("\n1. Add Student")
        print("2. Add Course")
        print("3. Enroll Student in a Course")
        print("4. List Students in a Course")
        print("5. Process Payment")
        print("6. Check Student Balance")
        print("7. show all registered students")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            regsys.register_student()
        elif choice == "2":
            regsys.add_course()
        elif choice == "3":
            regsys.enroll_in_course()
        elif choice == "4":
            regsys.list_students_in_course()
        elif choice == "5":
            regsys.calculate_payment()
        elif choice == "6":
            regsys.check_student_balance()
        elif choice == "7":
            regsys.show_registered_students()
        elif choice == "8":
            print("Exiting the system. Goodbye!")
            break

