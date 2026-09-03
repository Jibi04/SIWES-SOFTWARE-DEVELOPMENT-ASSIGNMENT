from helper_functions import get_integer_input_from_user, should_continue
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
        request = get_integer_input_from_user(f'{options}:> ')
        if request == 5:
            break
        elif request == 4:
            print('Student Count: ', len(students))
            if not should_continue():
                break
        elif request == 1:
            student_name = input('Student Name: ').strip()
            students.append(student_name.lower())
            print(f'Student with name {student_name} has been successfully added.')
            if not should_continue():
                break

        elif request == 2:
            student_name = input('Student Name: ').strip().lower()
            if student_name not in students:
                print('Invalid Student Name.')
                break
            else:
                students.remove(student_name)
                print(f'Student with name {student_name} has been successfully removed.')
                if not should_continue():
                    break
        elif request == 3:
            if not students:
                print('There are currently no students enrolled in this system.')
            for i, student in enumerate(students):
                print(f'{i}: {student}')
            if not should_continue():
                break
        else:
            print('Invalid response, (5) to exit')
            continue

if __name__ == '__main__':
    student_management_system()
