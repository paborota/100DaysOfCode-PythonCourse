from tkinter import *
import pandas
from random import choice
from os.path import exists

# ------------------------ CONSTANTS ------------------------#

BACKGROUND_COLOR = "#B1DDC6"
TIME_UNTIL_FLIP = 3


# ------------------------ GLOBALS ------------------------ #

def setup_word_dict():
    if exists("data/words_to_learn.csv"):
        try:
            return pandas.read_csv("data/words_to_learn.csv").to_dict()
        except pandas.errors.EmptyDataError:
            return pandas.read_csv
    else:
        return pandas.read_csv("data/french_words.csv").to_dict()



WORD_DICT = setup_word_dict()
# DICT_KEYS_REMAINING = list(WORD_DICT["French"].keys())

flip_timer = ''
word_index = 0
flipped = False


# ------------------------ SAVE UNKNOWN WORDS ------------------------ #

def on_close():
    print("User closed window")
    pandas.DataFrame(WORD_DICT).to_csv("data/words_to_learn.csv", index=False)
    window.destroy()


# ------------------------ BUTTON FUNCTIONALITY ------------------------#

def change_card_config(image, title, word):
    flash_card_canvas.itemconfig(flash_card_image, image=image)
    flash_card_canvas.itemconfig(flash_card_title, text=title)
    flash_card_canvas.itemconfig(flash_card_word, text=word)


def flip_card():
    global flip_timer
    global word_index
    global flipped

    flipped = True
    window.after_cancel(flip_timer)

    english_word = WORD_DICT["English"][word_index]

    change_card_config(flash_card_back_image, "English", english_word)


def generate_new_card():
    global flip_timer
    global word_index
    global flipped

    if not check_for_words_left():
        change_card_config(flash_card_front_image, "", "Completed!")
        return

    flipped = False

    word_index = choice(list(WORD_DICT["French"].keys()))
    new_word = WORD_DICT["French"][word_index]
    print(WORD_DICT)

    change_card_config(flash_card_front_image, "French", new_word)

    flip_timer = window.after(TIME_UNTIL_FLIP * 1000, func=flip_card)


def cancel_flip():
    window.after_cancel(flip_timer)


def check_for_words_left():
    if len(WORD_DICT["French"].keys()) > 0:
        return True

    return False


def pre_check(correct_button_pressed):
    # check to see if there are words before moving onto the button logic
    if not check_for_words_left():
        return

    if correct_button_pressed:
        correct_button_clicked()
    else:
        wrong_button_clicked()


def correct_button_clicked():
    global word_index
    cancel_flip()

    del WORD_DICT["French"][word_index]
    del WORD_DICT["English"][word_index]

    generate_new_card()


def wrong_button_clicked():
    cancel_flip()

    generate_new_card()


def card_clicked(event):
    global flipped

    if not flipped:
        flip_card()


# ------------------------ UI CONFIGURATION ------------------------#

if __name__ == "__main__":

    window = Tk()
    window.title("Flashly")
    window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

    flash_card_canvas = Canvas(window, width=800, height=525, bg=BACKGROUND_COLOR, highlightthickness=0, bd=0)
    flash_card_front_image = PhotoImage(file="images/card_front.png")
    flash_card_back_image = PhotoImage(file="images/card_back.png")
    flash_card_image = flash_card_canvas.create_image(400, 262.5, image=flash_card_front_image)
    flash_card_title = flash_card_canvas.create_text(400, 150, text="Title", fill="black", font=("Ariel", 40, "italic"))
    flash_card_word = flash_card_canvas.create_text(400, 263, text="word", fill="black", font=("Ariel", 60, "bold"))
    generate_new_card()
    flash_card_canvas.bind("<Button-1>", card_clicked)
    flash_card_canvas.grid(column=0, row=0, columnspan=2)


    unknown_button_image = PhotoImage(file="images/wrong.png")
    unknown_button = Button(image=unknown_button_image, highlightthickness=0, bd=0, command=lambda: pre_check(False))
    unknown_button.grid(column=0, row=1)

    correct_button_image = PhotoImage(file="images/right.png")
    correct_button = Button(image=correct_button_image, highlightthickness=0, bd=0, command=lambda: pre_check(True))
    correct_button.grid(column=1, row=1)



    window.protocol("WM_DELETE_WINDOW", on_close)
    window.mainloop()
