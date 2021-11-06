# Hangman challenge
import random


WORD_LIST = ["ardvark", "baboon", "camel"] # CHANGE THIS LIST TO ADD MORE WORDS


def print_board():
    for i in range(len(hangman)):
        print(hangman[i])
    print(" ".join(board))


def ini_game():
    global selected_list
    global board

    for i in range(len(selected_word)):
        selected_list.append(selected_word[i])

    for i in range(len(selected_word)):
        board.append("_")


def print_guesses():
    global guesses
    print("Past guesses: " + ", ".join(guesses))


def get_player_guess():
    return input("Please enter your choice: ").replace(" ", '').lower()[0]


def analyze_guess(guess):
    global guesses
    global selected_list
    global board

    found = False
    if guess not in guesses:
        guesses.add(guess)
        if guess in selected_list:
            found = True
            length = len(selected_list)
            i = 0
            while i < length:
                if selected_list[i] == guess:
                    board[i] = guess
                i += 1
    return found


def subtract_life():
    global hangman
    global lives

    lives -= 1
    if lives == 6:
        hangman[1] += "   |"
    elif lives == 5:
        hangman[2] += "   o"
    elif lives == 4:
        hangman[3] += "  /"
    elif lives == 3:
        hangman[3] += "|"
    elif lives == 2:
        hangman[3] += "\\"
    elif lives == 1:
        hangman[4] += "  /"
    else:
        hangman[4] += " \\"


selected_word = random.choice(WORD_LIST)
selected_list = []
board = []
hangman = ["_____", "|", "|", "|", "|", "|"]
guesses = set()
ini_game()

lives = 7
while True:
    print_board()
    if board == selected_list:
        print("Player wins!")
        break
    if lives <= 0:
        print("Game over!")
        break

    guess = get_player_guess()
    if not analyze_guess(guess):
        subtract_life()

    print("\n" * 100)
    print_guesses()
