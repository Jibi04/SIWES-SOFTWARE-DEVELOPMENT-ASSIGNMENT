def student_management_system():
    students = []
    line = 40 * '*'
    options = f"""
    Hi, what would you like to do today?
(1) - Add student
(2) - Remove student
(3) - View Students
(4) - Student count
(5) - exit
"""
    print(line)
    print('\t\tMENU\t\t')
    print(line)

    while True:
        request = get_user_values(f'{options}:> ')
        if request == 5:
            break
        elif request == 4:
            print('Student Count: ', len(students))
            if should_continue():
                continue
            else: break

        elif request == 1:
            student_name = input('Student Name: ').strip()
            students.append(student_name.lower())
            print(f'Student with name {student_name} has been successfully added.')
            if should_continue():
                continue
            else: break

        elif request == 2:
            student_name = input('Student Name: ').strip().lower()
            if student_name not in students:
                print('Invalid Student Name.')
                break
            else:
                students.remove(student_name)
                print(f'Student with name {student_name} has been successfully removed.')
                if should_continue():
                    continue
                else: break
        elif request == 3:
            if len(students) <= 0:
                print('There are currently no students enrolled in this system.')
            for i, student in enumerate(students):
                print(f'{i}: {student}')
            break
        else:
            print('Invalid response, (5) to exit')
            continue

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
    student_management_system()
