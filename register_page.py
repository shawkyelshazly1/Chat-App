import tkinter as tk
from tkinter.constants import BUTT, NSEW, TOP
from tkinter import Button, font as tkfont


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        welcomeLabel = tk.Label(self, text='Register Page')
        welcomeLabel.pack(side='top', fill='x', pady=10)

        logout_btn = tk.Button(
            self, text="Register", command=lambda: self.controller.show_frame("LoginPage"))
        logout_btn.pack()
