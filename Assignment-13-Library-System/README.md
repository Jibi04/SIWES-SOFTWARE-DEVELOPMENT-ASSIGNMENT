## Library System Manager
This programs automates library tasks such as
- borrow books
- add books to library
- return books
- view currently available books 
- delete books
- search books

#### How to run:
1. install python to your environment
2. create a projects directory and clone this repo
git clone https://github.com/Jibi04/SIWES-SOFTWARE-DEVELOPMENT-ASSIGNMENT
3. go to projects directory and run:

** on Linux **
python3 -m Assignment-13-Library-System.lib_management_system

** on Windows **
python -m Assignment-13-Library-System.lib_management_system

#### Note::
No real data is saved.

USAGE::
****************************************
                MENU
****************************************


    Hi, what would you like to do today?
(1) - Add Book
(2) - Borrow Book
(3) - Return Book
(4) - Search Book
(5) - View Available Books
(6) - Delete Book
(q) - exit
:> 1
Book Name: Verity
Author: Colleen hover
Copies to add: 12
'verity' by 'colleen hover' added to library.
Would you like to do anything else? (1 - YES, 0 - NO): 1


    Hi, what would you like to do today?
(1) - Add Book
(2) - Borrow Book
(3) - Return Book
(4) - Search Book
(5) - View Available Books
(6) - Delete Book
(q) - exit
:> 1
Book Name: The 48 laws of power
Author: Robert Greene
Copies to add: 10
'the 48 laws of power' by 'robert greene' added to library.
Would you like to do anything else? (1 - YES, 0 - NO): 1


    Hi, what would you like to do today?
(1) - Add Book
(2) - Borrow Book
(3) - Return Book
(4) - Search Book
(5) - View Available Books
(6) - Delete Book
(q) - exit
:> 1
Book Name: The Gentlemen
Author: Guy Ritchie
Copies to add: 8
'the gentlemen' by 'guy ritchie' added to library.
Would you like to do anything else? (1 - YES, 0 - NO): 1


    Hi, what would you like to do today?
(1) - Add Book
(2) - Borrow Book
(3) - Return Book
(4) - Search Book
(5) - View Available Books
(6) - Delete Book
(q) - exit
:> 1
Book Name: The odyssey
Author: Christopher Nolan
Copies to add: 23
'the odyssey' by 'christopher nolan' added to library.
Would you like to do anything else? (1 - YES, 0 - NO): 1


    Hi, what would you like to do today?
(1) - Add Book
(2) - Borrow Book
(3) - Return Book
(4) - Search Book
(5) - View Available Books
(6) - Delete Book
(q) - exit
:> 5
**************************************************
                Available Books
**************************************************


Author: Colleen hover   Book Name: Verity       Copies Available: 12


Author: Robert greene   Book Name: The 48 laws of power Copies Available: 10


Author: Guy ritchie     Book Name: The gentlemen        Copies Available: 8


Author: Christopher nolan       Book Name: The odyssey  Copies Available: 23

Would you like to do anything else? (1 - YES, 0 - NO): 1


    Hi, what would you like to do today?
(1) - Add Book
(2) - Borrow Book
(3) - Return Book
(4) - Search Book
(5) - View Available Books
(6) - Delete Book
(q) - exit
:> 2
Book Name: verity
How many copies: 3
Request to borrow 3 copies of 'Verity' by 'Colleen hover' has been approved, please go to counter to get your book.
Would you like to do anything else? (1 - YES, 0 - NO): 1


    Hi, what would you like to do today?
(1) - Add Book
(2) - Borrow Book
(3) - Return Book
(4) - Search Book
(5) - View Available Books
(6) - Delete Book
(q) - exit
:> 2
Book Name: The 48 laws of power
How many copies: 35
There are only 10 copies available
(1) - get available copies
(2) - Quit
:> 2
Would you like to do anything else? (1 - YES, 0 - NO): 1


    Hi, what would you like to do today?
(1) - Add Book
(2) - Borrow Book
(3) - Return Book
(4) - Search Book
(5) - View Available Books
(6) - Delete Book
(q) - exit
:> 4
Book name or Author: 48
**************************************************
                Books that match '48'
**************************************************


Author: Robert greene   Book Name: The 48 laws of power Copies Available: 10

Would you like to do anything else? (1 - YES, 0 - NO): 5
Invalid Response
Would you like to do anything else? (1 - YES, 0 - NO): 1


    Hi, what would you like to do today?
(1) - Add Book
(2) - Borrow Book
(3) - Return Book
(4) - Search Book
(5) - View Available Books
(6) - Delete Book
(q) - exit
:> 6
Book Name: The 48 laws of power
'the 48 laws of power' by 'robert greene' deleted.
Would you like to do anything else? (1 - YES, 0 - NO): 1


    Hi, what would you like to do today?
(1) - Add Book
(2) - Borrow Book
(3) - Return Book
(4) - Search Book
(5) - View Available Books
(6) - Delete Book
(q) - exit
:> 5
**************************************************
                Available Books
**************************************************


Author: Colleen hover   Book Name: Verity       Copies Available: 9


Author: Guy ritchie     Book Name: The gentlemen        Copies Available: 8


Author: Christopher nolan       Book Name: The odyssey  Copies Available: 23

Would you like to do anything else? (1 - YES, 0 - NO): 1


    Hi, what would you like to do today?
(1) - Add Book
(2) - Borrow Book
(3) - Return Book
(4) - Search Book
(5) - View Available Books
(6) - Delete Book
(q) - exit
:> q