from tkinter import *
from tkinter import ttk, messagebox
from tkinter import Frame


class ViewInventoryPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")

        self.controller = controller

 

        title_label = Label(
            self,
            text="Library Inventory",
            font=("Courier", 18, "bold"),
            bg="#c7e6fa",       # light blue
            width=22,
            height=2,
            relief="ridge"
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=15)

   
        Label(self, text="Search:", font=("Courier", 12), bg="white") \
            .grid(row=1, column=0, sticky="e", padx=8)

        self.search_entry = Entry(self, width=45, font=("Courier", 12), bg="black", fg="white")
        self.search_entry.grid(row=1, column=1, padx=5)

       def search_book(self):
        keyword = self.search_entry.get().strip().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for book in self.book_data:
            if (keyword in book[0].lower() or
                keyword in book[1].lower() or
                keyword in book[2].lower() or
                keyword in book[3].lower()):
                self.tree.insert("", "end", values=book)

        clear_btn = Button(
            self,
            text="Clear",
            font=("Courier", 12),
            bg="#c7e6fa",
            command=self.load_data
        )
        clear_btn.grid(row=1, column=3, padx=5)

  
        columns = ("Title", "Author", "Year", "Genre")
        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=15
        )

        style = ttk.Style()
        style.configure("Treeview",
                        background="black",
                        foreground="white",
                        fieldbackground="black",
                        rowheight=28,
                        font=("Courier", 12))
        style.configure("Treeview.Heading",
                        font=("Courier", 12, "bold"),
                        background="black",
                        foreground="white")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor="center")

        self.tree.grid(row=2, column=0, columnspan=4, padx=20, pady=15)

   
        add_btn = Button(
            self,
            text="Add Book",
            font=("Courier", 12),
            bg="#c7e6fa",
            width=15,
            command=lambda: controller.show_frame(AddBookPage)
        )
        add_btn.grid(row=3, column=0, pady=25)

         def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to edit.")
            return

        values = self.tree.item(selected[0], "values")

        edit_win = Toplevel(self)
        edit_win.title("Edit Book")
        edit_win.geometry("400x300")

        Label(edit_win, text="Title").grid(row=0, column=0, padx=10, pady=10)
        title_entry = Entry(edit_win)
        title_entry.grid(row=0, column=1, padx=10)
        title_entry.insert(0, values[0])

        Label(edit_win, text="Author").grid(row=1, column=0, padx=10, pady=10)
        author_entry = Entry(edit_win)
        author_entry.grid(row=1, column=1, padx=10)
        author_entry.insert(0, values[1])

        Label(edit_win, text="Year").grid(row=2, column=0, padx=10, pady=10)
        year_entry = Entry(edit_win)
        year_entry.grid(row=2, column=1, padx=10)
        year_entry.insert(0, values[2])

        Label(edit_win, text="Genres").grid(row=3, column=0, padx=10, pady=10)
        genre_entry = Entry(edit_win)
        genre_entry.grid(row=3, column=1, padx=10)
        genre_entry.insert(0, values[3])

        def save_edits():
            updated = (
                title_entry.get(),
                author_entry.get(),
                year_entry.get(),
                genre_entry.get()
            )
            idx = self.tree.index(selected[0])
            self.book_data[idx] = updated
            self.load_data()
            edit_win.destroy()

        Button(edit_win, text="Save", command=save_edits).grid(row=4, column=1, pady=20)

        delete_btn = Button(
            self,
            text="Delete Selected",
            font=("Courier", 12),
            bg="#c7e6fa",
            width=15,
            command=self.delete_selected
        )
        delete_btn.grid(row=3, column=2, pady=25)

        return_btn = Button(
            self,
            text="Return",
            font=("Courier", 12),
            bg="#c7e6fa",
            width=15,
            command=lambda: controller.show_frame(Dashboard)
        )
        return_btn.grid(row=3, column=3, pady=25)

        # Load backend data
        self.load_data()

     def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        books = self.controller.library.stats_inventory()

        for book in books:
            stats = book.get_stats()
            ID = stats["ID"]
            title = stats["name"]
            author = stats["author"]
            year = stats["publish_date"]
            genres = stats["genre_tags"]

            self.tree.insert("", "end", values=(ID, title, author, year, genres))


    def search_book(self):
        keyword = self.search_entry.get().strip().lower()

        if not keyword:
            self.load_data()
            return

        books = self.controller.library.stats_books()

        filtered = [
            b for b in books
            if keyword in b["title"].lower()
            or keyword in b["author"].lower()
            or keyword in str(b["publish_year"])
            or keyword in " ".join(b["genres"]).lower()
        ]

        for row in self.tree.get_children():
            self.tree.delete(row)

        for b in filtered:
            self.tree.insert(
                "",
                "end",
                values=(
                    b["title"],
                    b["author"],
                    b["publish_year"],
                    ", ".join(b["genres"])
                )
            )

      def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to delete.")
            return

        values = self.tree.item(selected[0], "values")
        book_title = values[0]

        answer = simpledialog.askstring(
            "Delete Book", 
            "Enter the title of the book to confirm deletion:"
        )
        if answer == book_title:
            idx = self.tree.index(selected[0])
            del self.book_data[idx]
            self.load_data()
            messagebox.showinfo("Deleted", f"'{book_title}' was removed from inventory.")
        else:
            messagebox.showerror("Error", "Incorrect title, book not deleted.")

    self.load_data()

