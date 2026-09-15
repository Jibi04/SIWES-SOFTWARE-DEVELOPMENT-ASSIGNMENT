from pathlib import Path
from typing import Literal
from validators import get_student_data, get_valid_matric_no, get_valid_text_from_user,get_integer_input_from_user
from helper_functions import generate_matric_no,  should_continue
from models import Student
from exceptions import StudentRepositoryError, StudentNotFoundError
from repository import write_as_batch, write_single_file,  format_students_data_to_dict

class StudentRepository:
    def __init__(self, department: str):
        self.department = department
        self._setup_file()
        self.students_data: dict[str, Student] = self._load_student_data()

    def _setup_file(self) -> None:
        student_data_dir = Path(__file__).parent / "students_data_dir"
        student_data_dir.mkdir(parents=True, exist_ok=True)
        department = self.department.replace(' ', '_').lower()
        self.filename = student_data_dir / f'{department}_students.txt'

    def _load_student_data(self) -> dict[str, Student]:
        if not self.file_exists_and_not_empty():
            try:
                text = "*name|age|major|phone|email|matric_no\n"
                self.filename.write_text(text)
                return {}
            except OSError as error:
                raise StudentRepositoryError(f"Unable to load student data: {error}")
        
        return format_students_data_to_dict(self.filename)

    def file_exists_and_not_empty(self) -> bool:
        if not self.filename.exists():
            return False
        return self.filename.stat().st_size > 0

    def write_to_file(self, mode: Literal['a', 'w'], data) -> None:
        type_of_write = {
            'a': write_single_file,
            'w': write_as_batch,
        }

        if mode not in type_of_write:
            raise ValueError(f"Invalid file mode. '{mode}'")
        try:
            func_to_call = type_of_write[mode]
            return func_to_call(filename=self.filename, data=data)
        except OSError as error:
            raise StudentRepositoryError(f"Unable to save student data: {error}")

    def search_student(self, key: str) -> Student | None:
        return self.students_data.get(key)

    def save_students_to_db(self, data) -> None:
        return self.write_to_file(mode='w', data=data)

    def save_student_to_db(self, data) -> None:
        self.write_to_file(data=data, mode='a')
        self.update_student_data()

    def delete_student_data(self, key: str) -> None:
        students = self.students_data.copy()
        if key not in self.students_data:
            raise StudentNotFoundError(f"Invalid Matric Number: '{key}'")
        
        del self.students_data[key]
        self.save_students_to_db(self.students_data)
        self.update_student_data()
    
    def update_student_data(self) -> None:
        self.students_data = self._load_student_data()

class StudentService:
    def __init__(self, department: str):
        self.student_repo = StudentRepository(department)

    def add_student(self, data: Student) -> str:
        while True:
            matric_no = generate_matric_no()
            if self.student_repo.search_student(matric_no) is None:
                break

        data['matric_no'] = matric_no
        
        status = self.student_repo.save_student_to_db(data)
        return matric_no

    def get_student(self, key: str) -> Student:
        entry = self.student_repo.search_student(key)
        if entry is None:
            raise StudentNotFoundError(f'{key} not a registered student.')
        return entry
        
    def delete_student(self, key: str) -> None:
        if self.student_repo.search_student(key) is None:
            raise StudentNotFoundError(f"Invalid Matric No: {key}")
        self.student_repo.delete_student_data(key)
        

def add_student_ui(management: StudentService) -> None:
    data = get_student_data()
    try:
        matric_no = management.add_student(data)
        print(f"Your Matric No is '{matric_no}'")
        return
    except StudentRepositoryError as e:
        print(e)

def get_student_ui(management: StudentService) -> None:
    key = get_valid_matric_no()
    try:
        student_entry = management.get_student(key)
    except StudentNotFoundError as e:
        print(e)
        return
    except StudentRepositoryError as e:
        print(e)
    
    line = 50 * '*'
    print(line)
    print('\t\tStudent Information')
    print(line)
    print(student_entry)
    return

def delete_student_ui(management: StudentService) -> None:
    key = get_valid_matric_no()
    try:
        management.delete_student(key)
        print("Student data deleted.")
    except StudentNotFoundError as e:
        print(e)
        return
    except StudentRepositoryError as e:
        print(e)

def student_file_system_handler() -> None:
    line = 40 * '*'
    options = f"""
    Hi, what would you like to do today?
(1) - Add new student
(2) - Get student data
(3) - Delete student data
(5) - exit
"""
    print(line)
    print('\t\tMENU\t\t')
    print(line)

    department = get_valid_text_from_user(msg='Department: ')
    try:
        dept_management = StudentService(department)
    except StudentRepositoryError as error:
        print(f"Error: {error}")
        return
    
    response_map = {
        1: add_student_ui,
        2: get_student_ui,
        3: delete_student_ui,
    }
    while True:
        response = get_integer_input_from_user(f'{options}:> ')
        if response == 5:
            break
        if response not in response_map:
            print('Please select a valid input value')
            continue
        function_to_call = response_map[response]
        function_to_call(dept_management)

        if not should_continue():
            break

if __name__ == '__main__':
    try:
        student_file_system_handler()
    except KeyboardInterrupt:
        print("\nUser Exited.")
        