def student_result_checker():
    name = input('Your Name: ')
    score = get_user_values('Your Score')

    print(f'Hi {name},')
    if (100 >= score >= 70):
        print('Congrationtulations. \nYour grade is \'A\'')
    elif (69 >= score >= 60):
        print('Congrationtulations. \nYour grade is \'B\'')
    elif (59 >= score >= 50):
        print('Weldone. \nYour grade is \'C\'')
    elif (49 >= score >= 45):
        print('Your grade is \'D\', You can do better.')
    elif (44 >= score >= 40):
        print('Your grade is \'E\', You can do better.')
    else:
        print('Your grade is \'F\', Better luck next time.')

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
    student_result_checker()