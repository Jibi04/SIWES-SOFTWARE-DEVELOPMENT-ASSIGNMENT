import json
from pathlib import Path
from dataclasses import dataclass
from validators import get_valid_text_from_user, get_integer_input_from_user
from helper_functions import should_continue
from exceptions import ExpenseRepositoryError
from typing import TypedDict

class Expense(TypedDict):
    expense: str
    size: int
    price_per_one: int

@dataclass
class ExpenseEntry:
    expense: str
    size: int
    price_per_one: int

    @property
    def total(self):
        return self.price_per_one * self.size

    @property
    def as_dict(self) -> Expense:
        return {"expense": self.expense, "size": self.size, "price_per_one": self.price_per_one}

class ExpenseRepository:
    def __init__(self):
        self._setup_repo()
        self._expense_entries: dict[int, ExpenseEntry] = self.load_file()

    def _setup_repo(self) -> None:
        parentpath = Path(__file__).parent.resolve()
        parentpath.mkdir(exist_ok=True)
        self._filepath = parentpath/'.expense_tracker.json'

    def load_file(self) -> dict[int, ExpenseEntry]:
        if not self._filepath.exists():
            self._setup_repo()
            return {}
        try:
            expenses = json.loads(str(self._filepath.read_text(encoding='utf-8')))
            return self.format_as_dict(expenses)
        except json.JSONDecodeError:
            return {}

    def format_as_dict(self, expenses: dict[int, Expense]) -> dict[int, ExpenseEntry]:
        expenses_ = {}
        for key, expense in expenses.items():
            try:
                expenses_[int(key)] = ExpenseEntry(**expense)
            except (ValueError, TypeError):
                print("Corrupted line skipping.")
                continue
        return expenses_

    def format_for_save(self, expenses: dict[int, ExpenseEntry]):
        data = {
            key:  expense.as_dict 
            for key, expense in expenses.items()
            }
        return json.dumps(data, indent=4)

    def remove_expense(self, expense_id: int) -> None:
        if expense_id not in self._expense_entries:
            raise ValueError(f"Invalid Expense ID: {expense_id}")
        del self._expense_entries[expense_id]
        self.save_expenses(self._expense_entries)

    def add_expense(self, expense: ExpenseEntry) -> None:
        last_known_key = next(reversed(self._expense_entries.keys()), 0)
        new_key = last_known_key + 1
        self._expense_entries[new_key] = expense
        self.save_expenses(self._expense_entries)

    def save_expenses(self, expenses: dict[int, ExpenseEntry]) -> None:
        try:
            data = self.format_for_save(expenses=expenses)
            self._filepath.write_text(data, encoding="utf-8")
        except OSError as e:
            raise ExpenseRepositoryError(e)
        
    @property
    def expenses(self) -> dict[int, ExpenseEntry]:
        return self._expense_entries.copy()

class ExpenseService:
    def __init__(self):
        self.expense_repo = ExpenseRepository()

    def add_expense(self, expense: ExpenseEntry) -> None:
        if not isinstance(expense, ExpenseEntry):
            raise TypeError(f"Expense must be an expense entry.")
        return self.expense_repo.add_expense(expense)

    def remove_expense(self, expense_id: int) -> None:
        return self.expense_repo.remove_expense(expense_id=expense_id)

    def total_expenses(self) -> int:
        total = 0
        for entry in self.expense_repo.expenses.values():
            total += entry.total
        return total

    def get_expenses(self) -> dict[int, ExpenseEntry]:
        return self.expense_repo.expenses

def add_expense_ui(expense_service: ExpenseService) -> None:
    expense_name = get_valid_text_from_user("Expense Name: ")
    expense_amount = get_integer_input_from_user("Expense size: ")
    price_per_one = get_integer_input_from_user("Price per one: ")

    entry = ExpenseEntry(expense=expense_name, size=expense_amount, price_per_one=price_per_one)
    try:
        expense_service.add_expense(entry)
        print("Expense Added!")
    except ExpenseRepositoryError as e:
        print(e)
        return
    
def remove_expense_ui(expense_service: ExpenseService) -> None:
    expense_id = get_integer_input_from_user("ExpenseID: ")
    try:
        expense_service.remove_expense(expense_id)
        print("Expense Removed!")
    except (ExpenseRepositoryError, ValueError) as e:
        print(e)
        return
    
def view_expenses_ui(expense_service: ExpenseService) -> None:
    expenses = expense_service.get_expenses()
    line = "******************************** MENU ********************************\n"
    for expense_id, expense in expenses.items():
        line += format_expense_entry_for_print(expense_id, expense)
    line += f"GRAND TOTAL: ${expense_service.total_expenses()}"
    print(line)

def calculate_total_ui(expense_service: ExpenseService) -> None:
    total = expense_service.total_expenses()
    print(f"Total Expenses: ${total}")

def format_expense_entry_for_print(expense_id, expense: ExpenseEntry) -> str:
    return f"""
Expense ID: {expense_id}
Expense: {expense.expense}
Size: {expense.size}
Price Per One: ${expense.price_per_one}
Expense-Total: ${expense.total}
**************************************************\n
    """


def expense_tracker():
    line = 40 * '*'
    options = f"""
Hi, what would you like to do?
(1) - Add new Expense
(2) - Remove Expense
(3) - View Expenses
(4) - Calculate Total
(q) - exit
"""
    print(line)
    print('\t\tMENU\t\t')
    print(line)
    
    response_map = {
        1: add_expense_ui,
        2: remove_expense_ui,
        3: view_expenses_ui,
        4: calculate_total_ui,
    }

    expense_service = ExpenseService()
    while True:
        response = input(f"{options}:> ").lower().strip()
        if response == 'q':
            break
        elif (not response.isdigit()) or (int(response) not in response_map):
            print("Invalid Response")
            continue
        else:
            function_to_call = response_map[int(response)]
            function_to_call(expense_service)
            if not should_continue():
                break

if __name__ == "__main__":
    try:
        expense_tracker()
    except KeyboardInterrupt:
        print("\nUser Exited")