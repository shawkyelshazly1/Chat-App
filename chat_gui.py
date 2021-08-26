import tkinter as tk
from tkinter.constants import BUTT, NSEW, TOP
from tkinter import Button, font as tkfont
from chat_room_page import ChatRoomPage
from Login_page import LoginPage
from register_page import RegisterPage


class ChatApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.grid(column=0, row=0, sticky=NSEW)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.frames = {}
        for page in (LoginPage, RegisterPage, ChatRoomPage):
            page_name = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky=NSEW)

        self.show_frame('LoginPage')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = ChatApp()
    app.geometry('400x400')
    app.mainloop()
