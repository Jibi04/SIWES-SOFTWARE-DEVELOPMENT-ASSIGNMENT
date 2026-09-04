import random
from dataclasses import dataclass
from typing import Dict
from helper_functions import get_valid_text_from_user, get_integer_input_from_user, should_continue

@dataclass
class Book:
    id: str
    name: str
    author: str
    book_count: int # How many copies of this book does the library have
    borrowed_count: int = 0 # How many copies of this book has been borrowed

class LibraryManager:
    def __init__(self):
        self.book_management = BookManager()

    def add_book(self) -> None:
        name = get_valid_text_from_user("Book Name: ")
        author = get_valid_text_from_user("Author: ")
        book_count = get_integer_input_from_user("Copies to add: ")
        if not book_count > 0:
            print("Operation Failed")
            return
        
        id = 'B-' + str(random.randrange(1000, 9999))

        book: Book = Book(id=id, name=name, author=author, book_count=book_count)

        self.book_management.add_book(book)
        print(f"'{book.name}' by '{book.author}' added to library.")
        return
        
    def return_book(self) -> None:
        name = get_valid_text_from_user("Book Name: ")
        self.book_management.return_book(name)
        return
    
    def borrow_book(self) -> None:
        name = get_valid_text_from_user("Book Name: ")
        if not self.book_management.availibility_status(name):
            print(f"Sorry we don't have '{name}' in store.")
            return
        copies = get_integer_input_from_user("How many copies: ")
        self.book_management.borrow_book(name, copies)
        return

    def delete_book(self) -> None:
        name = get_valid_text_from_user("Book Name: ")
        self.book_management.delete_book(name)
        return

    def available_books(self) -> None:
        books = self.book_management.get_books()
        if not books:
            print("There are no available books at this time.")
            return
        format_and_print(books)
        return
    
    def search_book(self) -> None:
        name = get_valid_text_from_user("Book name or Author: ")
        books = self.book_management.find_book(name)
        format_and_print(books=books, header=f"Books that match '{name}'")
        return

class BookManager:
    def __init__(self):
        self._available_books: Dict[str, Book] = {}

    def add_book(self, book: Book) -> None:
        book_instance = self._available_books.get(book.name)
        if book_instance is None:
            self._available_books[book.name] = book
            return
        
        book_instance.book_count += book.book_count
        self._available_books[book_instance.name] = book_instance
        return

    def borrow_book(self, name, required_copies: int = 1) -> None:
        status = self.availibility_status(name)
        if not status:
            print(f"'{name}' not available.")
            return 

        book = self._available_books[name]
        copies_available = book.book_count - book.borrowed_count

        if required_copies > copies_available:
            while True:
                res = get_integer_input_from_user(f"There are only {copies_available} copies available\n(1) - get available copies\n(2) - Quit\n:> ")
                if res not in (1, 2):
                    print('please select a valid option')
                    continue
                if res == 2:
                    return
                required_copies = copies_available
                break

        book.borrowed_count += required_copies
        self._available_books[name] = book
        print(f"Request to borrow {required_copies} copies of '{book.name.capitalize()}' by '{book.author.capitalize()}' has been approved, please go to counter to get your book.")
        return 
    
    def return_book(self, name) -> None:
        if name not in self._available_books:
            print(f"'{name}' not recognized")
            return 

        book = self._available_books[name]
        if not book.borrowed_count > 0:
            print(f"Sorry the copy of '{book.name}' by '{book.author}' in your possession isn't ours.")
            return
        book.borrowed_count -=1
        self._available_books[name] = book
        print(f"'{name}' returned.")
        return

    def get_books(self) -> Dict[str, Dict[str, str | int]]:
        books = {}
        for book in self._available_books.values():
            books[book.id] = format_book_for_print(book)
        return books
    
    def availibility_status(self, name) -> bool:
        book_instance = self._available_books.get(name)
        if book_instance is None:
            return False
        return (book_instance.book_count - book_instance.borrowed_count) > 0

    def delete_book(self, name):
        if name not in self._available_books:
            print(f"'{name}' not recognized.")
            return
        book = self._available_books.pop(name)
        print(f"'{book.name}' by '{book.author}' deleted.")
        return

    def find_book(self, name: str | None = None, author: str | None =None) -> Dict[str, Dict[str, str | int]]:
        key = name or author or ''

        matches = {}
        for book in self._available_books.values():
            if (key in book.author) or (key in book.name):
                matches[book.id] = format_book_for_print(book)
        return matches

def format_book_for_print(book: Book) -> Dict[str, str | int]:
    return {
        'author': book.author,
        'book-name': book.name,
        'copies-available': book.book_count - book.borrowed_count
    }

def format_and_print(books: Dict[str, Dict[str, str | int]], header='Available Books') -> None:
    line = 50 * '*'
    print(line)
    print(f'\t\t{header}')
    print(line)
    print()
    for book in books.values():
        author, book_name, copies_available = book.get('author', ''), book.get('book-name', ''), book.get('copies-available', '')
        row = f"""
Author: {author.capitalize()}\tBook Name: {book_name.capitalize()}\tCopies Available: {copies_available}
"""
        print(row)

def library_management_system():
    line = 40 * '*'
    options = f"""\n
    Hi, what would you like to do today?
(1) - Add Book
(2) - Borrow Book
(3) - Return Book
(4) - Search Book
(5) - View Available Books
(6) - Delete Book
(q) - exit
"""
    print(line)
    print('\t\tMENU\t\t')
    print(line)
    lib_manager = LibraryManager()

    response_map = {
        1: lib_manager.add_book,
        2: lib_manager.borrow_book,
        3: lib_manager.return_book,
        4: lib_manager.search_book,
        5: lib_manager.available_books,
        6: lib_manager.delete_book,
        'q': '',
    }

    while True:
        response = get_valid_text_from_user(f'{options}:> ')
        if response == 'q':
            break
        elif not response.isdigit():
            print("Please Select a valid option.")
        else:
            option = int(response)
            if option not in response_map:
                print("Please select a valid option")
                continue
            func_to_call = response_map[option]
            func_to_call()
            if not should_continue():
                break

if __name__ == '__main__':
    library_management_system()