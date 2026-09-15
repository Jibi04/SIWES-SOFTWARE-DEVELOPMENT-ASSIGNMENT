import random
from datetime import datetime, UTC

from validators import get_valid_text_from_user, get_integer_input_from_user, get_borrower_profile
from helper_functions import should_continue, format_for_print, is_available
from exceptions import BorrowedoutError, NotEnoughCopies
from models import BorrowerProfile, Book


class LibraryManagement:
    def __init__(self):
        self.book_management = BookManagement()
        self.borrower_profiles: dict[str, BorrowerProfile] = {}

    def add_book(self, name: str, author: str, book_count: int) -> str:
        book = self.book_management.get_book(name=name, author=author)
        if book:
            # Book instance already exists increase copies count
            self.book_management.add_to_library(book.book_id, copies=book_count)
        else:
            book_id = 'B-' + str(random.randrange(1000, 9999))
            book = Book(book_id=book_id, name=name, author=author, copies=book_count)
            self.book_management.add_book(book)
        return book.book_id
    def delete_book(self, name: str, author: str) -> str:
        if not (book:=self.book_management.get_book(name=name, author=author)):
            raise ValueError(f"Invalid key parameters Name: '{name}' Author: '{author}' .")
        self.book_management.delete_book(book.book_id)
        return book.book_id
    def borrow_book(self, name: str, author: str, borrow_count: int, borrower_profile: dict[str, str]) -> str:
        book = self.book_management.get_book(name=name, author=author)
        if book is None:
            raise ValueError(f"'{name}' by '{author}' not in our database.")

        status, copies_available = is_available(book)
        if not status:
            raise BorrowedoutError(f"Sorry '{name}' by '{author}' is all borrowed out.")
        elif borrow_count > copies_available:
            raise NotEnoughCopies(copies_available=copies_available)

        self.book_management.borrow_book(book.book_id, borrow_count)
        client_profile = {'book_id': book.book_id, 'borrow_count': borrow_count, 'date_borrowed': datetime.now(UTC)}
        for k, v in client_profile.items():
            borrower_profile[k] = v
        profile = BorrowerProfile(**borrower_profile)
        self.borrower_profiles[profile.user_id] = profile
        return book.book_id
    def return_book(self, user_id) -> str:
        user = self.validate_user_input(user_id=user_id)
        self.book_management.return_book(user.book_id, user.borrow_count)
        del self.borrower_profiles[user_id]
        return user_id
    def search_library(self, key) -> dict[str, Book]:
        books = self.book_management.find_book(key)
        if not books:
            raise ValueError(f"No books match '{key}'.")
        return books
    def books_available(self) -> dict[str, Book]:
        return self.book_management.get_books()
    def validate_user_input(self, user_id: str) -> BorrowerProfile:
        user = self.borrower_profiles.get(user_id)
        if user is None:
            raise ValueError(f"Invalid User ID: '{user_id}'")
        book = self.book_management.get_book(book_id=user.book_id)
        if book is None:
            raise ValueError(f"Invalid Book ID: '{user.book_id}'")
        return user
    
