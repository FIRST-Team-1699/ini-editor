"""
see https://stackoverflow.com/questions/3732605/add-advanced-features-to-a-tkinter-text-widget
"""

import os
import sys
import ftplib
import tkinter as tk
import subprocess
from tkinter import messagebox
from tkinter import filedialog



VERSION = "v0.1a-pre"

class App(tk.Tk):

    file = None
    connection = None

    def __init__(self):
        tk.Tk.__init__(self)

        # Main frame ... hehe get it?
        self.frame = tk.Frame()

        # Menu on the top
        self.toolbar = tk.Menu()

        # File menu
        file = tk.Menu(self.toolbar, tearoff = 0)
        file.add_command(label = "Open", command = self.open_locally)
        file.add_command(label = "Save", command = self.save_locally)
        file.add_command(label = "Save As", command = self.save_as_locally)
        file.add_separator()
        file.add_command(label = "Quit", command = self.quit)

        self.toolbar.add_cascade(label = "File", menu = file)

        # Remote menu
        remote = tk.Menu(self.toolbar, tearoff = 0)
        remote.add_command(label = "Connect", command = self.connect)
        remote.add_command(label = "View Connection", command = self.view_connect)
        remote.add_command(label = "Disconnect", command = self.disconnect)
        remote.add_separator()
        remote.add_command(label="Open", command=self.open_remotely)
        remote.add_command(label="Save", command=self.save_remotely)

        self.toolbar.add_cascade(label = "Remote", menu = remote)

        # Run menu
        run = tk.Menu(self.toolbar, tearoff = 0)
        run.add_command(label = "Run", command = self.simulate)

        self.toolbar.add_cascade(label = "Run", menu = run)

        # About and Version buttons
        self.toolbar.add_command(label = "About", command = self.about)
        self.toolbar.add_command(label = "Version", command = self.version)
        self.config(menu = self.toolbar)

        # Main part of the GUI
        # I'll use a frame to contain the widget and scrollbar; it looks a little nicer that way...
        text_frame = tk.Frame(borderwidth=1, relief="sunken")
        self.text = tk.Text(wrap="none", bg="gray16", fg = "gray78", borderwidth=0, highlightthickness=0, font = ("courier new", "11"))
        self.vsb = tk.Scrollbar(orient="vertical", borderwidth=1, command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(in_=text_frame,side="right", fill="y", expand=False)
        self.text.pack(in_=text_frame, side="left", fill="both", expand=True)
        self.frame.pack(side="top", fill="x")
        text_frame.pack(side="bottom", fill="both", expand=True)

        # Finishing touches
        self.wm_title("ini-editor")

    # Make an About box
    def about(self):
        tk.messagebox.showinfo("ini-editor About",
                               "The ini-editor is designed to assist in creating and editing configuration files."
                               + " See the wiki for help at:\n https://github.com/FIRST-Team-1699/ini-editor/wiki"
                               )
    # Make a Version box
    def version(self):
        tk.messagebox.showinfo("ini-editor Version", "ini-editor: \t\t" + VERSION + "\ntkinter: \t\t" + str(tk.TkVersion)
                               + "\npython: \t\t" + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "."
                               + str(sys.version_info[2]))

    # Open a local file
    def open_locally(self):
        # File selection box
        self.file = filedialog.askopenfilename(filetypes = (("Configuration files", "*.ini;*.cfg"), ("All files", "*.*")))
        # Test to make sure this is a legit file
        if (os.path.isfile(self.file)):
            # read in the file
            opened = open(self.file, "r")
            # remove old text from the textbox
            self.text.delete("1.0", "end") # might want to check if the user saved before doing this
            # write the new contents to the textbox
            self.text.insert("1.0", opened.read())
            # close your resources, or the Oracle of Java will come and crush your soul
            opened.close()
        else:
            # Path is not legit; ask if they want to retry
            m = messagebox.askretrycancel("ini-editor", "Selected path was not a file!")
            if m == True:
                # They want to retry
                self.open_locally()
            else:
                # They do not want to retry
                self.file = None
            pass
        pass

    def save_locally(self):
        if (self.file == None):
            self.save_as_locally()
        else:
            out = open(self.file, "w+")
            out.write(self.text.get("1.0", "end"))
            out.close()

    def save_as_locally(self):
        outfile = filedialog.asksaveasfilename(defaultextension = ".ini",
                                               filetypes = (("Configuration files", "*.ini;*.cfg"), ("All files", "*.*")))
        if (outfile.strip() != ""):
            self.file = outfile
            out = open(outfile, "w+")
            out.write(self.text.get("1.0", "end"))
            out.close()
        else:
            messagebox.showinfo("ini-editor", "Not saved, no file selected")

    def connect(self):
        pass

    def view_connect(self):
        if (self.conenction != None):
            messagebox.showinfo("ini-reader", "")

    def disconnect(self):
        if (self.connection != None):
            self.connection.quit()
            messagebox.showinfo("ini-editor", "Disconnected")
            self.connection = None
        else:
            messagebox.showinfo("ini-editor", "No connection")

    def open_remotely(self):
        pass

    def save_remotely(self):
        pass

    def simulate(self):
        # Check for None filepath
        if (self.file == None):
            # If no filepath, then see if there is anything in the textbox
            if (self.text.get("1.0", "end").strip() == ""):
                # Raise an error that there is no text in the textbox
                messagebox.showerror("ini-editor", "Cannot run simulation, nothing to run!")
            else:
                # Raise an error that the file was not saved
                messagebox.showerror("ini-editor", "Cannot run simulation, file was not saved.")
        else:
            # If there is a filepath, then run a simulation on it
            subprocess.run("java -jar sim/bin/Simulator.jar " + self.file)
        pass

def main():
    # Check for an existing simulator directory
    if (not os.path.exists("sim")):
        # No simulator directory found, raise an error and stop
        # For some reason, Tk starts it's magic before stopping here, so there is a small Tk box that's made.
        messagebox.showerror("ini-editor startup", "No simulation directory found, use start.py instead.")
        sys.exit(1)
    else:
        # If the directory is correct, then start the application
        app = App()
        app.mainloop()
    pass

if __name__ == "__main__":
    main()