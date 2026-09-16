from validators import get_integer_input_from_user
def simple_calculator():
    val1 = get_integer_input_from_user('Enter First Number')
    val2 = get_integer_input_from_user('Enter Second Number')

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
if __name__ == '__main__':
    simple_calculator()