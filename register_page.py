from sqlite3.dbapi2 import Time
from db import chatDB
import tkinter as tk
from tkinter.constants import BUTT, NSEW, TOP
from tkinter import Button, Widget, font as tkfont
import time


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.confirm_password = tk.StringVar()
        self.error_message = tk.StringVar()
        self.success_message = tk.StringVar()
        self.grid(padx=20, pady=10, column=0, row=0)
        self.grid_columnconfigure((0, 3), weight=1)
        self.grid_rowconfigure((0, 8), weight=1)
        self.create_frames()
        self.create_widgets()
        self.register_frame_error.grid_remove()
        self.db = chatDB()

    def create_widgets(self):
        self.first_name_label = tk.Label(
            self.register_frame_entries, text="First Name")
        self.first_name_label.grid(column=0, row=0)

        self.first_name_entry = tk.Entry(
            self.register_frame_entries, textvariable=self.first_name)
        self.first_name_entry.grid(
            column=1,  columnspan=2, row=0)

        self.last_name_label = tk.Label(
            self.register_frame_entries, text="Last Name")
        self.last_name_label.grid(column=0, row=1)

        self.last_name_entry = tk.Entry(
            self.register_frame_entries, textvariable=self.last_name)
        self.last_name_entry.grid(column=1, columnspan=2, row=1)

        self.username_label = tk.Label(
            self.register_frame_entries, text="Username")
        self.username_label.grid(column=0, row=2)

        self.username_entry = tk.Entry(
            self.register_frame_entries, textvariable=self.username)
        self.username_entry.grid(column=1, columnspan=2, row=2)

        self.password_label = tk.Label(
            self.register_frame_entries, text="Password")
        self.password_label.grid(column=0, row=3)

        self.password_entry = tk.Entry(
            self.register_frame_entries, textvariable=self.password, show="*")
        self.password_entry.grid(column=1, columnspan=2, row=3)

        self.confirm_password_label = tk.Label(
            self.register_frame_entries, text="Confirm Password")
        self.confirm_password_label.grid(column=0, row=4)

        self.confirm_password_entry = tk.Entry(
            self.register_frame_entries, textvariable=self.confirm_password, show="*")

        self.confirm_password_entry.grid(
            column=1, columnspan=2, row=4)

        self.register_button = tk.Button(
            self.register_frame_buttons, text="Register", command=self.register)
        self.register_button.grid(column=0, row=1)

        self.login_button = tk.Button(
            self.register_frame_buttons, text="Login", command=lambda: self.controller.show_frame('LoginPage'))
        self.login_button.grid(column=0, row=2, pady=10)

        self.error_message_label = tk.Label(
            self.register_frame_error, textvariable=self.error_message, fg='red')
        self.error_message_label.grid(column=9, row=1, sticky='nsew')

        self.success_message_label = tk.Label(
            self.register_frame_error, textvariable=self.success_message, fg='green')
        self.success_message_label.grid(column=9, row=1, sticky='nsew')

    def create_frames(self):
        self.register_frame_entries = tk.Frame(self)
        self.register_frame_entries.grid(
            column=1, row=1, rowspan=5)

        self.register_frame_entries.grid_rowconfigure((0, 4), weight=1)
        self.register_frame_entries.grid_columnconfigure((0, 5), weight=1)

        self.register_frame_buttons = tk.Frame(self)
        self.register_frame_buttons.grid(
            column=1,  row=7, rowspan=4, columnspan=3, pady=10)

        self.register_frame_buttons.grid_rowconfigure((0, 3), weight=1)
        self.register_frame_buttons.grid_columnconfigure((0, 3), weight=1)

        self.register_frame_error = tk.Frame(self)
        self.register_frame_error.grid(
            column=1, columnspan=2, row=11)

    def register(self):
        fName = self.first_name.get()
        lName = self.last_name.get()
        userName = self.username.get()
        password = self.password.get()
        confirmPassword = self.confirm_password.get()
        self.hide_error_message()
        if fName == '' or lName == '' or userName == '' or password == '' or confirmPassword == '':
            self.show_error_message('Fields cannot be empty.')
        elif password != confirmPassword:
            self.show_error_message("Passwords doesn't match")
        elif self.db.user_exists(userName) != None:
            self.show_error_message("Username already taken.")
        else:
            self.db.insert_user_db(fName, lName, userName, password)
            self.show_success_message('User Created!')
            self.after(1000, lambda: self.controller.show_frame('LoginPage'))

    def show_error_message(self, error_message):
        self.register_frame_error.grid()
        self.success_message_label.grid_remove()
        self.error_message_label.grid()
        self.error_message.set(error_message)

    def show_success_message(self, success_message):
        self.register_frame_error.grid()
        self.error_message_label.grid_remove()
        self.success_message_label.grid()
        self.success_message.set(success_message)

    def hide_error_message(self):
        self.register_frame_error.grid_remove()
        self.error_message.set('')
