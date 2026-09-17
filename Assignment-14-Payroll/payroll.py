from dataclasses import dataclass, field
from uuid import uuid4, UUID
from validators import get_valid_text_from_user, get_integer_input_from_user, get_floating_input_from_user

@dataclass
class Employee:
    firstname: str
    lastname: str
    salary: int
    tax_pcg: float = 0.0
    bonus: float = 0.0
    employee_id: UUID =  field(default_factory=uuid4)

    @property
    def gross_salary(self) -> float:
        bonus = 0
        if self.bonus > 0:
            bonus = (self.bonus / 100) * self.salary
        return float(self.salary) + bonus

    @property
    def tax(self) -> float:
        return (self.tax_pcg / 100) * self.gross_salary

    @property
    def net_salary(self) -> float:
        return self.gross_salary - self.tax

    @property
    def fullname(self) -> str:
        return f"{self.firstname.capitalize()} {self.lastname.capitalize()}"

def employee_payroll():
    firstname = get_valid_text_from_user("Firstname: ")
    lastname = get_valid_text_from_user("Last Name: ")
    salary = get_integer_input_from_user("Base Salary: ")
    tax = get_floating_input_from_user("Tax Percentage(%): ", allow_zero=True)
    bonus = get_floating_input_from_user("Bonus (%) [if any]: ", allow_zero=True)

    employee = Employee(firstname=firstname, lastname=lastname, salary=salary,  tax_pcg=tax, bonus=bonus)
    data_txt = format_payroll(employee=employee)
    print(data_txt)

def format_payroll(employee: Employee):
    return f"""
Employee ID: {employee.employee_id}
Full Name: {employee.fullname}
Bonus: ${employee.bonus}
Tax: ${employee.tax}
Base Salary: ${employee.salary}
Gross Salary: ${employee.gross_salary}
****************************************************
NET SALARY: {employee.net_salary}
****************************************************
"""

if __name__ == "__main__":
    employee_payroll()