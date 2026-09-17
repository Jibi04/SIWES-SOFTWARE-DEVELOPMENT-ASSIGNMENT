from validators import get_and_validate_email, get_and_validate_11_digit_phone, get_valid_age

def student_registration_system():
    line = 50 * '='

    name = input('Student Name: ').lower().strip()
    age = get_valid_age()
    school = input('school: ').lower().strip()
    department = input('Department: ').lower().strip()
    email = get_and_validate_email()
    phone = get_and_validate_11_digit_phone()

    registration_completion_msg = f"""
Welcome {name.capitalize()},
You have successfully registered.

Department: 
{department.capitalize()}

Email: 
{email.capitalize()}
"""
    print(line)
    print("\tSTUDENT REGISTRATION\t")
    print(line)
    print(registration_completion_msg)
if __name__ == '__main__':
    student_registration_system()