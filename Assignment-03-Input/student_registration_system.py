def student_registration_system():
    line = 50 * '='

    name = input('Student Name: ').lower().strip()
    age = get_user_values('Age: ')
    school = input('school: ').lower().strip()
    department = input('Department: ').lower().strip()
    email = validate_email()
    phone = input('phone no: ')

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
            res = input(f'{msg} ')
            val = float(res)
            return val
        except ValueError:
            print(f'Invalid Value expected an Integer/Decimal but got \'{type(res).__name__}\'')
            continue
        
if __name__ == '__main__':
    student_registration_system()