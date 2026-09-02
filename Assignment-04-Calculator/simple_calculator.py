def simple_calculator():
    val1 = get_user_values('Enter First Number')
    val2 = get_user_values('Enter Second Number')

    addition = val1 + val2
    subtration = val1 - val2
    multiplication = val1 * val2
    division = val1 / val2
    modulus = val1 % val2
    power = val1**val2

    results = f"""
addition = {addition}
subtraction = {subtration}
multiplication = {multiplication}
divsion = {division}
modulus = {modulus}
power = {power}
"""
    print(results)


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
    simple_calculator()