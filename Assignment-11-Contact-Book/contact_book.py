from validators import get_contact_info, get_integer_input_from_user
from helper_functions import should_continue, get_contact_card
from typing import Tuple, Dict, Any

CONTACT_DATABASE = {}
def contact_book():
    line = 40 * '*'
    options = f"""
    Hi, what would you like to do today?
(1) - New Contact
(2) - Search Contacts
(3) - Delete Contact
(4) - View Contact
(5) - exit
"""
    print(line)
    print('\t\tMENU\t\t')
    print(line)

    # Decided to take a dictionary mapping approach because if-else conditionals became too much.
    while True:
        res = get_integer_input_from_user(msg=f'{options}:> ')
        if res not in RESPONSE_MAP:
            print('Please select a valid option, (5 - quit)')
            continue
        if res == 5:
            break
        else:
            function_to_call = RESPONSE_MAP[res]
            function_to_call()
            if not should_continue():
                break

def search_contact_database(key: str = '') -> None | Tuple[str, Dict[str, Any]]:
    match: str | None = None
    for name in CONTACT_DATABASE.keys():
        if key in name.split('-'):
            match = name
            break
    if match is None:
        return None
    else:
        return match, CONTACT_DATABASE.get(match, {})

def new_contact() -> None:
    data = get_contact_info()
    fullname = data.get('firstname', '').lower() + '-' + data.get('lastname', '').lower()
    CONTACT_DATABASE[fullname] = data
    print(fullname.replace('-', ' '), ' contact created.')

def get_contact_data() -> None:
    key = input('Name: ')
    result = search_contact_database(key)
    if result is None:
        print(f'No match found for \'{key}\'')
        return

    _, data = result
    print(get_contact_card(data))

def delete_contact() -> None:
    key = input('Name: ')
    entry = search_contact_database(key=key)

    if entry is None:
        print(f'No match found for \'{key}\'')
        return
    
    CONTACT_DATABASE.pop(entry[0])
    print(f'{key} deleted.')

def view_all_contacts() -> None:
    if not CONTACT_DATABASE:
        print('There are no contacts saved yet.')
        return
    for data in CONTACT_DATABASE.values():
        print(get_contact_card(data))

RESPONSE_MAP = {
    1: new_contact,
    2: get_contact_data,
    3: delete_contact,
    4: view_all_contacts,
    5: ''
}

if __name__ == '__main__':
    contact_book()