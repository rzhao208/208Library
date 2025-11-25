from tkinter import *
from tkinter import ttk, messagebox, Frame, Toplevel


class ViewInventoryPage(Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")

        self.controller = controller

        # Make frame resizable
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title_label = Label(
            self,
            text="Library Inventory",
            font=("Courier", 18, "bold"),
            bg="#c7e6fa",
            width=22,
            height=2,
            relief="ridge"
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=15)

        Label(self, text="Search:", font=("Courier", 12), bg="white") \
            .grid(row=1, column=0, sticky="e", padx=8)

        self.search_entry = Entry(self, width=45, font=("Courier", 12), bg="black", fg="white")
        self.search_entry.grid(row=1, column=1, padx=5, sticky="we")

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

        # -----------------------------------------------------
        #  TABLE WITH AUTO RESIZE + COST COLUMN
        # -----------------------------------------------------
        columns = ("ID", "Title", "Author", "Year", "Genre", "Cost")

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings"
        )

        # SCROLLBARS
        vsb = Scrollbar(self, orient="vertical", command=self.tree.yview)
        hsb = Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=20, pady=(10, 0))
        vsb.grid(row=2, column=4, sticky="ns")
        hsb.grid(row=3, column=0, columnspan=4, sticky="ew")

        # STYLE FIX → readable headings
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
                        foreground="black")

        # COLUMN DEFINITIONS (wider for readability)
        self.tree.column("ID", width=70, anchor="center")
        self.tree.column("Title", width=250, anchor="center")
        self.tree.column("Author", width=200, anchor="center")
        self.tree.column("Year", width=100, anchor="center")
        self.tree.column("Genre", width=300, anchor="center")
        self.tree.column("Cost", width=120, anchor="center")

        for col in columns:
            self.tree.heading(col, text=col)

        # -----------------------------------------------------
        # BUTTONS
        # -----------------------------------------------------
        add_btn = Button(
            self,
            text="Add Book",
            font=("Courier", 12),
            bg="#c7e6fa",
            width=15,
            command=self.refresh_after_add
        )
        add_btn.grid(row=4, column=0, pady=25)

        edit_btn = Button(
            self,
            text="Edit Selected",
            font=("Courier", 12),
            bg="#c7e6fa",
            width=15,
            command=self.edit_selected_form
        )
        edit_btn.grid(row=4, column=1, pady=25)

        delete_btn = Button(
            self,
            text="Delete Selected",
            font=("Courier", 12),
            bg="#c7e6fa",
            width=15,
            command=self.delete_selected
        )
        delete_btn.grid(row=4, column=2, pady=25)

        self.button1 = Button(
            self,
            text='🏠︎ Back to Dashboard',
            bg="lightblue",
            fg='black',
            font=("Courier", 10),
            borderwidth=2,
            relief='ridge',
            command=lambda: controller.show_frame("Dashboard")
        )
        self.button1.place(relx=1, rely=1, x=-10, y=-10, anchor='se')

        # Initial load
        self.load_data()

    # ---------------------------------------------------------
    # NORMALIZE BACKEND DATA
    # ---------------------------------------------------------
    def _normalize_stats(self, raw):
        if hasattr(raw, "get_stats"):
            stats = raw.get_stats()
        else:
            stats = raw

        return {
            "id": stats.get("id") or stats.get("ID") or 0,
            "title": stats.get("title") or stats.get("name") or "",
            "author": stats.get("author", ""),
            "year": stats.get("year") or stats.get("publish_year") or "",
            "genres": stats.get("genre") or stats.get("genres") or "",
            "cost": stats.get("cost") or stats.get("price") or ""
        }

    # ---------------------------------------------------------
    # LOAD TABLE CONTENT
    # ---------------------------------------------------------
    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            books = self.controller.library.stats_inventory()
        except:
            books = {}

        for book_id, book in books.items():
            b = self._normalize_stats(book)

            # b["id"] may be 0 — DON'T FILTER IT OUT
            self.tree.insert(
                "",
                "end",
                values=(
                    b["id"],
                    b["title"],
                    b["author"],
                    b["year"],
                    b["genres"],
                    b["cost"]
                )
            )

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------
    def search_book(self):
        keyword = self.search_entry.get().strip().lower()

        if not keyword:
            self.load_data()
            return

        try:
            books = self.controller.library.stats_inventory()
        except:
            books = {}

        for row in self.tree.get_children():
            self.tree.delete(row)

        for book_id, book in books.items():
            b = self._normalize_stats(book)

            combo = f"{b['title']} {b['author']} {b['year']} {b['genres']} {b['cost']}".lower()

            if keyword in combo:
                self.tree.insert("", "end", values=(
                    b["id"],
                    b["title"],
                    b["author"],
                    b["year"],
                    b["genres"],
                    b["cost"]
                ))

    # ---------------------------------------------------------
    # EDIT SELECTED
    # ---------------------------------------------------------
    def edit_selected_form(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a book to edit.")
            return

        values = self.tree.item(sel[0])["values"]
        book_id, old_title, old_author, old_year, old_genres, old_cost = values

        form = Toplevel(self)
        form.title("Edit Book")
        form.geometry("430x350")
        form.config(bg="white")

        fields = ["Title", "Author", "Year", "Genre", "Cost"]
        initial = [old_title, old_author, old_year, old_genres, old_cost]
        entries = {}

        for i, field in enumerate(fields):
            Label(form, text=field + ":", bg="white", font=("Courier", 11)) \
                .grid(row=i, column=0, padx=10, pady=8, sticky="e")

            entry = Entry(form, font=("Courier", 11), width=30)
            entry.insert(0, initial[i])
            entry.grid(row=i, column=1, pady=8)
            entries[field] = entry

        def save():
            new_vals = [entries[f].get().strip() for f in fields]

            if any(v == "" for v in new_vals):
                messagebox.showerror("Error", "All fields required.")
                return

            new_title, new_author, new_year, new_genres, new_cost = new_vals

            # Update TreeView
            self.tree.item(sel[0], values=(
                book_id, new_title, new_author, new_year, new_genres, new_cost
            ))

            # Update backend
            try:
                data = {
                    "title": new_title,
                    "author": new_author,
                    "publish_year": new_year,
                    "genres": new_genres,
                    "cost": new_cost
                }
                if hasattr(self.controller.library, "update_book"):
                    self.controller.library.update_book(book_id, data)

            except Exception:
                messagebox.showwarning("Warning", "Backend update may have failed.")

            form.destroy()
            self.load_data()

        Button(
            form, text="Save Changes",
            bg="lightblue", fg="black",
            font=("Courier", 10),
            borderwidth=2, relief="ridge",
            command=save
        ).grid(row=len(fields), column=0, columnspan=2, pady=15)

    # ---------------------------------------------------------
    # DELETE SELECTED
    # ---------------------------------------------------------
    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a book to delete.")
            return

        values = self.tree.item(sel[0], "values")
        book_id = values[0]
        title = values[1]

        if not messagebox.askyesno("Confirm", f"Delete '{title}'?"):
            return

        try:
            if hasattr(self.controller.library, "delete_book_by_id"):
                self.controller.library.delete_book_by_id(book_id)
        except:
            messagebox.showwarning("Warning", "Backend delete failed.")

        self.load_data()

    # ---------------------------------------------------------
    # AUTO-REFRESH AFTER ADD BOOK
    # ---------------------------------------------------------
    def refresh_after_add(self):
        # open add book page normally
        self.controller.show_frame("AddBookPage")

        # refresh when page returns
        self.after(300, self.load_data)
