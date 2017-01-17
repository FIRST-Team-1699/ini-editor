"""
https://stackoverflow.com/questions/36219613/make-tkinter-prompt-inherit-parent-windows-icon
"""
import tkinter as tk
from tkinter import simpledialog


class _QueryConnection(simpledialog._QueryString):

    def __init__(self, *args, **kw):
        simpledialog._QueryString.__init__(self, *args, **kw)

    def buttonbox(self):
        """
        Make a standard button box
        """

        box = tk.Frame(self)

        w = tk.Button(box, text="OK", command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=3, pady=3)
        w.tkraise()
        w = tk.Button(box, text="Cancel", command=self.cancel)
        w.pack(side=tk.LEFT, padx=3, pady=3)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack(side=tk.RIGHT)

    def body(self, master):

        frame = tk.Frame(master)
        label = tk.Label(frame, text=self.prompt)
        label.pack(side=tk.LEFT, padx=3, pady=3)

        self.entry = tk.Entry(frame, width=30)
        self.entry.pack(side=tk.RIGHT, padx=2, pady=2)

        frame.pack()
        self.iconbitmap("data/icon.ico")

        if self.initialvalue is not None:
            self.entry.insert(0, self.initialvalue)
            self.entry.select_range(0, tk.END)

        return self.entry

def ask_connection(title, prompt):
    q = _QueryConnection(title, prompt)
    return q.result

class _QueryLogin(simpledialog._QueryString):

    def __init__(self, *args, **kw):
        simpledialog._QueryString.__init__(self, *args, **kw)

    def buttonbox(self):
        """
        Make a standard button box
        """
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=3, pady=3)
        w.tkraise()
        w = tk.Button(box, text="Cancel", command=self.cancel)
        w.pack(side=tk.LEFT, padx=3, pady=3)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack(side=tk.RIGHT)

    def body(self, master):
        frame = tk.Frame(master)

        login_frame = tk.Frame(frame)
        login_label = tk.Label(login_frame, text="Username: ", width=10)
        login_label.pack(side=tk.LEFT, padx=3, pady=3)

        password_frame = tk.Frame(frame)
        password_label = tk.Label(password_frame, text="Password: ", width=10)
        password_label.pack(side=tk.LEFT, padx=3, pady=3)

        self.login_entry = tk.Entry(login_frame, width=20)
        self.login_entry.pack(side=tk.RIGHT, padx=2, pady=2)

        self.password_entry = tk.Entry(password_frame, width=20, show=u"\u2022")
        self.password_entry.pack(side=tk.RIGHT, padx=2, pady=2)

        login_frame.pack(side=tk.TOP)
        password_frame.pack(side=tk.BOTTOM)

        frame.pack()

        self.iconbitmap("data/icon.ico")

        if self.initialvalue is not None:
            self.login_entry.insert(0, self.initialvalue)
            self.login_entry.select_range(0, tk.END)
            return self.password_entry

        return self.login_entry

    def validate(self):
        self.result = [self.login_entry.get(), self.password_entry.get()]
        return 1

def ask_login(title, username=None):
    q = _QueryLogin(title, "", initialvalue=username)
    return q.result