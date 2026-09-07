import re
import random
from datetime import datetime
from typing import Any, Literal, Dict
from dataclasses import dataclass

@dataclass
class User:
    firstname: str
    lastname: str
    birthyear: int
    nationality: str
    email: str
    phone: str
    account_number: str 
    transaction_pin: str
    available_balance: int = 0
    account_name: str | None = None
    account_type: Literal['savings', 'current'] = 'savings'

def validate_four_digit(msg: str) -> str:
    while True:
        response = input(msg).strip()
        if not response.isdigit():
            print("Invalid input, please select 4 digit integers only")
            continue
        if len(response) != 4:
            print("Invalid input, must be 4 digits")
            continue
        return response

def get_valid_transaction_pin() -> str:
    while True:
        response1 = validate_four_digit(msg="4 digit transaction pin: ")
        response2 = validate_four_digit(msg="Confirm 4 digit transaction pin: ")

        if response1 != response2:
            print("transaction pin does not match please try again.")
            continue
        return response1

def get_valid_email() -> str:
    while True:
        res = get_valid_text_from_user('Email: ')
        if '@' not in res:
            print(f'Invalid Email address')
            continue

        pattern = r'\.([a-z]{2,3})$'
        pattern = re.compile(pattern=pattern)
        if not pattern.search(res):
            print('Invalid Email Address')
            continue
        return res

def get_valid_phone(msg='Phone No: ') -> str:
    while True:
        res = input(f'{msg}').strip().lower()
        if not res.isdigit():
            print(f'Invalid Phone number.')
            continue
        if len(res) != 11:
            print(f'Invalid Phone number')
            continue
        return res
    
def get_floating_input_from_user(msg: str) -> float:
    while True:
        try:
            res = float(input(f'{msg}'))
            if res <= 0:
                print('Please input a valid integer greater than zero.')
                continue
            return float(res)
        except ValueError:
            print('Please input a valid integer or decimal.')
            continue

def get_integer_input_from_user(msg: str) -> int:
    while True:
        res = input(f'{msg}')
        if not res.isdigit():
            print('Please input a valid Integer value')
            continue
        integer_res = int(res)
        if integer_res <= 0:
            print('Please select a valid integer greater than zero.')
            continue
        return integer_res

def validate_client_amt(msg: str) -> int:
    while True:
        try:
            amt = int(input(f'{msg}'))
        except ValueError:
            print('Please, Input a valid Amount greater than $0.00')
            continue
        if amt <= 0:
            print('Invalid ammount')
            continue
        return amt

def get_birth_year() -> str:
    while True:
        res = get_integer_input_from_user(msg='Birth year: ')
        if (1905 >= res) or (res >= datetime.now().year):
            print('Invalid birth year')
            continue
        return str(res)
    
def get_valid_age() -> int:
    res = get_birth_year()
    return (datetime.now().year - int(res))

def should_continue(msg='Would you like to do anything else?'):
    while True:
        response = input( msg + '(1 - YES, 0 - NO): ')
        if (not response.isdigit()) or (int(response) not in (1, 0)):
            print("Invalid Response")
            continue

        return int(response)

def get_contact_info():
    return {
        'firstname': get_valid_text_from_user('First Name: '),
        'lastname': get_valid_text_from_user('Last Name: '),
        'phone': get_valid_phone(),
        'email': get_valid_email()
    }

def get_contact_card(data: dict[str, Any]):
    line = 50 * '*'
    contact_card = f"""
{line}
Full Name: {data.get('firstname', '')} {data.get('lastname', '')}
Email: {data.get('email', '')}
Phone: {data.get('phone', '')}
{line}
"""
    return contact_card

def get_student_data():
    return {
        'name': get_valid_text_from_user('Student Name: '), 
        'age': get_valid_age(), 
        'course': get_valid_text_from_user('Course: '), 
        'phone': get_valid_phone(), 
        'email': get_valid_email(),
        'department': get_valid_text_from_user('Department: '),
        'matric-no': get_valid_matric_no(),
    }

def get_valid_text_from_user(msg: str = '') -> str:
    while True:
        response = input(f'{msg}').strip().lower()
        if not response:
            print("Field is empty.")
            continue
        return response

def get_valid_matric_no() -> str:
    while True:
        mat_no = get_valid_text_from_user(msg='Matric NO: ')
        if re.search(r's\d{4}$', mat_no) is None:
            print('Invalid Matric No.')
            continue
        return mat_no

def get_valid_user_profile():
    return dict(
        firstname = get_valid_text_from_user('First Name: '),
        lastname = get_valid_text_from_user('Last Name: '),
        birthyear = get_birth_year(),
        nationality = get_valid_text_from_user("Nationality: "),
        email= get_valid_email(),
        phone= get_valid_phone(),
        ) 

def generate_account_number():
    number = str(datetime.now().year)[2:] + str(random.randrange(10000000, 99999999))
    return number

def get_valid_account_type() -> Literal['current', 'savings']:
    acct_type_map = {
        1: 'savings',
        2: 'current',
        3: 'savings'
    }

    while True:
        acct_type = get_integer_input_from_user('Account-Type: (1-savings, 2-current, 3-default): ')
        if not acct_type in acct_type_map:
            print("Please enter a valid response.")
            continue
        return acct_type_map[acct_type]

def user_to_dict(user: User):
    return {
        'firstname': user.firstname,
        'lastname': user.lastname,
        'birthyear': user.birthyear,
        'nationality': user.nationality,
        'email': user.email,
        'phone': user.phone,
        'acct-name': user.account_name,
        'acct-no': user.account_number,
        'acct-type': user.account_type,
    }

def validate_account_number(msg='Account Number: '):
    while True:
        acct_no = get_valid_text_from_user(msg)
        if not acct_no.isdigit() or (not len(acct_no) == 10):
            print('Invalid Account number. (ctrl-c to quit)')
            continue
        return acct_no

def messenger(status: bool, msg: str, payload: Any = None) -> Dict[str, bool | str]:
    return {
        'status': status,
        'message': msg,
        'payload': payload
    }