from pathlib import Path
from typing import Literal
from helper_functions import get_student_data, get_valid_matric_no, generate_matric_no, get_valid_text_from_user,get_integer_input_from_user, should_continue, Student

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
        if not self.validate_file_content():
            try:
                text = "*name|age|major|phone|email|matric_no\n"
                self.filename.write_text(text)
                return {}
            except PermissionError:
                raise IncompleteOperationError(f"Permission Error: '{self.filename}'")
            except OSError as error:
                raise IncompleteOperationError(f"Unable to load student data: {error}")
        
        return format_students_data_to_dict(self.filename)

    def validate_file_content(self) -> bool:
        if not self.filename.exists():
            return False
        return self.filename.stat().st_size > 0

    def write_to_file(self, mode: Literal['a', 'w'], data) -> bool:
        type_of_write = {
            'a': write_single_file,
            'w': write_as_batch,
        }

        if mode not in type_of_write:
            raise ValueError(f"Invalid file mode. '{mode}'")
        try:
            func_to_call = type_of_write[mode]
            return func_to_call(filename=self.filename, data=data)
        except PermissionError:
            raise IncompleteOperationError(f"""
            Unable to save student data:
            Permission error '{self.filename}'
            """)
        except OSError as error:
            raise IncompleteOperationError(f"Unable to save student data: {error}")

    def search_student(self, key: str) -> Student | None:
        return self.students_data.get(key)

    def save_students_to_db(self, data) -> bool:
        return self.write_to_file(mode='w', data=data)

    def save_student_to_db(self, data) -> bool:
        return self.write_to_file(data=data, mode='a')

    def delete_student_data(self, key: str) -> bool:
        students = self.students_data.copy()
        if key not in self.students_data:
            return False
        
        del self.students_data[key]
        status = self.save_students_to_db(self.students_data)

        if not status:
            self.students_data = students
            return False
        return True

    def update_student_data(self) -> None:
        self.students_data = self._load_student_data()

class StudentManagement:
    def __init__(self, department: str):
        self.student_repo = StudentRepository(department)
        self.students_data = self.student_repo.students_data

    def add_student(self, data: Student) -> str:
        while True:
            matric_no = generate_matric_no()
            if self.student_repo.search_student(matric_no) is None:
                break

        data['matric_no'] = matric_no
        
        status = self.student_repo.save_student_to_db(data)
        if not status:
            raise ValueError("Error: Unable to complete save.")
        self.student_repo.update_student_data()
        return matric_no

    def get_student(self, key: str) -> Student:
        entry = self.student_repo.search_student(key)
        if entry is None:
            raise ValueError(f'{key} not a registered student.')
        return entry
        
    def delete_student(self, key: str) -> None:
        if self.student_repo.search_student(key) is None:
            raise ValueError(f"Invalid Matric No: {key}")
        self.student_repo.update_student_data()


def write_single_file(filename: Path, data) -> bool:
    line = format_students_data_as_txt(data)
    with open(filename, 'a') as f:
        f.write(line)
    return True

def write_as_batch(filename: Path, data) -> bool:
    text = "*name|age|major|phone|email|matric_no\n"
    for entry in data.values():
        line = format_students_data_as_txt(entry)
        text += line
    filename.write_text(text)
    return True

def format_students_data_as_txt(data) -> str:
    line = f"{data['name']}|{data['age']}|{data['major']}|{data['phone']}|{data['email']}|{data['matric_no']}\n"
    return line

def format_students_data_to_dict(filename: Path) -> dict[str, Student]:
    data = {}
    with filename.open('r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.strip().split('|')
            if line.startswith('*'):
                continue
            elif len(parts) != 6:
                print("Corrupted line skipping...")
                continue
            name, age, major, phone, email, mat_no = parts
            data[mat_no]={
                'name': name,
                'age': age,
                'major': major,
                'phone': phone,
                'email': email,
                'matric_no': mat_no
            }

    return data
    

def add_student_ui(management: StudentManagement) -> None:
    data = get_student_data()
    try:
        matric_no = management.add_student(data)
        print(f"Your Matric No is '{matric_no}'")
        return
    except ValueError:
        print("Unable to create student Data at the moment.")
        return
    except IncompleteOperationError as e:
        print(f"Unable to create student data.\n{str(e)}")

def get_student_ui(management: StudentManagement) -> None:
    key = get_valid_matric_no()
    try:
        student_entry = management.get_student(key)
    except ValueError:
        print(f"'{key}' not a registered Student.")
        return
    except IncompleteOperationError as e:
            print(f"Unable to create student data.\n{str(e)}")
    
    line = 50 * '*'
    print(line)
    print('\t\tStudent Information')
    print(line)
    print(student_entry)
    return

def delete_student_ui(management: StudentManagement) -> None:
    key = get_valid_matric_no()
    try:
        management.delete_student(key)
        print("Student data deleted.")
    except ValueError as e:
        print(str(e))
        return
    except IncompleteOperationError as e:
            print(f"Unable to create student data.\n{str(e)}")


class IncompleteOperationError(Exception):...

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
        dept_management = StudentManagement(department)
    except IncompleteOperationError as error:
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
        