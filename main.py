import csv
import argparse
import logging

logging.basicConfig(filename='logger.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger()


class Validate:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.name, value)

    def validate(self, value):
        if not value.replace(' ', '').isalpha() or not value.istitle():
            logger.error("ФИО должно состоять только из букв и начинаться с заглавной буквы")
            raise ValueError('ФИО должно состоять только из букв и начинаться с заглавной буквы')


class Student:
    name = Validate()
    """
    Атрибуты:
    - name (str): ФИО студента
    - subjects (dict): словарь, содержащий предметы и их оценки и результаты тестов
    """

    def __init__(self, name, subjects_file):
        """
        __init__(self, name, subjects_file): Конструктор класса.
        Принимает имя студента и файл с предметами и их результатами.
        Инициализирует атрибуты name и subjects и вызывает метод load_subjects для загрузки предметов из файла.
        """
        self.name = name
        self.subjects = {}
        self.load_subjects(subjects_file)

    def __setattr__(self, name, value):
        """
        __setattr__(self, name, value): Дескриптор, который проверяет установку атрибута name.
        Убеждается, что name начинается с заглавной буквы и состоит только из букв.
        """
        if name == "name":
            if not value.replace(' ', '').isalpha() or not value.istitle():
                logger.error("ФИО должно состоять только из букв и начинаться с заглавной буквы")
                raise ValueError('ФИО должно состоять только из букв и начинаться с заглавной буквы')
        super.__setattr__(self, name, value)

    def __getattr__(self, name):
        """
        __getattr__(self, name): Позволяет получать значения атрибутов предметов
        (оценок и результатов тестов) по их именам."""
        if name in self.subjects:
            return self.subjects[name]
        else:
            raise AttributeError(f"Предмет {name} не найден")

    def __str__(self):
        """__str__(self): Возвращает строковое представление студента, включая имя и список предметов."""
        return f"Студент: {self.name}\nПредметы: {', '.join(self.subjects.keys())}"

    def load_subjects(self, subjects_file):
        """
        load_subjects(self, subjects_file): Загружает предметы из файла CSV.
        Использует модуль csv для чтения данных из файла и добавляет предметы в атрибут subjects.
        """
        with open(subjects_file, 'r', encoding="utf8", newline='\n') as f:
            reader = csv.reader(f, delimiter=' ', quotechar=',')
            for row in reader:
                subject = row[0]
                if subject not in self.subjects:
                    self.subjects[subject] = {'grades': [], 'test_scores': []}

    def add_grade(self, subject, grade):
        """
        add_grade(self, subject, grade): Добавляет оценку по заданному предмету.
        Убеждается, что оценка является целым числом от 2 до 5.
        """
        if subject not in self.subjects:
            self.subjects[subject] = {'grades': [], 'test_scores': []}
        if not isinstance(grade, int) or grade < 2 or grade > 5:
            logger.warning("Оценка должна быть целым числом от 2 до 5")
            raise ValueError("Оценка должна быть целым числом от 2 до 5")
        self.subjects[subject]['grades'].append(grade)

    def add_test_score(self, subject, test_score):
        """
        add_test_score(self, subject, test_score): Добавляет результат теста по заданному предмету.
        Убеждается, что результат теста является целым числом от 0 до 100.
        """
        if subject not in self.subjects:
            self.subjects[subject] = {'grades': [], 'test_scores': []}
        if not isinstance(test_score, int) or test_score < 0 or test_score > 100:
            logger.warning("Результат теста должен быть целым числом от 0 до 100")
            raise ValueError("Результат теста должен быть целым числом от 0 до 100")
        self.subjects[subject]['test_scores'].append(test_score)

    def get_average_test_score(self, subject):
        """get_average_test_score(self, subject): Возвращает средний балл по тестам для заданного предмета."""
        if subject not in self.subjects.keys():
            logger.error(f'Предмет {subject} не найден')
            raise ValueError(f"Предмет {subject} не найден")
        test_scores = self.subjects[subject]['test_scores']
        if len(test_scores) == 0:
            return 0
        return sum(test_scores) / len(test_scores)

    def get_average_grade(self):
        """get_average_grade(self): Возвращает средний балл по всем предметам."""
        total_grades = []
        for subject in self.subjects.keys():
            grades = self.subjects[subject]['grades']
            if len(grades) > 0:
                total_grades.extend(grades)
        if len(total_grades) == 0:
            return 0
        return sum(total_grades) / len(total_grades)


def main():
    parser = argparse.ArgumentParser(description='My first argument parser')
    parser.add_argument('file_name', metavar='N', type=str, nargs='*', help='press some filename')
    args = parser.parse_args()
    logger.info(f'В скрипт передано: {args}')
    if args.file_name:
        file_name_csv = args.file_name[0]
        logger.info(f'Переданное имя файла: {args.file_name[0]}')
    else:
        file_name_csv = "subjects.csv"
        logger.info(f'Аргументы не переданы(имя файла по умолчанию): {file_name_csv}')

    student = Student("Иван Иванов", file_name_csv)

    student.add_grade("Математика", 4)
    student.add_test_score("Математика", 85)

    student.add_grade("История", 5)
    student.add_test_score("История", 92)

    average_grade = student.get_average_grade()
    logger.info(f"Средний балл: {average_grade}")

    average_test_score = student.get_average_test_score("Математика")
    logger.info(f"Средний результат по тестам по математике: {average_test_score}")

    logger.info(student)


if __name__ == "__main__":
    main()
