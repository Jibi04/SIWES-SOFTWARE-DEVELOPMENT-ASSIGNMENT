import random

def guess_the_number():
    number = random.randint(0, 1000)
    attempts = 0
    allowable_attempts = 5
    while True:
        if attempts == 5:
            print('Sorry, You are only allowed 5 attempts')
            print(f'Value: {number}')
            break
        player_guess = input("Guess the Number (q - quit): ")
        if player_guess.lower() =='q':
            print('Quitting...')
            break 
        try:
            player_guess = int(player_guess)
        except ValueError:
            print("Expected Integer but got 'str'.")
            continue
        if player_guess > number:
            print("Too High")
        elif player_guess < number:
            print("Too Low")
        else:
            print("Correct!")
        attempts += 1
        print(f'{attempts}/{allowable_attempts} attempts.')

if __name__ == '__main__':
    guess_the_number()