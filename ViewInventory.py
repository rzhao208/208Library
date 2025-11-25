from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class LibraryInventory(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="white")
        self.controller = controller

        # =============================== TITLE ===============================
        title_frame = Frame(self, bg="white")
        title_frame.pack(pady=20)

        title_label = Label(
            title_frame,
            text="Library Inventory",
            font=("Courier", 26, "bold"),
            bg="#c7e6fa",
            padx=40,
            pady=8
        )
        title_label.pack()

        # ================= BACK TO DASHBOARD (TOP LEFT) =====================
        back_btn = Button(
            self,
            text="🏠 Back to Dashboard",
            font=("Courier", 12),
            bg="#c7e6fa",
            relief="flat",
            command=lambda: controller.show_frame("Dashboard")
        )
        back_btn.place(x=10, y=10)

        # =============================== SEARCH BAR ===============================
        search_frame = Frame(self, bg="white")
        search_frame.pack(pady=10)

        Label(search_frame, text="Search:", bg="white", font=("Courier", 12)).grid(row=0, column=0)

        self.search_entry = Entry(search_frame, font=("Courier", 12), width=50)
        self.search_entry.grid(row=0, column=1, padx=10)

        search_icon = Image.open("search.png").resize((22, 22))
        self.search_icon = ImageTk.PhotoImage(search_icon)

        search_button = Button(
            search_frame,
            image=self.search_icon,
            bg="#c7e6fa",
            relief="flat",
            command=self.search_book
        )
        search_button.grid(row=0, column=2)

        clear_button = Button(
            search_frame,
            text="Clear",
            width=10,
            bg="#c7e6fa",
            relief="flat",
            command=self.load_inventory
        )
        clear_button.grid(row=0, column=3, padx=10)

        # =============================== TABLE ===============================

        table_frame = Frame(self, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Title", "Author", "Year", "Genre", "Cost")

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        # TREEVIEW STYLE — FIX HEADER TEXT COLOR
        style = ttk.Style()
        style.configure("Treeview",
                        background="black",
                        foreground="white",
                        rowheight=28,
                        font=("Courier", 12),
                        fieldbackground="black")

        style.configure("Treeview.Heading",
                        background="#c7e6fa",
                        foreground="black",
                        font=("Courier", 12, "bold"))

        # Column sizes
        widths = {
            "ID": 60,
            "Title": 250,
            "Author": 180,
            "Year": 120,
            "Genre": 230,
            "Cost": 100
        }

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[col], anchor="center")

        # =============================== BUTTONS ===============================
        btn_frame = Frame(self, bg="white")
        btn_frame.pack(pady=20)

        add_btn = Button(
            btn_frame,
            text="Add Book",
            font=("Courier", 14),
            bg="#c7e6fa",
            relief="flat",
            command=self.add_book
        )
        add_btn.grid(row=0, column=0, padx=20)

        edit_btn = Button(
            btn_frame,
            text="Edit Selected",
            font=("Courier", 14),
            bg="#c7e6fa",
            relief="flat",
            command=self.edit_selected
        )
        edit_btn.grid(row=0, column=1, padx=20)

        delete_btn = Button(
            btn_frame,
            text="Delete Selected",
            font=("Courier", 14),
            bg="#c7e6fa",
            relief="flat",
            command=self.delete_selected
        )
        delete_btn.grid(row=0, column=2, padx=20)

        # Load books at start
        self.load_inventory()

    # ============================= LOAD INVENTORY =============================
    def load_inventory(self):
        self.tree.delete(*self.tree.get_children())
        library = self.controller.library.get_all_books()  # Must return dict

        for book_id, data in library.items():
            self.tree.insert(
                "",
                "end",
                values=(
                    book_id,
                    data.get("Title", ""),
                    data.get("Author", ""),
                    data.get("publish_date", ""),
                    data.get("genre_tags", ""),
                    data.get("Cost", "")
                )
            )

    # ============================= SEARCH BOOK =============================
    def search_book(self):
        query = self.search_entry.get().lower()
        self.tree.delete(*self.tree.get_children())

        library = self.controller.library.get_all_books()

        for book_id, data in library.items():
            if query in str(data).lower():
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        book_id,
                        data.get("Title", ""),
                        data.get("Author", ""),
                        data.get("Year", ""),
                        data.get("Genre", ""),
                        data.get("Cost", "")
                    )
                )

    # ============================= ADD BOOK =============================
    def add_book(self):
        self.controller.show_frame("AddBook")
        self.after(300, self.load_inventory)

    # ============================= DELETE BOOK =============================
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a book to delete.")
            return

        item = self.tree.item(selected[0])
        book_id = int(item["values"][0])

        self.controller.library.delete_book(book_id)
        self.load_inventory()

    # ============================= EDIT BOOK =============================
    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a book to edit.")
            return

        item = self.tree.item(selected[0])
        book_id = int(item["values"][0])

        # Open editor window
        top = Toplevel(self)
        top.title("Edit Book")
        top.geometry("400x400")

        book = self.controller.library.get_book(book_id)

        fields = ["Title", "Author", "Year", "Genre", "Cost"]
        entries = {}

        for i, field in enumerate(fields):
            Label(top, text=field).pack()
            e = Entry(top)
            e.pack()
            e.insert(0, book.get(field, ""))
            entries[field] = e

        def save_changes():
            new_data = {f: entries[f].get() for f in fields}
            self.controller.library.update_book(book_id, new_data)
            self.load_inventory()
            top.destroy()

        Button(top, text="Save Changes", bg="#c7e6fa", command=save_changes).pack(pady=10)
