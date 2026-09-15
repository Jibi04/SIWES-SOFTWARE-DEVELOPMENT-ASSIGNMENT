
from pathlib import Path
from models import Student

def write_single_file(filename: Path, data: Student) -> None:
    line = format_students_data_as_txt(data)
    with open(filename, 'a') as f:
        f.write(line)

def write_as_batch(filename: Path, data: dict[str, Student]) -> None:
    text = "*name|age|major|phone|email|matric_no\n"
    for entry in data.values():
        line = format_students_data_as_txt(entry)
        text += line
    filename.write_text(text)

def format_students_data_as_txt(data: Student) -> str:
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
            try:
                age = int(age)
            except ValueError:
                print("Skipping Corrupted 'age'.")
                continue
            data[mat_no]={
                'name': name,
                'age': age,
                'major': major,
                'phone': phone,
                'email': email,
                'matric_no': mat_no
            }

    return data
    