class BookManagement:
    def __init__(self):
        self._book_database: dict[str, Book] = {}

    def add_book(self, book: Book) -> str:
        book_id = book.book_id
        self._book_database[book_id] = book
        return book_id
    def get_book(self, name: str | None = None, author: str | None = None, book_id: str | None = None) -> Book | None:
        if book_id:
            return self._book_database.get(book_id)

        if name is None:
            raise ValueError("Name parameter cannot be None.")
        if author is None:
            raise ValueError("Author parameter cannot be None.")
        
        for book in self._book_database.values():
            if (name in book.name) and (author in book.author):
                return book
        return
    def delete_book(self, book_id: str) -> bool:
        if book_id not in self._book_database:
            raise ValueError(f"Invalid bookID: '{book_id}'")
        del self._book_database[book_id]
        return True
    def borrow_book(self, book_id: str, borrow_count: int = 1) -> str:
        book = self._book_database.get(book_id)
        if book is None:
            raise ValueError(f"Invalid Book ID '{book_id}'.")

        _, copies_available = is_available(book=book)
        if borrow_count > copies_available:
            raise NotEnoughCopies(msg=f"Not enough copies in the database.", copies_available=copies_available)

        book.borrow_count += borrow_count
        self._book_database[book.book_id] = book
        return book_id
    def return_book(self, book_id: str, borrow_count: int) -> str:
        book = self._book_database.get(book_id)
        if book is None:
            raise ValueError(f"Invalid book ID: {book_id}")
        if borrow_count > book.borrow_count:
            raise ValueError(f"Book-Return Overload, copies to return exceed amount of books owned by Library.")

        book.borrow_count -= borrow_count
        self._book_database[book_id] = book
        return book_id
    def find_book(self, name) -> dict[str, Book]:
        matches = {}
        for book in self._book_database.values():
            if (name in book.name) or (name in book.author):
                matches[book.book_id] = book

        return matches
    def get_books(self) -> dict[str, Book]:
        return self._book_database
    def add_to_library(self, book_id, copies: int):
        book = self._book_database.get(book_id)
        if book is None:
            raise ValueError(f"Invalid book ID: '{book_id}'")
        book.copies += copies
        self._book_database[book.book_id] = book


def add_book_ui(library: LibraryManagement) -> None:
    name = get_valid_text_from_user("Book Name: ")
    author = get_valid_text_from_user("Author: ")
    book_count = get_integer_input_from_user("Copies to add: ")

    book_id = library.add_book(name=name, author=author, book_count=book_count)
    print(f"Book Added: bookID '{book_id}'")
def delete_book_ui(library: LibraryManagement) -> None:
    name = get_valid_text_from_user("Name: ")
    author = get_valid_text_from_user("Author: ")
    try:
        library.delete_book(name=name, author=author)
    except ValueError as e:
        print(e)
def borrow_book_ui(library: LibraryManagement) -> None:
    borrower_name, user_id, name, email, author, borrow_count = get_borrower_profile()
    borrower_profile = {
        'name': borrower_name,
        'email': email,
        'user_id': user_id 
        }
    try:
        library.borrow_book(name=name, author=author, borrow_count=borrow_count, borrower_profile=borrower_profile)
        print(f"your borrwerID: '{user_id}'")
    except BorrowedoutError as e:
        print(e)
        return
    except NotEnoughCopies as e:
        print(e)
        if not should_continue(msg="Would you like to take the available copies? "):
            return
        borrow_count = e.copies_available
        library.borrow_book(name=name, author=author, borrow_count=borrow_count, borrower_profile=borrower_profile)
    except ValueError as e:
        print(e)
        return
def return_book_ui(library: LibraryManagement) -> None:
    user_id = get_valid_text_from_user("User ID: ").upper()
    try:
        library.return_book(user_id=user_id)
    except ValueError as e:
        print(e)
        return
def search_library_ui(library: LibraryManagement) -> None:
    key = get_valid_text_from_user("Book name or Author: ")
    try:
        books = library.search_library(key)
        payload = format_for_print(books=books, header=f"Books that match '{key}'")
        print(payload)
    except ValueError as e:
        print(e)
        return
def library_menu_ui(library: LibraryManagement) -> None:
    books = library.books_available()
    payload = format_for_print(books=books, header="Books in the Library.")
    print(payload)

def library_management_system():
    line = 40 * '*'
    options = f"""
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
    lib_manager = LibraryManagement()

    response_map = {
        1: add_book_ui,
        2: borrow_book_ui,
        3: return_book_ui,
        4: search_library_ui,
        5: library_menu_ui,
        6: delete_book_ui,
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
            response = func_to_call(lib_manager)
            if not should_continue():
                break
    
if __name__ == '__main__':
    try:
        library_management_system()
    except KeyboardInterrupt:
        print("\nUser Exited.")