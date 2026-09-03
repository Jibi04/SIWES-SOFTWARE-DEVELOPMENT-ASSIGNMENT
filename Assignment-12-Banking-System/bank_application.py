import time
from typing import Dict
from helper_functions import validate_account_number, get_valid_user_profile, generate_account_number, User, should_continue, validate_client_amt, get_integer_input_from_user, get_floating_input_from_user

USERS_DATABASE: Dict[str, User] = {}

def create_account():
    new_user = get_valid_user_profile()
    acct_no = generate_account_number()
    account_name = str(new_user.get('firstname', '')) + str(new_user.get('lastname', ''))
    user = User(account_name=account_name, account_number=acct_no, **new_user)
    USERS_DATABASE[acct_no] = user

    print(f'\nAccount Created.\nYour Account Details\naccount number: {user.account_number}\naccount name: {user.account_name}\naccount type: {user.account_type}\n')

def bank_app():
    while True:
        response = get_integer_input_from_user('(1) - Create New User\n(2) - Already have an account\n(3) - Quit\n:> ')
        if response == 1:
            create_account()
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
                print(f'Your available balance: ${float(available_balance)}')
                if not should_continue():
                    break
            elif response == 2:
                amt = validate_client_amt('Amount to Deposit: ')
                available_balance+=amt
                print(f'${amt} Deposited.')
                print(f'Your new available balance is ${available_balance}')
                if not should_continue():
                    break
            elif response == 3:
                amt = validate_client_amt('How much would like to withdraw?: ')
                if amt > available_balance:
                    print("Insufficient Account Balance, exitting.")
                    break
                available_balance-=amt
                print(f'${amt} Debited\nYour new available balance is ${available_balance}')
                if not should_continue():
                    break
            elif response == 4:
                acct_no = validate_account_number()
                amt = get_floating_input_from_user('Amount to transfer: ')
                if amt > available_balance:
                    print('Insufficient Balance.')
                    continue
                available_balance-=amt
                print('processing...')
                time.sleep(.7)
                print(f'Success.\nAvailable balance: ${available_balance}')
                if not should_continue():
                    break
    

if __name__ == '__main__':
    bank_app()