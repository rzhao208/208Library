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

        search_btn = Button(
            self,
            text="🔍",
            font=("Courier", 12),
            bg="#c7e6fa",
            command=self.search_book
        )
        search_btn.grid(row=1, column=2, padx=5)

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

        edit_btn = Button(
            self,
            text="Edit Selected",
            font=("Courier", 12),
            bg="#c7e6fa",
            width=15
        )
        edit_btn.grid(row=3, column=1, pady=25)

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

    def search_items(self):
        query = self.search_var.get().lower()
        for item in self.tree.get_children():
            values = " ".join(str(v).lower() for v in self.tree.item(item)["values"])
            self.tree.item(item, tags=("match" if query in values else "nomatch"))

        self.tree.tag_configure("match", background="white")
        self.tree.tag_configure("nomatch", background="#E8E8E8")

    def clear_search(self):
        self.search_var.set("")
        for i in self.tree.get_children():
            self.tree.item(i, tags="")
        self.tree.tag_configure("", background="white")

    def edit_selected_form(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a book to edit.")
            return

        old_values = self.tree.item(sel[0])["values"]

        form = tk.Toplevel(self)
        form.title("Edit Book")
        form.geometry("350x300")
        form.config(bg="white")

        fields = ["Title", "Author", "Year", "Genre"]
        entries = {}

        for i, field in enumerate(fields):
            tk.Label(form, text=field + ":", bg="white", font=("Courier", 11))\
                .grid(row=i, column=0, padx=10, pady=8, sticky="e")
            entry = tk.Entry(form, font=("Courier", 11), width=25)
            entry.insert(0, old_values[i])
            entry.grid(row=i, column=1, pady=8)
            entries[field] = entry

        def save():
            new_values = [entries[f].get() for f in fields]
            if any(v == "" for v in new_values):
                messagebox.showerror("Error", "All fields required.")
                return

            self.tree.item(sel[0], values=new_values)
            form.destroy()

        tk.Button(
            form, text="Save Changes",
            bg="lightblue", fg="black",
            font=("Courier", 10),
            borderwidth=2, relief="ridge",
            command=save
        ).grid(row=len(fields), column=0, columnspan=2, pady=15)

    def delete_selected(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Warning", "Please select a book to delete.")
            return

        values = self.tree.item(selected[0], "values")
        book_title = values[0]

        self.controller.library.delete_book(book_title)

        messagebox.showinfo("Deleted", f"'{book_title}' was removed from inventory.")

        self.load_data()


