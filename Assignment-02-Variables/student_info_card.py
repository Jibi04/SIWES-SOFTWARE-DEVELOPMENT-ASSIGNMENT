from datetime import datetime
def student_information_card(
        fullname: str,
        department: str,
        level: int | str,
        school: str,
        state: str,
        fav_color: str,
        fav_food: str,
        birth_year: int
):
    birth_year = birth_year
    age = datetime.now().year - birth_year
    line = 50 * '*'

    student_profile_card = f"""
Fullname: {fullname}
Age: {age}
Favorite Food: {fav_food}\tFavorite Color: {fav_color}
School: {school}\tState: {state}
Department: {department}\t\tLevel: {level}
{line}
"""
    print(line)
    print("\tSTUDENT INFORMATION CARD\t")
    print(line)
    print(student_profile_card)

if __name__ == '__main__':
    student_information_card(
        fullname='Jibi Barji Philip',
        department='Mathematics',
        level=300,
        school='University Of Jos',
        state='Plateau',
        fav_color='red',
        fav_food='rice',
        birth_year=2004
    )