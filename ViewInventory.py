from tkinter import *
from tkinter import ttk, messagebox
from tkinter import Frame

class ViewInventoryPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")

        self.controller = controller

        # Title
        title_label = Label(
            self,
            text="Library Inventory",
            font=("Courier", 18, "bold"),
            bg="#c7e6fa",
            width=22,
            height=2,
            relief="ridge"
        )
        title_label.grid(row=0, column=0, columnspan=5, pady=15)

        # Search
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

        # TABLE COLUMNS (with new COST column)
        columns = ("ID", "Title", "Author", "Year", "Genre", "Cost")

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings"
        )

        # TABLE STYLE (fix header text color)
        style = ttk.Style()
        style.configure("Treeview",
                        background="black",
                        foreground="white",
                        fieldbackground="black",
                        rowheight=28,
                        font=("Courier", 12))

        style.configure("Treeview.Heading",
                        font=("Courier", 12, "bold"),
                        background="#c7e6fa",
                        foreground="black")   # <-- FIXED VISIBILITY

        for col in columns:
            w = 70 if col == "ID" else 150
            if col == "Cost":
                w = 100
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        # Make table resizable
        self.tree.grid(row=2, column=0, columnspan=5, padx=20, pady=15, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Buttons
        add_btn = Button(
            self,
            text="Add Book",
            font=("Courier", 12),
            bg="#c7e6fa",
            width=15,
            command=lambda: (controller.show_frame("AddBookPage"), self.after(300, self.load_data))
        )
        add_btn.grid(row=3, column=0, pady=25)

        edit_btn = Button(
            self,
            text="Edit Selected",
            font=("Courier", 12),
            bg="#c7e6fa",
            width=15,
            command=self.edit_selected_form
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

        self.button1 = Button(
            self,
            text='🏠︎Back to Dashboard',
            bg="lightblue",
            fg='black',
            font=("Courier", 10),
            borderwidth=2,
            relief='ridge',
            command=lambda: controller.show_frame("Dashboard")
        )
        self.button1.place(relx=1, rely=1, x=-10, y=-10, anchor='se')

        self.load_data()

    # Normalizer now includes cost
    def _normalize_stats(self, raw):
        stats = raw if isinstance(raw, dict) else raw.get_stats()

        id_val = stats.get("ID") or stats.get("id") or stats.get("Id")
        title = stats.get("title") or stats.get("name") or ""
        author = stats.get("author") or ""
        year = stats.get("year") or stats.get("publish_year") or ""
        genres = stats.get("genres") or stats.get("genre") or []
        cost = stats.get("cost") or stats.get("price") or ""

        if isinstance(genres, str):
            genres = [g.strip() for g in genres.split(",")]

        if genres is None:
            genres = []

        return {
            "id": id_val,
            "title": title,
            "author": author,
            "year": year,
            "genres": genres,
            "cost": cost
        }

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            books = self.controller.library.stats_inventory()
        except:
            books = {}

        for book_id, book in books.items():
            normalized = self._normalize_stats(book)
            self.tree.insert(
                "",
                "end",
                values=(
                    normalized["id"],
                    normalized["title"],
                    normalized["author"],
                    normalized["year"],
                    ", ".join(normalized["genres"]),
                    normalized["cost"]
                )
            )

    def search_book(self):
        keyword = self.search_entry.get().strip().lower()

        if not keyword:
            self.load_data()
            return

        try:
            books = self.controller.library.stats_inventory()
        except:
            books = {}

        filtered = []

        for book_id, book_obj in books.items():
            n = self._normalize_stats(book_obj)
            combined = f"{n['title']} {n['author']} {n['year']} {' '.join(n['genres'])}".lower()
            if keyword in combined:
                filtered.append(n)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for b in filtered:
            self.tree.insert(
                "",
                "end",
                values=(
                    b["id"],
                    b["title"],
                    b["author"],
                    b["year"],
                    ", ".join(b["genres"]),
                    b["cost"]
                )
            )

    def edit_selected_form(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a book to edit.")
            return

        old = self.tree.item(sel[0])["values"]
        book_id, old_title, old_author, old_year, old_genres, old_cost = old

        form = Toplevel(self)
        form.title("Edit Book")
        form.geometry("400x360")
        form.config(bg="white")

        fields = ["Title", "Author", "Year", "Genre", "Cost"]
        entries = {}
        initial = [old_title, old_author, old_year, old_genres, old_cost]

        for i, f in enumerate(fields):
            Label(form, text=f + ":", bg="white", font=("Courier", 11))\
                .grid(row=i, column=0, padx=10, pady=8, sticky="e")
            e = Entry(form, font=("Courier", 11), width=30)
            e.insert(0, initial[i])
            e.grid(row=i, column=1, pady=8)
            entries[f] = e

        def save():
            vals = [entries[f].get().strip() for f in fields]
            if any(v == "" for v in vals):
                messagebox.showerror("Error", "All fields required.")
                return

            new_title, new_author, new_year, new_genres, new_cost = vals

            self.tree.item(sel[0], values=(
                book_id, new_title, new_author, new_year, new_genres, new_cost
            ))

            try:
                data = {
                    "title": new_title,
                    "author": new_author,
                    "publish_year": new_year,
                    "genres": [g.strip() for g in new_genres.split(",")],
                    "cost": new_cost
                }
                if hasattr(self.controller.library, "update_book"):
                    self.controller.library.update_book(book_id, data)
            except:
                messagebox.showinfo("Note", "Local updated; backend may not have.")

            form.destroy()
            self.load_data()

        Button(
            form, text="Save Changes",
            bg="lightblue", fg="black",
            font=("Courier", 10),
            borderwidth=2, relief='ridge',
            command=save
        ).grid(row=len(fields), column=0, columnspan=2, pady=15)

    def delete_selected(self):
        sel = self.tree.selection()

        if not sel:
            messagebox.showwarning("Warning", "Please select a book to delete.")
            return

        values = self.tree.item(sel[0], "values")
        book_id = values[0]
        book_title = values[1]

        if not messagebox.askyesno("Confirm Delete", f"Delete '{book_title}'?"):
            return

        try:
            if hasattr(self.controller.library, "delete_book_by_id"):
                self.controller.library.delete_book_by_id(book_id)
            else:
                self.controller.library.delete_book(book_title)
        except:
            pass

        self.tree.delete(sel[0])
        messagebox.showinfo("Deleted", f"'{book_title}' removed.")
        self.load_data()
