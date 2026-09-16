from validators import validate_client_amt
from helper_functions import should_continue
def atm_machine():
    available_balance = 100000.00
    user = input('accout name: ')
    print(f"Welcome, {user.capitalize()}")

    while True:
        response = input('What would you like to do? (1 - check balance, 2 - Deposit, 3 - withdraw, q - Quit): ')
        if response.lower() == 'q':
            break

        if not response.isdigit():
            print("Invalid Input value, (q - to Quit): ")
            continue

        response = int(response)
        if response not in (1, 2, 3):
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

    print(f'Thank you for banking with us.')
if __name__ == '__main__':
    atm_machine()