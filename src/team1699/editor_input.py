"""
https://stackoverflow.com/questions/36219613/make-tkinter-prompt-inherit-parent-windows-icon
"""
import tkinter
from tkinter import simpledialog


class StringDialog(simpledialog.Dialog):

    def __init__(self, title, prompt, parent = None):

        if not parent:
            parent = tkinter._default_root

        print(parent)
        simpledialog.Dialog.__init__(self, parent, title = title)

    def body(self, master):
        return self.buttonbox()

def ask_string(title, prompt):
    d = StringDialog(title, prompt)
    print(d)

ask_string("test", "really?")
