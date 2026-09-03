import re
from pathlib import Path
from typing import Dict, Any
from helper_functions import get_student_data, get_valid_matric_no, get_valid_text_from_user,get_integer_input_from_user, should_continue

class StudentManagement:
    def __init__(self, department: str):
        student_data_dir = Path(__file__).parent / "students_data_dir"
        student_data_dir.mkdir(parents=True, exist_ok=True)
        self.filename = student_data_dir / f'{department.lower()}-students.txt'
        self._students_data = self._load_student_data()

    def add_student(self) -> None:
        data = get_student_data()
        self._save_student_to_db(data)
        print("Student data created.")

    def get_student(self) -> Dict[str, Any] | None:
        key = get_valid_matric_no()
        entry = self._search_student(key)
        if entry is None:
            print(f'{key} not a registered student.')
            return
        line = 50 * '*'
        print(line)
        print('\t\tStudent Information')
        print(line)
        print(entry)
        return

    def delete_student(self) -> None:
        key = get_valid_matric_no()
        entry = self._students_data.pop(key, None)

        if entry is None:
            print("Matric Number not recognized.")
            return
        self._save_students_data(self._students_data)
        print("Student Entry deleted.")
        return
    
    def _search_student(self, key: str) -> Dict[str, Any] | None:
        return self._students_data.get(key)
    
    def _save_students_data(self, data):
        text = "*name|age|course|phone|email|department|matric_no\n"
        for entry in data:
            line = self._format_students_data_as_txt(entry)
            text += line
        text.strip('\n')
        self.filename.write_text(text)

    def _format_students_data_as_txt(self, data) -> str:
        line = f"{data.get('name', '')}|{data.get('age', '')}|{data.get('course', '')}|{data.get('phone', '')}|{data.get('email', '')}|{data.get('department', '')}|{data.get('matric-no', '')}\n"
        return line

    def _save_student_to_db(self, data):
        line = self._format_students_data_as_txt(data)
        with open(self.filename, 'a') as f:
            f.write(line)

    def _format_students_data_to_dict(self, filename: Path) -> Dict[str, Any]:
        data = {}
        with filename.open('r') as f:
            for line in f:
                if '*' in line:
                    continue
                name, age, course, phone, email, dept, mat_no = line.strip().split('|')
                keys = ['name', 'age', 'course', 'phone', 'email', 'department', 'matric-no']

                entry = dict.fromkeys(keys)
                entry['name'] = name
                entry['age'] = age
                entry['course'] = course
                entry['phone'] = phone
                entry['email'] = email
                entry['department'] = dept
                entry['matric-no'] = mat_no

                data[mat_no] = entry
        return data

    def _load_student_data(self) -> Dict[str, Any]:
        if not self.filename.exists() or (not self.filename.read_text()):
            self.filename.write_text("*name|age|course|phone|email|department|matric-no\n")
            return {}
        
        return self._format_students_data_to_dict(self.filename)

def student_file_system_handler():
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
    dept_management = StudentManagement(department)
    response_map = {
        1: dept_management.add_student,
        2: dept_management.get_student,
        3: dept_management.delete_student,
        5: ''
    }
    while True:
        response = get_integer_input_from_user(f'{options}:> ')
        if response not in response_map:
            print('Please select a valid input value')
            continue
        if response == 5:
            break
        function_to_call = response_map[response]
        function_to_call()

        if not should_continue():
            break

if __name__ == '__main__':
    student_file_system_handler()