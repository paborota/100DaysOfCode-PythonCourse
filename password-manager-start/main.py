import json
import random
import pyperclip
from random import choice, randint
import string
from tkinter import *
from tkinter import messagebox


CHARACTER_SET = list(string.ascii_letters)
NUMBER_SET = list(string.digits)
SYMBOL_SET = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '@', '^', '-']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password_button_clicked():
    # print("Generating password..")

    password_letters = [choice(CHARACTER_SET) for _ in range(randint(8, 10))]
    password_symbols = [choice(SYMBOL_SET) for _ in range(randint(2, 4))]
    password_numbers = [choice(NUMBER_SET) for _ in range(randint(2, 4))]

    generated_password_list = password_letters + password_symbols + password_numbers
    random.shuffle(generated_password_list)
    generated_password = ''.join(generated_password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, generated_password)

    # copy to clipboard
    pyperclip.copy(generated_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def clear_inputs():
    website_input.delete(0, END)
    # email_username_entry.delete(0, END) # Maybe keep email since it could be used multiple times?
    password_entry.delete(0, END)


def save():
    website = website_input.get().strip()
    email = email_username_entry.get().strip()
    password = password_entry.get().strip()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    # opening and reading the json data
    try:
        with open("data.json", 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        # the data file was unable to be opened/didn't exist
        data = new_data
    except json.decoder.JSONDecodeError:
        # the data file was empty
        data = new_data
    else:
        data.update(new_data)

    # open or create the file and then write the newly added information
    with open("data.json", 'w') as data_file:
        json.dump(data, data_file, indent=4)

        window.bell()
        clear_inputs()
        print("Entry added!")


def add_entry_button_clicked():
    if '' in [website_input.get(), email_username_entry.get(), password_entry.get()]:
        messagebox.showinfo(title="Uh oh", message="Missing one of more fields!")
        return

    save()


# ---------------------------- ENTRY SEARCH ------------------------------- #


def entry_search():
    try:
        with open("data.json", 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        # the data file was unable to be opened/didn't exist
        messagebox.showerror(title="Oops", message="No entries available.")
    except json.decoder.JSONDecodeError:
        # the data file was empty
        messagebox.showerror(title="Oops", message="No entries available.")
    else:
        if website_input.get() in data:
            # entry found, prompt info
            value = data[website_input.get()]
            message = f"email: {value['email']}\n"\
                      f"password: {value['password']}"
            messagebox.showinfo(title="Match found", message=message)
        else:
            # entry was not found, prompt user
            messagebox.showerror(title="Existential crisis", message="No entry for that website exists.")


def website_lookup_button_clicked():
    entry_search()


def copy_saved_password(text):
    pyperclip.copy(text)


def saved_passwords_menu():
    saved_passwords = Tk()
    saved_passwords.title("Saved Passwords")
    saved_passwords.config(padx=20, pady=15)

    try:
        with open("data.json", 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        no_passwords_found_label = Label(saved_passwords, text="No saved passwords found. :(", width=30)
        no_passwords_found_label.grid(column=0, row=0, columnspan=3)
        pass
    else:
        sp_website_label = Label(saved_passwords, text="Website", width=10)
        sp_website_label.grid(column=0, row=0)

        sp_email_label = Label(saved_passwords, text="Email", width=10)
        sp_email_label.grid(column=1, row=0)

        sp_password_label = Label(saved_passwords, text="Password", width=10)
        sp_password_label.grid(column=2, row=0)

        i = 2
        for entries in data:
            website = entries
            email = data[website]["email"]
            password = data[website]["password"]

            saved_website_label = Label(saved_passwords, text=website, width=15, anchor='w')
            saved_website_label.grid(column=0, row=i)

            saved_email_label = Label(saved_passwords, text=email, width=15, anchor='w')
            saved_email_label.grid(column=1, row=i)

            saved_password_button = Button(saved_passwords, text=password, width=15,
                                           command=lambda: copy_saved_password(password))
            saved_password_button.grid(column=2, row=i)
            i += 1

    # create all instances of the saved passwords inside the saved passwords menu

    saved_passwords.mainloop()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=30, pady=20)

canvas = Canvas(width=200, height=200, highlightthickness=0)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)


# website input
website_label = Label(text="Website:", anchor="e")
website_label.grid(column=0, row=1, sticky="EW")

website_input = Entry(width=33)
website_input.focus()
website_input.grid(column=1, row=1, columnspan=1)

website_lookup_button = Button(text="Search", width=15, command=website_lookup_button_clicked)
website_lookup_button.grid(column=2, row=1)

# Email/Username input
email_username_label = Label(text="Email/Username:", anchor="e")
email_username_label.grid(column=0, row=2)

email_username_entry = Entry()
email_text = "dummy_email@dummy.com"
email_username_entry.insert(0, email_text)
email_username_entry.grid(column=1, row=2, columnspan=2, sticky="EW")


# Password input
password_label = Label(text="Password:", anchor="e")
password_label.grid(column=0, row=3, sticky="EW")

password_entry = Entry()
password_entry.grid(column=1, row=3, sticky="EW")

generate_password_button = Button(text="Generate Password", width=15, command=generate_password_button_clicked)
generate_password_button.grid(column=2, row=3)


# Add entry button
add_entry_button = Button(text="Add", command=add_entry_button_clicked)
add_entry_button.grid(column=1, row=4, columnspan=2, stick="EW")


# Menu Bar
menu_bar = Menu(window)
options = Menu(menu_bar, tearoff=0)

options.add_command(label="Saved Passwords", command=saved_passwords_menu)

options.add_separator()

options.add_command(label="Exit", command=window.destroy)

menu_bar.add_cascade(label="Options", menu=options)
window.config(menu=menu_bar)



window.mainloop()
