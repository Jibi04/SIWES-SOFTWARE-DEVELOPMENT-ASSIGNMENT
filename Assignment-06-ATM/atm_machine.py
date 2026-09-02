def atm_machine():
    available_balance = 100000.00
    user = input('accout name: ')
    print(f"Welcome, {user}")
    while True:
        response = input('What would you like to do today? (1 - check balance, 2 - Deposit, 3 - withdraw, q - Quit): ')
        if response.lower() == 'q':
            break

        try:
            response = int(response)
        except ValueError:
            print("Invalid Input value or (q) to exit")
            continue

        if response not in (1, 2, 3):
            print('Invalid response, q) to exit')
            continue
        else:
            if response == 1:
                print(f'Your available balance: {float(available_balance)}')
                if should_continue():
                    continue
                else: break
            elif response == 2:
                amt = get_user_values('Amount to Deposit')
                available_balance+=amt
                print(f'{amt} Deposited.')
                print(f'Your new available balance is {available_balance}')
                if should_continue():
                    continue
                else: break

            elif response == 3:
                amt = get_user_values('How much would like to withdraw today?')
                if amt > available_balance:
                    print("Insufficient Account Balance, exitting.")
                    break
                available_balance-=amt
                print(f'{amt} Debited\nYour new available balance is {available_balance}')
                if should_continue():
                    continue
                else: break

    print(f'Thank you for banking with us.')

def should_continue():
    response = int(input('Would you like to do anything else? (1 - YES, 0 - NO): '))
    return bool(response)


def get_user_values(msg: str):
    while True:
        try:
            res = input(f'{msg}: ')
            val = float(res)
            return val
        except ValueError:
            print(f'Invalid Value expected an Integer/Decimal but got \'{type(res).__name__}\'')
            continue
 
if __name__ == '__main__':
    atm_machine()