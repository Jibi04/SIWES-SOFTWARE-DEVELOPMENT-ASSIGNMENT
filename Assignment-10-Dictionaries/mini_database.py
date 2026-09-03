from helper_functions import get_integer_input_from_user, get_valid_phone, get_valid_age, get_valid_email, should_continue

DATABASE = {}
def dictionary_database_system():
    line = 40 * '*'
    options = f"""
    Hi, what would you like to do today?
(1) - Add student
(2) - Get Student Data
(5) - exit
"""
    print(line)
    print('\t\tMENU\t\t')
    print(line)

    while True:
        request = get_integer_input_from_user(f'{options}:> ')
        if request not in (1, 2, 5):
            print('Please select a valid option')
            continue
        if request == 5:
            break
        elif request == 1:
            student_data = get_student_data()
            student_name = student_data.get('name', '').lower()
            DATABASE[student_name] = student_data
            print(f"'{student_name.capitalize()}' added.")
            if not should_continue():
                break
        elif request == 2:
            student_name = input('Student Name: ').lower()
            data = DATABASE.get(student_name)
            if data is None:
                print(f"Student not registered.")
            else:
                print(data)

            if not should_continue():
                break

def get_student_data():
    name = input('Student Name: ')
    age = get_valid_age()
    course = input('Course: ')
    phone = get_valid_phone()
    email = get_valid_email()
    return {
        'name': name, 
        'age': int(age), 
        'course': course, 
        'phone': phone, 
        'email': email
    }

if __name__ == '__main__':
    dictionary_database_system()