import tkinter as tk
from tkinter import ttk

class ViewInventory(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ---------- Title ----------
        title_label = tk.Label(self, text="View Inventory", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # ---------- Table Frame ----------
        table_frame = tk.Frame(self)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Treeview (inventory table)
        columns = ("Title", "Author", "Publish Date", "Genre")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        self.tree.pack(fill="both", expand=True)

        # ---------- Refresh Button ----------
        refresh_button = tk.Button(self, text="Refresh Inventory", command=self.load_data)
        refresh_button.pack(pady=10)


    def load_data(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Ensure controller + library exist
        if not hasattr(self.controller, "library"):
            print("Library not found in controller")
            return

        library = self.controller.library

        # Reload shelve file to get latest data
        library.inventory = dict(library.shelve_file)

        # Insert each book into the table
        for book_id, book in library.inventory.items():
            title = book.name
            author = book.author
            publish = book.publish_date
            genre = ", ".join(book.genre_tags) if book.genre_tags else ""

            self.tree.insert("", "end", values=(title, author, publish, genre))


    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.load_data()   # auto-refresh when switching to this page
