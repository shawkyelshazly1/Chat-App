from sqlite3.dbapi2 import Row
import tkinter as tk
from tkinter.constants import BUTT, E, NSEW, S, TOP, W
from tkinter import font as tkfont
from db import chatDB
import socket
# Login Page Frame

PORT = 5000
SERVER = '127.0.1.1'
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'


class LoginPage(tk.Frame):
    # initializing the controller for parent to move between frames
    # global username, password, error_message text variables
    # configuring columns & rows
    # creating inner frames & widgets attached to them
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.error_message = tk.StringVar()
        self.grid_columnconfigure((0, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.create_frames()
        self.create_widgets()
        self.db = chatDB()

    # creating all needed wigets within the created frames
    def create_widgets(self):
        self.username_label = tk.Label(
            self.login_frame_entries, text='Username')
        self.username_label.grid(column=1, row=0, sticky='ew')

        self.username_entry = tk.Entry(
            self.login_frame_entries, textvariable=self.username)
        self.username_entry.grid(column=2, row=0, sticky='ew')

        self.password_label = tk.Label(
            self.login_frame_entries, text='Password')
        self.password_label.grid(column=1, row=1, sticky='ew')

        self.password_entry = tk.Entry(
            self.login_frame_entries, textvariable=self.password, show='*')
        self.password_entry.grid(column=2, row=1, sticky='ew')

        self.login_btn = tk.Button(
            self.login_frame_buttons, text="Login", command=self.login)
        self.login_btn.grid(pady=10, column=0, columnspan=2, row=2)

        self.register_btn = tk.Button(
            self.login_frame_buttons, text="Register", command=lambda: self.controller.show_frame('RegisterPage'))
        self.register_btn.grid(pady=20, columnspan=2, column=0, row=3)

        self.error_message_label = tk.Label(
            self.login_frame_error, textvariable=self.error_message, fg='red')
        self.error_message_label.grid(column=9, row=0)

    # creating inner frames to hold and organize the widgets

    def create_frames(self):
        self.login_frame_entries = tk.Frame(self)

        self.login_frame_entries.grid(
            column=1, columnspan=2, row=0, rowspan=2, pady=20)

        self.login_frame_entries.grid_columnconfigure((0, 3), weight=1)
        self.login_frame_entries.grid_rowconfigure(0, weight=1)

        self.login_frame_buttons = tk.Frame(self)
        self.login_frame_buttons.grid(
            column=1, columnspan=3, row=2, rowspan=2)

        self.login_frame_error = tk.Frame(self)
        self.login_frame_error.grid(
            column=1, columnspan=2, row=4)

    # login func to validate non empty inputs
    # showing/hiding error messages
    # moving to other frames on successful login
    def login(self):
        self.hide_error_message()
        if len(self.username.get()) == 0 or len(self.password.get()) == 0:
            self.show_error_message("Please Enter Username and Password")

        else:
            user = self.db.retrieve_user_db(
                self.username.get(), self.password.get())
            print(user)
            if user:
                self.controller.username.set(user[3])
                self.controller.show_frame('ChatRoomPage')
                self.client_connection()
                self.controller.frames['ChatRoomPage'].recieving_thread()

            else:
                self.show_error_message(
                    "Can't find user, Register if you don't have account")

    # showing & hiding error message
    def show_error_message(self, message):
        self.error_message.set(message)

    def hide_error_message(self):
        self.error_message.set('')

    def client_connection(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDRESS)
        self.controller.client = self.client
