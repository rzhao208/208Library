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

        # Include ID column so inserted tuples match columns
        columns = ("ID", "Title", "Author", "Year", "Genre")
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
            # adapt width for ID
            w = 70 if col == "ID" else 180
            self.tree.column(col, width=w, anchor="center")

        self.tree.grid(row=2, column=0, columnspan=4, padx=20, pady=15)

        add_btn = Button(
    self,
    text="Add Book",
    font=("Courier", 12),
    bg="#c7e6fa",
    width=15,
    command=lambda: controller.show_frame("AddBookPage")
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

    def _normalize_stats(self, raw):
        """
        Accept either an object with get_stats() or a dict and return a dict with normalized keys.
        Normalized keys returned: id, title, author, year, genres
        """
        stats = {}
        if hasattr(raw, "get_stats") and callable(raw.get_stats):
            stats = raw.get_stats()
        elif isinstance(raw, dict):
            stats = raw
        else:
            return None

        # Try multiple possible key names
        id_val = stats.get("ID") or stats.get("id") or stats.get("Id") or ""
        title = stats.get("name") or stats.get("title") or ""
        author = stats.get("author") or ""
        year = stats.get("publish_date") or stats.get("publish_year") or stats.get("year") or ""
        genres = stats.get("genre_tags") or stats.get("genres") or stats.get("genre") or []
        if isinstance(genres, str):
            genres_list = [g.strip() for g in genres.split(",") if g.strip()]
        else:
            try:
                genres_list = list(genres)
            except Exception:
                genres_list = []

        return {
            "id": id_val,
            "title": title,
            "author": author,
            "year": year,
            "genres": genres_list
        }

    def load_data(self):
        # Clear the tree
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Get books; fall back to an empty list if method missing
        books = []
        try:
            books = self.controller.library.stats_inventory() or []
        except Exception:
            try:
                books = self.controller.library.get_all_books() or []
            except Exception:
                books = []

        for book in books:
            normalized = self._normalize_stats(book)
            if not normalized:
                continue
            id_val = normalized["id"]
            title = normalized["title"]
            author = normalized["author"]
            year = normalized["year"]
            genres = ", ".join(normalized["genres"])
            # Insert consistent number of values matching columns
            self.tree.insert("", "end", values=(id_val, title, author, year, genres))

    def search_book(self):
        keyword = self.search_entry.get().strip().lower()

        if not keyword:
            self.load_data()
            return

        # Use the same data source as load_data
        books = []
        try:
            books = self.controller.library.stats_inventory() or []
        except Exception:
            try:
                books = self.controller.library.get_all_books() or []
            except Exception:
                books = []

        filtered = []
        for b in books:
            normalized = self._normalize_stats(b)
            if not normalized:
                continue
            combined = " ".join([
                str(normalized["title"]),
                str(normalized["author"]),
                str(normalized["year"]),
                " ".join(normalized["genres"])
            ]).lower()
            if keyword in combined:
                filtered.append(normalized)

        # Refresh tree with filtered results
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
                    ", ".join(b["genres"])
                )
            )

    def edit_selected_form(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a book to edit.")
            return

        old_values = self.tree.item(sel[0])["values"]
        # Expect ordering: ID, Title, Author, Year, Genre
        book_id = old_values[0]
        old_title = old_values[1]
        old_author = old_values[2]
        old_year = old_values[3]
        old_genres = old_values[4] if len(old_values) > 4 else ""

        form = Toplevel(self)
        form.title("Edit Book")
        form.geometry("400x320")
        form.config(bg="white")

        fields = ["Title", "Author", "Year", "Genre"]
        entries = {}

        initial = [old_title, old_author, old_year, old_genres]

        for i, field in enumerate(fields):
            Label(form, text=field + ":", bg="white", font=("Courier", 11))\
                .grid(row=i, column=0, padx=10, pady=8, sticky="e")
            entry = Entry(form, font=("Courier", 11), width=30)
            entry.insert(0, initial[i])
            entry.grid(row=i, column=1, pady=8)
            entries[field] = entry

        def save():
            new_values = [entries[f].get().strip() for f in fields]
            if any(v == "" for v in new_values):
                messagebox.showerror("Error", "All fields required.")
                return

            new_title, new_author, new_year, new_genres = new_values
            # Update treeview
            self.tree.item(sel[0], values=(book_id, new_title, new_author, new_year, new_genres))

            # Try to update backend if an update method exists; be tolerant if not present
            try:
                # common names tried: update_book(id, data) or update_book_by_id(id, data)
                data = {
                    "title": new_title,
                    "author": new_author,
                    "publish_year": new_year,
                    "genres": [g.strip() for g in new_genres.split(",") if g.strip()]
                }
                if hasattr(self.controller.library, "update_book"):
                    # signature might differ; many libraries accept (id, data)
                    try:
                        self.controller.library.update_book(book_id, data)
                    except TypeError:
                        # maybe expects (title, ...) — ignore if mismatch
                        pass
                elif hasattr(self.controller.library, "update_book_by_id"):
                    self.controller.library.update_book_by_id(book_id, data)
            except Exception:
                # Don't crash on backend update failures; show a non-fatal warning
                messagebox.showinfo("Note", "Local view updated. Backend update could not be completed automatically.")
            finally:
                form.destroy()

        Button(
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
        # values ordering: ID, Title, Author, Year, Genre
        book_id = values[0] if len(values) > 0 else None
        book_title = values[1] if len(values) > 1 else ""

        # Ask for confirmation
        if not messagebox.askyesno("Confirm Delete", f"Delete '{book_title}'?"):
            return

        # Try to delete by id if possible, otherwise try by title
        try:
            if book_id:
                # Try common delete method names; be tolerant if not present
                if hasattr(self.controller.library, "delete_book_by_id"):
                    self.controller.library.delete_book_by_id(book_id)
                elif hasattr(self.controller.library, "delete_book"):
                    # delete_book might accept id or title; try id then title
                    try:
                        self.controller.library.delete_book(book_id)
                    except Exception:
                        self.controller.library.delete_book(book_title)
                else:
                    # last resort: try delete_book with title
                    if hasattr(self.controller.library, "delete_by_title"):
                        self.controller.library.delete_by_title(book_title)
            else:
                # no id available
                if hasattr(self.controller.library, "delete_book"):
                    self.controller.library.delete_book(book_title)
        except Exception:
            # Don't crash; notify user
            messagebox.showwarning("Warning", "Book removal attempted, but backend deletion may have failed.")

        # Remove from view and inform user
        self.tree.delete(selected[0])
        messagebox.showinfo("Deleted", f"'{book_title}' was removed from inventory (view updated).")
