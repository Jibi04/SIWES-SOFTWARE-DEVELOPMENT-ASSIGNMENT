from helper_functions import get_integer_input_from_user
def student_result_checker():
    name = input('Your Name: ')
    print(f'Hi {name},')
    while True:
        score = get_integer_input_from_user('Your Score: ')
        if score > 100:
            print('Score cannot be greated than 100')
            continue
        elif score < 0:
            print('Score cannot be less zero (0)')
            continue
        else:
            break
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

if __name__ == '__main__':
    student_result_checker()