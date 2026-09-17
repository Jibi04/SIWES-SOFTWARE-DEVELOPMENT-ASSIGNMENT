import re
from datetime import datetime, UTC
from typing import Literal
from models import Student, ClientProfile

def get_integer_input_from_user(msg: str) -> int:
    while True:
        res = input(f'{msg}')
        if not res.isdigit():
            print('Please input a valid Integer greater than zero.')
            continue
        integer_res = int(res)
        if integer_res <= 0:
            print('Please select a valid number greater than zero.')
            continue
        return integer_res
def get_birth_year() -> int:
    while True:
        res = get_integer_input_from_user(msg='Birth year: ')
        if (1905 >= res) or (res >= datetime.now(UTC).year):
            print('Invalid birth year')
            continue
        return res
def get_valid_age() -> int:
    res = get_birth_year()
    return (datetime.now().year - int(res))
def get_floating_input_from_user(msg: str, allow_zero: bool = False) -> float:
    while True:
        try:
            res = float(input(f'{msg}'))
            if res <= 0:
                if allow_zero:
                    return res
                print('Please input a valid decimal value greater than 0.0')
                continue
            return float(res)
        except ValueError:
            print('Please input a valid decimal value greater than 0.0')
            continue
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
def validate_name_input(msg: str) -> str:
    while True:
        name = input(msg).strip()
        pattern = re.compile(r"^[A-Za-z'_\s]+$")
        if not pattern.fullmatch(name):
            print("Please input a valid Name.")
            continue
        return name
def get_valid_matric_no() -> str:
    while True:
        mat_no = get_valid_text_from_user(msg='Matric NO: ')
        if not re.fullmatch(r's/\d{4}/\d{4}$', mat_no):
            print('Invalid Matric No.')
            continue
        return mat_no
def get_valid_text_from_user(msg: str = '') -> str:
    while True:
        response = input(f'{msg}').strip()
        if not response:
            print("Field is empty.")
            continue
        pattern = re.compile(r"^[0-9\w'\.]+$")
        if not pattern.fullmatch(response):
            print("Please Input a valid text.")
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
def get_and_validate_11_digit_phone(msg='Phone No: ') -> str:
    while True:
        res = input(f'{msg}').strip()
        if not res.isdigit():
            print(f'Invalid Phone number.')
            continue
        if len(res) != 11:
            print(f'Invalid Phone number')
            continue
        return res
def validate_client_amt(msg: str) -> int:
    while True:
        try:
            amt = int(input(f'{msg}'))
        except ValueError:
            print('Please, Input a valid Amount greater than $0.00')
            continue
        if amt <= 0:
            print('Please, Input a valid Amount greater than $0.00')
            continue
        return amt
def get_and_validate_email() -> str:
    while True:
        res = get_valid_text_from_user('Email: ')
        pattern = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+$")
        if not pattern.fullmatch(res):
            print('Invalid Email Address')
            continue
        return res
def validate_account_number_input(msg='Account Number: '):
    while True:
        acct_no = input(msg).strip()
        if not acct_no.isdigit() or (not len(acct_no) == 10):
            print('Invalid Account number. (ctrl-c to quit)')
            continue
        return acct_no
def validate_account_type_input() -> Literal['current', 'savings']:
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
def get_book_profile():
    name = validate_name_input("Book Name: ")
    author = validate_name_input("Author: ")
    borrow_count = get_integer_input_from_user("Copies to borrow: ")
    return (name, author, borrow_count)
def get_user_profile() -> ClientProfile:
    return{
        "firstname": validate_name_input('First Name: '),
        "lastname": validate_name_input('Last Name: '),
        "email": get_and_validate_email(),
        "nationality": validate_name_input("Nationality: "),
        "birthyear": get_birth_year(),
        "phone": get_and_validate_11_digit_phone(),
    }
def get_student_data() -> Student:
    return {
        'name': validate_name_input('Student Name: '), 
        'age': get_valid_age(), 
        'major': validate_name_input('Major: '), 
        'phone': get_and_validate_11_digit_phone(), 
        'email': get_and_validate_email(),
        'matric_no': '',
    }
def get_contact_info():
    return {
        'firstname': validate_name_input('First Name: '),
        'lastname': validate_name_input('Last Name: '),
        'phone': get_and_validate_11_digit_phone(),
        'email': get_and_validate_email()
    }
