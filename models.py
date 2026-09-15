from dataclasses import dataclass
from typing import TypedDict, Literal

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

class ClientProfile(TypedDict):
    firstname: str
    lastname: str
    birthyear: str
    nationality: str
    email: str
    phone: str
    
class Student(TypedDict):
    name: str
    age: int
    phone: str
    email: str
    major: str
    matric_no: str

@dataclass
class Book:
    book_id: str
    name: str
    author: str
    copies: int
    borrow_count: int = 0

@dataclass
class BorrowerProfile:
    name: str
    email: str
    user_id: str
    book_id: str
    borrow_count: int
    date_borrowed: str