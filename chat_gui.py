import socket
import tkinter as tk
from tkinter.constants import BUTT, NSEW, TOP
from tkinter import Button, font as tkfont
from chat_room_page import ChatRoomPage
from Login_page import FORMAT, LoginPage
from register_page import RegisterPage

# Main chat App GUI class


class ChatApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.username = tk.StringVar()
        self.client = None

        # Container for the App which will hold all frames

        container = tk.Frame(self)
        container.grid(column=0, row=0, sticky='nsew')
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # creating dictionary of applicable frames {'page_name':frame object}

        self.frames = {}
        for page in (LoginPage, RegisterPage, ChatRoomPage):
            page_name = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('LoginPage')

    # function to be used across pages to move from page to another by raising frames

    def show_frame(self, page_name):
        for frame in self.frames:
            self.frames[frame].grid_remove()

        self.frames[page_name].grid()

    def on_close(self):
        self.destroy()
        if self.client != None:
            try:
                self.client.send(
                    f'{self.username.get()} has left the chat!'.encode(FORMAT))
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
            except:
                print('error')


if __name__ == "__main__":
    app = ChatApp()
    app.title('Chat App')
    # app.geometry('400x400')
    app.protocol('WM_DELETE_WINDOW', app.on_close)
    app.mainloop()
