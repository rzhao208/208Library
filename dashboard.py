
from tkinter import *
from filetest import Library

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

# Class to handle frame switching mechanism

# App will be a subclass of Tk because it will behave like a window with all the features,
# but also have the frame-switching functionality
class App(Tk):
    def __init__(self):

        # call the super constructor since we are overriding the init constructor of the Tk window with the frame-switching functionality
        super().__init__()

        # set the title and size of the window
        self.title("Library Inventory Manager")
        self.geometry("640x480")

        # create an instance of the library persistant book database
        # this is how we can attach the backend to the frontend
        self.library = Library("books")


        # this is the main frame 'container' that holds all the frames
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # since the children frames use grid, configure the row and column so that those frames can expand correctly
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # create an empty dict to store all frames
        self.frames = {}

        for F in (Dashboard, AddBookPage, ViewInventoryPage, ViewStatisticsPage):
            frame = F(container, self) # ex. frame = Dashboard(container, self), where container is the parent and self is App
            self.frames[F] = frame

            # the children frames use grid so we can stack them and raise them accordingly
            frame.grid(row=0, column=0, sticky="nsew")

        # show the Dashboard page initially
        self.show_frame(Dashboard)

    # this is the function we will call using lambda under each button to switch the frame accordingly
    def show_frame(self, screen):
        frame = self.frames[screen]
        frame.tkraise()


# Dashboard UI Layout

# Dashboard itself is a frame, so it inherits from the Frame class
class Dashboard(Frame):
    def __init__(self, parent, controller):
        # Since Dashboard overrides init, we need to call Frame's original constructor explicitly so it still runs and creates the frame
        # also set the configuration option for the background within super as it creates the Frame, so it is cleaner than
        # calling self.configure(bg='azure') seperately
        super().__init__(parent, bg='azure')

        # this is a reference to the App, which is the controller class
        self.controller = controller

        # create a label for the dashboard title
        self.label1 = Label(self, text='🏠︎Dashboard', bg="lightblue", fg='black', font=("Courier", 16), width=20, height=2, borderwidth=2, relief='ridge')
        self.label1.grid(row=1, column=0, sticky='w',padx = 10, pady=30)

        # create labels for the welcome text
        self.label2 = Label(self, text="Welcome, Librarian!", bg='azure', font=("Courier", 16, "italic", "bold"))
        self.label2.grid(row=2, column=0, sticky="w", padx=10, pady=1)

        self.label3 = Label(self, text="What would you like to do today?", bg='azure', font=("Courier", 14, "bold"))
        self.label3.grid(row=3, column=0, sticky="w", padx=10, pady=20)

        # create buttons for the various functionalities the librarian can perform
        # the buttons will use callback functions to open the superimposed frames

        # 'add book' button
        self.button1 = Button(self, text='Add New Book', bg='dark sea green', font=('Courier', 16, "bold"), command= lambda: controller.show_frame(AddBookPage))
        self.button1.grid(row=5, column=0, sticky='w', padx=10, pady=5)

        # 'view inventory' button
        self.button2 = Button(self, text='View Inventory', bg='dark sea green', font=('Courier', 16, "bold"), relief='raised', command= lambda: controller.show_frame(ViewInventoryPage))
        self.button2.grid(row=6, column=0, sticky='w', padx=10, pady=10)

        # 'view statistics' button
        self.button2 = Button(self, text='View Statistics', bg='dark sea green', font=('Courier', 16, "bold"),
                              relief='raised', command=lambda: controller.show_frame(ViewStatisticsPage))
        self.button2.grid(row=7, column=0, sticky='w', padx=10, pady=10)


class AddBookPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # to ensure the cell expands and the buttons expand accordingly
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        # create a button to go back to the home screen
        self.button1 = Button(self, text='🏠︎Back to Dashboard', bg="lightblue", fg='black', font=("Courier", 10),borderwidth=2, relief='ridge', command= lambda: controller.show_frame(Dashboard))
        self.button1.grid(row=0, column=0, sticky="se", padx=10, pady=10)

class ViewInventoryPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create a button to go back to the home screen
        self.button1 = Button(self, text='🏠︎Back to Dashboard', bg="lightblue", fg='black', font=("Courier", 10),
                              borderwidth=2, relief='ridge', command=lambda: controller.show_frame(Dashboard))
        self.button1.grid(row=0, column=0, sticky="se", padx=10, pady=10)

class ViewStatisticsPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create a button to go back to the home screen
        self.button1 = Button(self, text='🏠︎Back to Dashboard', bg="lightblue", fg='black', font=("Courier", 10),
                              borderwidth=2, relief='ridge', command=lambda: controller.show_frame(Dashboard))
        self.button1.grid(row=3, column=0, sticky="se", padx=10, pady=10)

        # create a title label for the page
        self.label1 = Label(self, text="Library Inventory Statistics",bg="lightblue", fg='black', font=("Courier", 14), borderwidth=2, relief='ridge')
        self.label1.grid(row=0, column=0, sticky="n", pady=20)

        # create a display of the total book count in the inventory

        # first, retrieve the total book count from the backend, store in a variable
        total_books = self.controller.library.stats_book_count()

        # then, create a label to show the integer of total books
        self.label2 = Label(self, text='Total Inventory:' + str(total_books), font=("Courier", 14), bg="white")
        self.label2.grid(row=1, column=0, sticky="w", padx=20)




app = App()
app.mainloop()
