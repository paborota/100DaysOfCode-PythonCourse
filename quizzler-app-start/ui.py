from tkinter import *
from data import question_data
import html

THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self):
        self.score = 0
        self.question_num = 0
        self.wait_for_next_question = False

        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(bg=THEME_COLOR, padx=20)

        self.score = 0
        self.score_label = Label(self.window, text="Score: 0")
        self.score_label.config(font=("Arial", 10, "bold"), bg=THEME_COLOR, fg="#FFFFFF")
        self.score_label.grid(column=1, row=0, padx=20, pady=20)

        self.canvas = Canvas(self.window, height=250, width=300)
        self.question_text = self.canvas.create_text(150, 125, text="Question goes here.", font=("Arial", 20, "italic"),
                                                     justify=CENTER, width=280)
        self.next_question()
        self.canvas.config(bd=0, highlightthickness=0)
        self.canvas.grid(column=0, row=1, columnspan=2, pady=20)

        true_img = PhotoImage(file="images/true.png")
        self.true_button = Button(image=true_img, command=self.true_button_clicked)
        self.true_button.config(bd=0, highlightthickness=0, bg=THEME_COLOR)
        self.true_button.grid(column=0, row=2, pady=20)

        false_img = PhotoImage(file="images/false.png")
        self.false_button = Button(image=false_img, command=self.false_button_clicked)
        self.false_button.config(bd=0, highlightthickness=0, bg=THEME_COLOR)
        self.false_button.grid(column=1, row=2, pady=20)

        self.window.resizable(False, False)
        self.window.mainloop()

    def get_new_question(self) -> str:
        if self.question_num < len(question_data):
            return html.unescape(question_data[self.question_num]["question"])
        return "Out of questions!"

    def next_question(self):
        self.question_num += 1
        self.canvas.config(bg="#FFFFFF")
        self.canvas.itemconfig(self.question_text, text=self.get_new_question())
        self.wait_for_next_question = False

    def answer_feedback(self, answered_correctly: bool):
        """
        Displays to the user if their answer was wrong by changing the background of the canvas
        to either red or green
        """
        if answered_correctly:
            # Green
            self.canvas.config(bg="#00FF7F")
        else:
            # Red
            self.canvas.config(bg="#FF6347")

    def increment_score(self):
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")

    def questions_left(self) -> bool:
        """
        returns true if there are questions left in the list that have not been asked yet.
        """
        if self.question_num >= len(question_data):
            return False
        return True

    def check_answer(self) -> bool:
        if question_data[self.question_num]["correct_answer"] == "True":
            return True
        return False

    def true_button_clicked(self):
        if not self.questions_left() or self.wait_for_next_question:
            return

        if self.check_answer():
            self.increment_score()
            self.answer_feedback(True)
        else:
            self.answer_feedback(False)

        self.wait_for_next_question = True
        self.window.after(1000, self.next_question)

    def false_button_clicked(self):
        if not self.questions_left() or self.wait_for_next_question:
            return

        if not self.check_answer():
            self.increment_score()
            self.answer_feedback(True)
        else:
            self.answer_feedback(False)

        self.wait_for_next_question = True
        self.window.after(1000, self.next_question)
