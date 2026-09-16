import random
from datetime import datetime, UTC

from validators import get_valid_text_from_user, get_integer_input_from_user, get_book_profile, get_and_validate_email, validate_name_input
from helper_functions import should_continue, format_for_print, is_available
from exceptions import BorrowedoutError, NotEnoughCopies, IsBorrowedBookError
from models import BorrowerProfile1, BorrowRecord, Book


class LibraryManagement:
    def __init__(self):
        self.book_management = BookManagement()
        self.borrower_profiles: dict[str, BorrowerProfile1] = {}

    def add_book(self, name: str, author: str, book_count: int) -> str:
        book = self.book_management.get_book_by_name_and_author(name=name, author=author)
        if book:
            # Book instance already exists increase copies count
            self.book_management.add_to_library(book.book_id, copies_to_add=book_count)
        else:
            book_id = 'B-' + str(random.randrange(1000, 9999))
            book = Book(book_id=book_id, name=name, author=author, total_copies=book_count)
            self.book_management.add_book(book)
        return book.book_id
    def delete_book(self, book_id: str) -> str:
        if not self.book_management.get_book_by_id(book_id=book_id):
            raise ValueError(f"Invalid book ID.")
        self.book_management.delete_book(book_id)
        return book_id
    
    def borrow_book(self, name: str, author: str, borrow_count: int, borrower_profile: BorrowerProfile1) -> str:
        book = self.book_management.get_book_by_name_and_author(name=name, author=author)
        if book is None:
            raise ValueError(f"'{name}' by '{author}' not in our database.")

        status, copies_available = is_available(book)
        if not status:
            raise BorrowedoutError(f"Sorry '{name}' by '{author}' is all borrowed out.")
        elif borrow_count > copies_available:
            raise NotEnoughCopies(copies_available=copies_available)

        self.book_management.borrow_book(book.book_id, borrow_count)
        if book.book_id in borrower_profile.active_borrowings:
            borrower_profile.active_borrowings[book.book_id].copies_borrowed += borrow_count
        else:
            borrower_profile.active_borrowings[book.book_id] = BorrowRecord(
                book_id = book.book_id,
                copies_borrowed=borrow_count,
                date_borrowed=datetime.now(UTC).isoformat()
            )

        self.borrower_profiles[borrower_profile.user_id] = borrower_profile
        return book.book_id
    
    def return_book(self, user_id: str, book_id: str) -> None:
        user = self.borrower_profiles.get(user_id)
        if user is None:
            raise ValueError("Invalid UserID")
        if book_id not in user.active_borrowings:
            raise ValueError("Invalid BookID")
        
        self.book_management.return_book(book_id, user.active_borrowings[book_id].copies_borrowed)
        del user.active_borrowings[book_id]
        if not user.active_borrowings:
            del self.borrower_profiles[user_id]
            return
        self.borrower_profiles[user_id] = user
    
    def search_library(self, key) -> dict[str, Book]:
        books = self.book_management.find_book(key)
        if not books:
            raise ValueError(f"No books match '{key}'.")
        return books
    def books_available(self) -> dict[str, Book]:
        return self.book_management.get_books()
    
    def validate_user_input(self, user_id: str, book_id: str) -> BorrowerProfile1:
        user = self.borrower_profiles.get(user_id)
        if user is None:
            raise ValueError(f"Invalid User ID: '{user_id}'")
        
        return user

    def get_profile_if_exists(self, email: str) -> BorrowerProfile1 | None:
        for profile in self.borrower_profiles.values():
            if profile.email == email:
                return profile
        return 
    
class BookManagement:
    def __init__(self):
        self._book_database: dict[str, Book] = {}

    def get_book_by_id(self, book_id: str) -> Book | None:
        return self._book_database.get(book_id)
    def add_book(self, book: Book) -> str:
        book_id = book.book_id
        self._book_database[book_id] = book
        return book_id
    def get_book_by_name_and_author(self, name: str, author: str) -> Book | None:
        for book in self._book_database.values():
            if (name.lower() in book.name.lower()) and (author.lower() in book.author.lower()):
                return book
        return
    def delete_book(self, book_id: str) -> bool:
        book = self._book_database.get(book_id)
        if book is None:
            raise ValueError(f"Invalid bookID: '{book_id}'")

        if not book.borrow_count == 0:
            raise IsBorrowedBookError(f"{book.borrow_count} copies of {book_id} are not yet returned, cannot complete delete operation.")
        
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
        return self._book_database.copy()
    def add_to_library(self, book_id, copies_to_add: int):
        book = self._book_database.get(book_id)
        if book is None:
            raise ValueError(f"Invalid book ID: '{book_id}'")
        book.total_copies += copies_to_add
        self._book_database[book.book_id] = book


def add_book_ui(library: LibraryManagement) -> None:
    name = get_valid_text_from_user("Book Name: ")
    author = get_valid_text_from_user("Author: ")
    book_count = get_integer_input_from_user("Copies to add: ")

    book_id = library.add_book(name=name, author=author, book_count=book_count)
    print(f"Book Added: bookID '{book_id}'")
def delete_book_ui(library: LibraryManagement) -> None:
    book_id = input("BookID: ")
    try:
        library.delete_book(book_id)
        print("Sucess!!")
    except ValueError as e:
        print(e)
    except IsBorrowedBookError as e:
        print(e)
def borrow_book_ui(library: LibraryManagement) -> None:
    email = get_and_validate_email()
    borrower_profile = library.get_profile_if_exists(email)
    name, author, borrow_count = get_book_profile()
    if borrower_profile is None:
        borrower_name = validate_name_input("Your name: ")
        user_id = "U-" + str(random.randrange(1000, 9999))
        borrower_profile = BorrowerProfile1(name=borrower_name, email=email, user_id=user_id)
    try:
        book_id = library.borrow_book(name=name, author=author, borrow_count=borrow_count, borrower_profile=borrower_profile)
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
    print(f"Success!!\nYour BorrwerID: '{borrower_profile.user_id}'\nBookID: '{book_id}'")
def return_book_ui(library: LibraryManagement) -> None:
    user_id = get_valid_text_from_user("User ID: ").upper()
    book_id = get_valid_text_from_user("Book ID: ").upper()
    try:
        library.return_book(user_id=user_id, book_id=book_id)
        print("Success!!")
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