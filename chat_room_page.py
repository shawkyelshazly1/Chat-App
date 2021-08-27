import tkinter as tk
from tkinter.constants import BUTT, NSEW, TOP
from tkinter import Button, font as tkfont

# chat room frame


class ChatRoomPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=600, height=500)
        self.controller = controller
        self.create_frames()
        self.create_widgets()
        self.populate()

    # creating widgets that would be part of the chat room frame

    def create_widgets(self):

        self.message_entry = tk.Text(
            self.message_box_frame, width=61)
        self.message_entry.pack(side='left')

        self.send_button = tk.Button(
            self.message_box_frame, text="Send")
        self.send_button.pack(side='right', ipadx=30, ipady=30)

    def create_frames(self):
        self.messages_frame = tk.Frame(
            self, width=600, height=420, bg='red')
        self.messages_frame.pack(side='top')

        self.canvas = tk.Canvas(
            self.messages_frame, width=600, height=420, bg='#d8e2dc')

        self.content_frame = tk.Frame(self.canvas, bg='#d8e2dc')

        self.canvas.create_window(
            (0, 0), window=self.content_frame, anchor='nw')
        self.canvas.pack(side='left', anchor='center', fill='both')

        self.vsb = tk.Scrollbar(self.messages_frame, orient='vertical')
        self.vsb.pack(side='right', fill='y')
        self.vsb.config(command=self.canvas.yview)

        self.canvas.config(yscrollcommand=self.vsb.set)

        self.content_frame.bind("<Configure>", self.onFrameConfigure)

        self.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.canvas.bind('<Leave>', self._unbound_to_mousewheel)

        self.message_box_frame = tk.Frame(
            self, width=600, height=80, bg='black')
        self.message_box_frame.pack(side='bottom')
        self.message_box_frame.pack_propagate(0)

    

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event, scroll_direction):

        self.canvas.yview_scroll(int(scroll_direction), "units")

    def _bound_to_mousewheel(self, event):

        self.canvas.bind_all(
            "<Button-5>", lambda event: self._on_mousewheel(event, 1))
        self.canvas.bind_all(
            "<Button-4>", lambda event: self._on_mousewheel(event, -1))

    def _unbound_to_mousewheel(self, event):

        self.canvas.unbind_all("<Button-5>")
        self.canvas.unbind_all("<Button-4>")
