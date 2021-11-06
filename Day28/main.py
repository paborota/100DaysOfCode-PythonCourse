from tkinter import *


# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# ---------------------------- TIMER RESET ------------------------------- # 


def reset_button_clicked():
    global rounds_completed

    # reset everything including the countdown label and remove all checkmarks
    start_button["state"] = "active"
    
    cancel_timer()
    set_countdown_label(0)

    rounds_completed = 0
    set_checkmarks()


# ---------------------------- TIMER MECHANISM ------------------------------- # 


def start_button_clicked():
    start_button["state"] = "disabled"
    work_time()


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 

def popup():
    # forcefully pop the window back into view, even if minimized
    window.deiconify()
    window.focus_force()
    window.attributes("-topmost", 1)
    window.bell()


def set_countdown_label(time):
    mins = time // 60
    secs = time % 60

    if mins < 10:
        mins = f"0{mins}"
    if secs < 10:
        secs = f"0{secs}"
    new_label = f"{mins}:{secs}"
    canvas.itemconfig(canvas_text_index, text=new_label)


def increment_rounds_completed():
    global rounds_completed

    # increment and then update the visual checkmarks
    rounds_completed += 1
    set_checkmarks()


def set_checkmarks():
    global rounds_completed

    # use rounds_completed to insert the correct amount of checkmarks for the label
    new_text = ""
    for _ in range(rounds_completed):
        new_text += "✔"
    rounds_label.config(text=new_text)


def set_timer_label():
    global on_break

    if on_break:
        timer_label.config(text="Break", fg=RED)
    else:
        timer_label.config(text="Timer", fg=GREEN)


def work_time():
    global on_break

    # flip that we're not on break anymore
    # set up the timer for work minutes
    on_break = False
    set_timer(time=WORK_MIN * 60)
    window.bell()


def normal_break():
    global on_break

    # flip that we're on break
    on_break = True
    set_timer_label()

    # set timer for break minutes
    set_timer(time=SHORT_BREAK_MIN * 60)
    popup()


def big_break():
    global on_break
    global rounds_completed

    # flip that we're on break
    on_break = True
    set_timer_label()

    # remove all checkmarks
    rounds_completed = 0
    set_checkmarks()

    # set timer for long break minutes
    set_timer(time=LONG_BREAK_MIN * 60)
    popup()


def set_timer(wait=1000, time=SHORT_BREAK_MIN):
    global timer

    timer = window.after(wait, count_down, time)


def cancel_timer():
    global timer

    window.after_cancel(timer)


def count_down(time):
    global on_break
    global rounds_completed

    set_countdown_label(time)

    if time == 0:
        # Timer has elapsed, check if it was a break timer
        # If was break timer, start work timer.
        # If was work timer, start break timer.
        if not on_break:
            # We've completed a work period
            increment_rounds_completed()
            set_checkmarks()
            if rounds_completed >= 4:
                # We've done 4 work periods, time for a big break
                big_break()
            else:
                # Time for a small break
                normal_break()
        else:
            # Break time is over, time to get back to work
            work_time()
    else:
        # Timer is not finished, keep going
        set_timer(time=time - 1)


timer = 0
on_break = False
rounds_completed = 0


# ---------------------------- UI SETUP ------------------------------- #

# Main Window
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)


# Labels
timer_label = Label(text="Timer")
timer_label.config(font=(FONT_NAME, 50, "bold"), bg=YELLOW, fg=GREEN)
timer_label.grid(column=1, row=0)

rounds_label = Label(text="")
rounds_label.config(font=(FONT_NAME, 12, "bold"), bg=YELLOW, fg=GREEN)
rounds_label.grid(column=1, row=3)


# Canvas
background_image = PhotoImage(file="background_image.png")
background_image_half_width = background_image.width() * 0.5
background_image_half_height = background_image.height() * 0.5

canvas = Canvas(width=background_image.width(), height=background_image.height(), bg=YELLOW, highlightthickness=0)
canvas.create_image(background_image_half_width, background_image_half_height - 1, image=background_image)
canvas_text_index = canvas.create_text(background_image_half_width, background_image_half_height*1.25, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)


# Buttons
start_button = Button(text="Start", highlightthickness=0, command=start_button_clicked)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_button_clicked)
reset_button.grid(column=2, row=2)


window.resizable(False, False)
window.mainloop()
