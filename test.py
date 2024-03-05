import pytest
from main import Student


def create_student():
    student = Student("Иван Иванов", "subjects.csv")
    student.add_grade("Математика", 4)
    student.add_test_score("Математика", 85)
    student.add_grade("История", 5)
    student.add_test_score("История", 92)
    return student


def test_employee_full_name():
    student = Student("Иван Иванов", "subjects.csv")
    assert student.name == "Иван Иванов"


def test_get_average_grade():
    student = create_student()
    average_grade = student.get_average_grade()
    assert average_grade == 4.5


def test_average_test_score():
    student = create_student()
    average_test_score = student.get_average_test_score("Математика")
    assert average_test_score == 85.0


def test_str():
    student = create_student()
    assert str(student) == 'Студент: Иван Иванов\nПредметы: Математика, История'


if __name__ == '__main__':
    pytest.main()