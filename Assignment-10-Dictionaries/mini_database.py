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
        request = get_user_values(f'{options}:> ')
        if request == 5:
            break
        elif request == 1:
            student_data = get_student_data()
            student_name = student_data.get('name', '').lower()
            DATABASE[student_name] = student_data
            print(f"'{student_name.capitalize()}' added.")
            if should_continue:
                continue
            else: break
        elif request == 2:
            student_name = input('Student Name: ').lower()
            data = DATABASE.get(student_name)
            if data is None:
                print(f"Student not registered.")
            else:
                print(data)

            if should_continue:
                continue
            else: break
        

def get_student_data():
    name = input('Student Name: ')
    age = get_user_values('Age: ')
    course = input('Course: ')
    phone = input('phone no: ')
    email = validate_email()
    return {
        'name': name, 
        'age': int(age), 
        'course': course, 
        'phone': phone, 
        'email': email
    }

def validate_email():
    while True:
        res = input(f'Email: ').lower().strip()
        if '@' not in res:
            print(f'Invalid Email address')
            continue
        return res
    
def get_user_values(msg: str):
    while True:
        try:
            res = input(f'{msg}: ')
            val = float(res)
            return val
        except ValueError:
            print(f'Invalid Value expected an Integer/Decimal but got \'{type(res).__name__}\'')
            continue

def should_continue():
    response = int(input('Would you like to do anything else? (1 - YES, 0 - NO): '))
    return bool(response)

if __name__ == '__main__':
    dictionary_database_system()