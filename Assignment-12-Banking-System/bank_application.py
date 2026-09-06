import time
from typing import Dict
from helper_functions import validate_account_number, get_valid_user_profile, generate_account_number, User, should_continue, validate_client_amt, get_integer_input_from_user, get_floating_input_from_user, get_valid_transaction_pin, get_valid_account_type, messenger, validate_four_digit

USERS_DATABASE: Dict[str, User] = {}

def create_account():
    new_user = get_valid_user_profile()
    account_name = str(new_user.get('firstname', '')) + str(new_user.get('lastname', ''))
    acct_type = get_valid_account_type()
    acct_no = generate_account_number()
    transaction_pin = get_valid_transaction_pin()
    user = User(
        account_name=account_name, 
        account_number=acct_no, 
        account_type=acct_type, 
        transaction_pin=transaction_pin, 
        **new_user
        )
    USERS_DATABASE[acct_no] = user

    return messenger(status=True, msg=f'\nAccount Created.\nYour Account Details\naccount number: {user.account_number}\naccount name: {user.account_name}\naccount type: {user.account_type}\n')

def bank_app():
    while True:
        response = get_integer_input_from_user('(1) - Create Account\n(2) - Already have an account\n(3) - Quit\n:> ')
        if response == 1:
            res = create_account()
            msg = res.get('message', '')
            print(msg)
        elif response == 2:
            acct_no = validate_account_number()
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
    available_balance = user.available_balance
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
                print(f'Your available balance: ${float(available_balance)}')
                if not should_continue():
                    break
            elif response == 2:
                deposit(user)
            elif response == 3:
                withdraw(user)
            elif response == 4:
                transfer(user)
            if not should_continue():
                break

def deposit(user: User):
    available_balance = user.available_balance
    while True:
        amt = validate_client_amt('Amount to Deposit: ')
        available_balance+=amt
        user.available_balance = available_balance
        simulate_processing()
        print(f'${amt} Deposited.')
        print(f'Your new available balance is ${available_balance}')
        break

def transfer(user: User):
    available_balance = user.available_balance
    while True:
        acct_no = validate_account_number('Recipient Account Number, (ctrl+c to quit): ')
        recipient = USERS_DATABASE.get(acct_no)

        if recipient is None:
            if not should_continue(msg="Invalid account number: would you like to retry transaction?"):
                break
            continue

        amt = validate_client_amt('Amount to transfer: ')
        print(f"You are about to send '${amt}' to '{recipient.account_name}' Validate transaction by inputing your 4 digit transaction pin")
        if not is_valid_pin(user.transaction_pin):
            return
        
        if amt > available_balance:
            print('Insufficient Balance.')
            continue
        available_balance-=amt
        recipient.available_balance += amt
        user.available_balance = available_balance
        
        simulate_processing()
        print(f'Success.\nAvailable balance: ${available_balance}')
        break

def withdraw(user: User):
    available_balance = user.available_balance
    while True:
        amt = validate_client_amt('How much would like to withdraw?: ')
        if amt > available_balance:
            print("Insufficient Account Balance")
            if not should_continue(msg='Would you like to try again?'):
                break
        available_balance-=amt
        user.available_balance = available_balance
        simulate_processing()
        print(f'${amt} Debited\nYour new available balance is ${available_balance}')
        break

def is_valid_pin(user_pin: str) -> bool:
    for trial in range(1, 4):
        msg = '4 digit pin: '
        if trial > 1:
            msg = f'you have {4 - trial} attempts left.'

        response = validate_four_digit(msg)
        if response == user_pin:
            return True
        error_msg = "Incorrect pin"
        if trial == 4:
            error_msg = "trials exhausted."
        print(error_msg)

    return False

def simulate_processing():
    print('Processing...')
    time.sleep(.7)

if __name__ == '__main__':
    bank_app()