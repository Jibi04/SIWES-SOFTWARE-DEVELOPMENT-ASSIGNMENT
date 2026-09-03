import re
from typing import Any

def get_valid_email() -> str:
    while True:
        res = input(f'Email: ').lower().strip()
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
        res = input(f'{msg}')
        if not res.isdigit():
            print('please input a valid integer or decimal')
            continue
        return float(res)

def get_integer_input_from_user(msg: str) -> int:
    while True:
        res = input(f'{msg}')
        
        if not res.isdigit():
            print('Please input a valid Integer value')
            continue
        integer_res = int(res)
        if integer_res < 0:
            print('Please select a valid integer greater than zero.')
        return integer_res

def validate_client_amt(msg: str) -> float:
    while True:
        try:
            amt = float(input(f'{msg}'))
        except ValueError:
            print('Please, Input a valid Integer or Decimal greater than $0.00')
            continue
        if amt <= 0:
            print('Invalid ammount')
            continue
        return amt

def get_valid_age() -> int:
    while True:
        res = get_integer_input_from_user(msg='Age: ') or 0
        if (121 <= res) or (res <= 0):
            print('Invalid age')
            continue
        return res

def should_continue():
    while True:
        response = input('Would you like to do anything else? (1 - YES, 0 - NO): ')
        if (not response.isdigit()) or (int(response) not in (1, 0)):
            print("Invalid Response")
            continue

        return int(response)

def get_contact_info():
    firstname = input('First Name: ').capitalize()
    lastname = input('Last Name: ').capitalize()
    phone = get_valid_phone()
    email = get_valid_email()

    return {
        'firstname': firstname,
        'lastname': lastname,
        'phone': phone,
        'email': email
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