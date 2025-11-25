from tkinter import messagebox
from tkinter import *
from filetest import Library

from ViewInventory import ViewInventoryPage

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

        # after initializing the library, create the preset books once by calling create_sample()
        # but only run this if the shelve database is currently empty

        if self.library.stats_book_count() == 0:
            self.library.create_sample()


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

            # before, we used the class object like Dashboard, AddBookPage as the key, ex. self.frames[F] = frame
            # but this required importing Dashboard and AddBookPage in ViewInventory.py
            # which created a circular import since we also import ViewInventoryPage in this file
            # so, to avoid the circular import, we use F.__name__ to call the actual instances of the frames, and it stores the class name as a string
            # ex. If F = Dashboard, F.name = "Dashboard"
            # so for the callbacks, we can just refer to the frames using strings, ex. "Dashboard", and require no importing
            self.frames[F.__name__] = frame

            # the children frames use grid so we can stack them and raise them accordingly
            frame.grid(row=0, column=0, sticky="nsew")

        # show the Dashboard page initially
        self.show_frame("Dashboard")

    # this is the function we will call using lambda under each button to switch the frame accordingly
    def show_frame(self, name):
        frame = self.frames[name]
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
        self.button1 = Button(self, text='Add New Book', bg='dark sea green', font=('Courier', 16, "bold"), command= lambda: controller.show_frame("AddBookPage"))
        self.button1.grid(row=5, column=0, sticky='w', padx=10, pady=5)

        # 'view inventory' button
        self.button2 = Button(self, text='View Inventory', bg='dark sea green', font=('Courier', 16, "bold"), relief='raised', command= lambda: controller.show_frame("ViewInventoryPage"))
        self.button2.grid(row=6, column=0, sticky='w', padx=10, pady=10)

        # 'view statistics' button
        self.button2 = Button(self, text='View Statistics', bg='dark sea green', font=('Courier', 16, "bold"),
                              relief='raised', command=lambda: controller.show_frame("ViewStatisticsPage"))
        self.button2.grid(row=7, column=0, sticky='w', padx=10, pady=10)


class AddBookPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f3e8ff")  # light purple

        self.controller = controller

        Label(self, text="Add New Book", font=("Courier", 18, "bold"), bg="#f3e8ff") \
            .grid(row=0, column=0, columnspan=2, pady=10)

        # Book Title
        Label(self, text="Book Title:", bg="#f3e8ff").grid(row=1, column=0, sticky="w")
        self.title_entry = Entry(self, width=40)
        self.title_entry.grid(row=1, column=1)

        # Author
        Label(self, text="Author:", bg="#f3e8ff").grid(row=2, column=0, sticky="w")
        self.author_entry = Entry(self, width=40)
        self.author_entry.grid(row=2, column=1)

        # Publish Year
        Label(self, text="Publish Year:", bg="#f3e8ff").grid(row=3, column=0, sticky="w")
        self.publish_entry = Entry(self, width=40)
        self.publish_entry.grid(row=3, column=1)

        # Cost
        Label(self, text="Cost ($):", bg="#f3e8ff").grid(row=4, column=0, sticky="w")
        self.cost_entry = Entry(self, width=40)
        self.cost_entry.grid(row=4, column=1)

        # Genre
        Label(self, text="Genre:", bg="#f3e8ff").grid(row=5, column=0, sticky="w")
        self.genre_entry = Entry(self, width=40)
        self.genre_entry.grid(row=5, column=1)

        # Save Button
        Button(self, text="Save", bg="lightgreen",
               command=self.save_book).grid(row=6, column=0, pady=20)

        # Cancel button
        Button(self, text="Cancel", bg="red",
               command=self.confirm_cancel).grid(row=6, column=1, pady=20)

        # Return button
        Button(self, text="Return", bg="lightblue",
               command=self.confirm_return).grid(row=7, column=0, columnspan=2, pady=10)

        # create a button to go back to the home screen
        self.button1 = Button(self, text='🏠︎Back to Dashboard', bg="lightblue", fg='black', font=("Courier", 10),
                              borderwidth=2, relief='ridge', command=lambda: controller.show_frame("Dashboard"))
        self.button1.place(relx=1, rely=1, x=-10, y=-10, anchor='se')


    # Clear all fields
    def clear_fields(self):
        self.title_entry.delete(0, END)
        self.author_entry.delete(0, END)
        self.publish_entry.delete(0, END)
        self.cost_entry.delete(0, END)
        self.genre_entry.delete(0, END)

    #     # Asks whether they are sure they want to cancel
    def confirm_cancel(self):
        answer = messagebox.askyesno("Confirm Cancel", "Are you sure you want to cancel?")
        if answer:
            self.clear_fields()

    #     # Asks whether they are sure they want to return
    def confirm_return(self):
        answer = messagebox.askyesno("Confirm Return", "Are you sure you want to return?")
        if answer:
            self.controller.show_frame("Dashboard")

    # Save Book
    def save_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        publish = self.publish_entry.get().strip()
        cost = self.cost_entry.get().strip()
        genre = self.genre_entry.get().strip()

        # Required fields
        if not title or not author:
            messagebox.showerror("Error", "Title and Author are required! Please enter them and try again.")
            return

        genre_list = [genre] if genre else []

        # Save to backend
        self.controller.library.add_book(title, author, publish, cost, genre_list)

        messagebox.showinfo("Success", "Book saved successfully!")

        # Clear fields 
        self.clear_fields()

# class ViewInventoryPage(Frame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#
#         self.controller = controller
#
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_columnconfigure(0, weight=1)
#
#         # create a button to go back to the home screen
#         self.button1 = Button(self, text='🏠︎Back to Dashboard', bg="lightblue", fg='black', font=("Courier", 10),
#                               borderwidth=2, relief='ridge', command=lambda: controller.show_frame(Dashboard))
#         self.button1.grid(row=0, column=0, sticky="se", padx=10, pady=10)

class ViewStatisticsPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create a button to go back to the home screen
        self.button1 = Button(self, text='🏠︎Back to Dashboard', bg="lightblue", fg='black', font=("Courier", 10),
                              borderwidth=2, relief='ridge', command=lambda: controller.show_frame("Dashboard"))
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

        # create a chart for the most popular book genre, which updates based on the data

        # retrieve the genre statistics dict from backend
        genre_stats = controller.library.stats_tags()

        # store keys and values in lists to be accessed by the x and y axes
        genres = list(genre_stats.keys())
        counts = list(genre_stats.values())

        # create the figure
        fig = Figure(figsize=(5,5))
        chart = fig.add_subplot(111)

        # fig.tight_layout() # ensures nothing gets cut out

        # title and labels
        chart.set_title('Book Genres by Popularity')
        chart.bar(genres, counts)
        chart.set_xlabel('Genres')
        chart.set_ylabel('Count')
        chart.tick_params(axis='x', labelsize=5)
        chart.set_xticklabels(genres, rotation=45)

        # embed the chart to tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=3, column=0, sticky='w', pady=10, padx=10)





app = App()
app.mainloop()
