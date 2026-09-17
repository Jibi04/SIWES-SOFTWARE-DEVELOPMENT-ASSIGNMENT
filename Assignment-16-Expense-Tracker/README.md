### Expense Tracker

A simple CLI-based expense tracker built with Python.

The application allows users to add, view, remove, and calculate expenses. Expenses are stored locally in a JSON file so that they persist between program runs.

#### Features

Add an expense

View expenses

Remove an expense

Calculate total expenses

Store expenses in a JSON file

Basic input validation and error handling

Project Structure
expense-tracker/
│
├── expense_tracker.py

#### How It Works

The application is separated into different responsibilities:

UI — Handles user interaction through the command line.

Service — Contains the application's business logic.

Repository — Handles loading and saving expenses.

ExpenseEntry — Represents an individual expense.

Expenses are currently stored in a JSON file

#### Requirements
Python 3.9+

No external packages are required beyond the project's own modules.

#### Running the Application

Clone or download the project, then run:

python -m Assignment-16-Expense-Tracker.expense_tracker


Follow the menu prompts to manage your expenses.

#### Example
(1) - Add new Expense
(2) - Remove Expense
(3) - View Expenses
(4) - Calculate Total
(q) - exit

#### Purpose
This project was built as a learning project to practice:

Python

Object-Oriented Programming

Dataclasses

Type hints

File handling

JSON persistence

Exception handling

Separation of concerns

Basic software architecture