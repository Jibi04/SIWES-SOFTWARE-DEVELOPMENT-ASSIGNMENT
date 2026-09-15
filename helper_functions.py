import random
from datetime import datetime, UTC
from typing import Literal
from models import User, Book
from validators import validate_four_digit


def should_continue(msg='Would you like to do anything else? ') -> bool:
    while True:
        response = input( msg + '(1 - YES, 0 - NO): ')
        if (not response.isdigit()) or (int(response) not in (1, 0)):
            print("Invalid Response")
            continue

        return int(response) == 1

def get_contact_card(data: dict[str, str]):
    line = 50 * '*'
    contact_card = f"""
{line}
Full Name: {data.get('firstname', '')} {data.get('lastname', '')}
Email: {data.get('email', '')}
Phone: {data.get('phone', '')}
{line}
"""
    return contact_card

def generate_matric_no() -> str:
    return f's/{datetime.now(UTC).year}/{random.randrange(1000, 9999)}'

def generate_account_number():
    number = str(datetime.now().year)[2:] + str(random.randrange(10000000, 99999999))
    return number

def is_valid_pin(user_pin: str) -> bool:
    for trial in range(1, 5):
        attempts_remaining = 4 - trial
        response = validate_four_digit("enter 4 digit pin: ")
        if response == user_pin:
            return True
        if attempts_remaining > 0:
            print(f'you have {attempts_remaining} attempt(s) left.')
        else:
            print("Incorrect pin, No more attempts.")
    return False

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

def is_available(book: Book) -> tuple[bool, int]:
    copies_available = book.copies - book.borrow_count
    return copies_available > 0, copies_available

def format_for_print(books: dict[str, Book], header='Available Books') -> str:
    line = 50 * '*'
    text = f"""
{line}
\t\t{header}
{line}\n
"""
    for book in books.values():
        text += f"Author: {book.author.capitalize()}\tBook Name: {book.name.capitalize()}\tCopies Available: {book.copies - book.borrow_count}\n"
    return text
