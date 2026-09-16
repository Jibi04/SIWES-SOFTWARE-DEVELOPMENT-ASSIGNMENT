import time
from helper_functions import  generate_account_number, should_continue, is_valid_pin
from validators import validate_account_number_input, get_user_profile, validate_client_amt, get_integer_input_from_user, get_valid_transaction_pin, validate_account_type_input
from models import User
from exceptions import InsufficientBalanceError

USERS_DATABASE: dict[str, User] = {}

def create_account_ui():
    new_user = get_user_profile()
    account_type = validate_account_type_input()
    transaction_pin = get_valid_transaction_pin()
    while True:
        account_no = generate_account_number()
        if account_no not in USERS_DATABASE:
            break

    user = User(
        **new_user,
        account_name=f"{new_user.get('firstname').capitalize()} {new_user.get('lastname').capitalize()}",
        account_number=account_no,
        account_type=account_type,
        transaction_pin=transaction_pin,
    )
    create_account(user)
    print(f"""
******************* Account Details **********************
Account Name: {user.account_name}
Account Number: {user.account_number}
Account Type: {user.account_type}
""")

def create_account(user: User):
    USERS_DATABASE[user.account_number] = user
    return True

def bank_app():
    while True:
        response = get_integer_input_from_user('(1) - Create Account\n(2) - Already have an account\n(3) - Quit\n:> ')
        if response == 1:
            create_account_ui()
        elif response == 2:
            acct_no = validate_account_number_input()
            if acct_no not in USERS_DATABASE:
                print('Invalid Account Number.')
                continue
            user_info = USERS_DATABASE[acct_no]
            atm_machine(user_info)
        elif response == 3:
            break
        else:
            print('Invalid Response')

    print(f'Thank you for banking with us.')
def atm_machine(user: User):
    print(f"Welcome {user.firstname.capitalize()},")

    while True:
        response = input('What would you like to do?\n(1) - check balance\n(2) - deposit\n(3) - withdraw\n(4) - transfer\n(q) - back\n:> ')
        if response.lower() == 'q':
            break
        if not response.isdigit():
            print("Invalid Input value, (q - to Quit): ")
            continue
        response = int(response)
        if response not in (1, 2, 3, 4):
            print('Invalid response, (q - to Quit): ')
            continue
        else:
            if response == 1:
                simulate_processing()
                print(f'Your available balance: ${float(user.available_balance)}')
            elif response == 2:
                deposit_ui(user)
            elif response == 3:
                withdraw_ui(user)
            elif response == 4:
                transfer_ui(user)
            if not should_continue():
                break

def deposit_ui(user: User):
    while True:
        amt = validate_client_amt('Amount to Deposit: ')
        deposit(user, amt)
        simulate_processing()
        print(f"""
${amt} Deposited.
You available balance is ${user.available_balance}""")
        break
def deposit(user: User, amt: int):
    user.available_balance += amt
    return True

def transfer_ui(user: User):
    while True:
        account_no = validate_account_number_input("Recipient Account Number, (ctrl+c to quit): ")
        if account_no == user.account_number:
            print("Error: You cannot Send money to your self.")
            return
        recipient = USERS_DATABASE.get(account_no)
        if recipient is None:
            if not should_continue("Invalid Account Number: Would you like to retry the conversation? "):
                return
            continue
        amt = validate_client_amt("Amount to transfer: ")
        print(f"You are about to transfer ${amt} to {recipient.account_name}, validate transaction by inputing your 4 digit transaction pin.")
        if not is_valid_pin(user.transaction_pin):
            return
        try:
            transfer(sender=user, recipient=recipient, amt=amt)
            simulate_processing()
            print(f"Success.\nYour Available Balance: ${user.available_balance}")
            return
        except InsufficientBalanceError:
            print("Insufficient Balance.")
            return
def transfer(sender: User, recipient: User, amt: int):
    if amt > sender.available_balance:
        raise InsufficientBalanceError('Insufficient Balance.')
    
    sender.available_balance-=amt
    recipient.available_balance += amt

def withdraw_ui(user: User):
    amt = validate_client_amt("How much would you like to withdraw? ")
    if user.available_balance > amt:
        print("Insufficient Balance.")
        return
    withdraw(user=user, amt=amt)
    simulate_processing()
    print(f"${amt} Debited\nYour new available balance is ${user.available_balance}")
def withdraw(user: User, amt: int):
    user.available_balance-=amt
    return

def simulate_processing(timer=.7):
    print('Processing...')
    time.sleep(timer)

if __name__ == '__main__':
    try:
        bank_app()
    except KeyboardInterrupt:
        print("\nUser Exited.")