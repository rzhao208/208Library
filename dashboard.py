# Dashboard UI Layout

from tkinter import *

class Dashboard:
    def __init__(self, master):
        self.master = master
        master.title("Library Inventory Manager")

        # allow the frame to expand as the window expands
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)

        # create a main frame where all the widgets will lay
        self.main_frame = Frame(master, bg="azure")
        self.main_frame.grid(row=0, column=0, padx = 10, pady= 10, sticky="nsew")

        # create a label for the dashboard title
        self.label1 = Label(self.main_frame, text='🏠︎Dashboard', bg="lightblue", fg='black', font=("Courier", 16), width=20, height=2, borderwidth=2, relief='ridge')
        self.label1.grid(row=1, column=0, sticky='w',padx = 10, pady=10)

        # create labels for the welcome text
        self.label2 = Label(self.main_frame, text="Welcome, Librarian!", bg='azure', font=("Courier", 16, "italic", "bold"))
        self.label2.grid(row=2, column=0, sticky="w", padx=10, pady=1)

        self.label3 = Label(self.main_frame, text="What would you like to do today?", bg='azure', font=("Courier", 14, "bold"))
        self.label3.grid(row=3, column=0, sticky="w", padx=10, pady=10)

        # create buttons for the various functionalities the librarian can perform










root = Tk()
dashboard = Dashboard(root)
root.geometry("640x480")
root.mainloop()