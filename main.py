from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
import pyperclip
import json

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

# ---------------------------- Constants ------------------------------- #
FONT = ('arial', 12, 'bold')
GRAY = "#D9D9D9"
WHITE = "#FEFBF6"
RED = "#62374E"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_generator():
    password_entry.delete(0, END)
    letters_list = [choice(letters) for _ in range(randint(8, 10))]
    symbols_list = [choice(symbols) for _ in range(randint(2, 4))]
    numbers_list = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = letters_list + symbols_list + numbers_list
    shuffle(password_list)
    created_password = "".join(password_list)
    password_entry.insert(0, created_password)
    pyperclip.copy(created_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_button():
    website = website_entry.get()
    username = email_entry.get()
    password = password_entry.get()

    new_data = {
        website:
            {
                "Email": username,
                "Password": password
            }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="OOPS", message="Don't leave any of the fields empty.")

    else:
        try:
            with open("Passwords.json", "r") as password_file:
                data = json.load(password_file)

        except FileNotFoundError:
            with open("Passwords.json", "w") as password_file:
                json.dump(new_data, password_file, indent=4)
        else:
            data.update(new_data)

            with open("Passwords.json", "w") as password_file:
                json.dump(data, password_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- SEARCH ------------------------------- #


def search():
    req_website = (website_entry.get()).title()

    if len(req_website) == 0:
        messagebox.showerror(title="Oops!", message="Don't leave any of the fields empty.")

    else:
        try:
            with open("Passwords.json", "r") as passwords_list:
                data = json.load(passwords_list)
        except FileNotFoundError:
            messagebox.showerror(title="Oops!", message="No Data File Found. ")

        else:
            if req_website in data:
                email = data[req_website]['Email']
                password = data[req_website]['Password']
                messagebox.showinfo(title=req_website, message=f"Email: {email}\nPassword: {password}\n"
                                                               "Note: Password is copied to clipboard")
                pyperclip.copy(password)

            else:
                messagebox.showerror(title="Oops!", message=f"Details for {req_website} not found.")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50, bg=GRAY)
canvas = Canvas(width=200, height=200)
image_lock = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image_lock)
canvas.config(bg=GRAY, highlightthickness=0)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:", font=FONT, bg=GRAY, fg=RED)
website_label.grid(column=0, row=1)

username_label = Label(text="Email/Username:", font=FONT, bg=GRAY, fg=RED)
username_label.grid(column=0, row=2)

password_label = Label(text="Password:", font=FONT, bg=GRAY, fg=RED)
password_label.grid(column=0, row=3, padx=15)

# Entries
website_entry = Entry(width=25)
website_entry.focus()
website_entry.grid(column=1, row=1, pady=3)

email_entry = Entry(width=39)

email_entry.grid(column=1, row=2, columnspan=2, pady=3)

password_entry = Entry(width=25)
password_entry.grid(column=1, row=3, pady=3)

# Buttons
search_button = Button(text="Search", width=11, font=('arial', 9, 'bold'), fg=RED, bg=WHITE, command=search)
search_button.grid(column=2, row=1)

generate_button = Button(text="Generate Password", width=34, font=('arial', 9, 'bold'), fg=RED, bg=WHITE,
                         command=password_generator)
generate_button.grid(column=1, row=4, columnspan=2, pady=5)


add_button = Button(text="Add", width=11, font=('arial', 9, 'bold'), fg=RED, bg=WHITE, command=add_button)
add_button.grid(column=2, row=3)

window.mainloop()
