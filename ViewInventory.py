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

        # TREEVIEW STYLING — BLACK HEADER TEXT
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
            "Author": 200,
            "Year": 120,
            "Genre": 250,
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

        # Initial load
        self.load_inventory()

    # ============================= LOAD INVENTORY =============================
    def load_inventory(self):
        self.tree.delete(*self.tree.get_children())
        inventory = self.controller.library.stats_inventory()

        for book_id, book in inventory.items():
            stats = book.get_stats()
            self.tree.insert(
                "",
                "end",
                values=(
                    stats["ID"],
                    stats["name"],
                    stats["author"],
                    stats["publish_date"],
                    ", ".join(stats["genre_tags"]),
                    stats["cost"]
                )
            )

    # ============================= SEARCH BOOK =============================
    def search_book(self):
        query = self.search_entry.get().lower()
        self.tree.delete(*self.tree.get_children())

        inventory = self.controller.library.stats_inventory()

        for _, book in inventory.items():
            stats = book.get_stats()
            text = json.dumps(stats).lower()

            if query in text:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        stats["ID"],
                        stats["name"],
                        stats["author"],
                        stats["publish_date"],
                        ", ".join(stats["genre_tags"]),
                        stats["cost"]
                    )
                )

    # ============================= ADD BOOK =============================
    def add_book(self):
        self.controller.show_frame("AddBook")
        self.after(250, self.load_inventory)

    # ============================= DELETE BOOK =============================
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a book to delete.")
            return

        item = self.tree.item(selected[0])
        book_id = item["values"][0]

        self.controller.library.delete_book(book_id)
        self.load_inventory()

    # ============================= EDIT BOOK =============================
    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a book to edit.")
            return

        item = self.tree.item(selected[0])
        book_id = item["values"][0]

        book = self.controller.library.inventory[str(book_id)]
        stats = book.get_stats()

        top = Toplevel(self)
        top.title(f"Edit Book (ID {book_id})")
        top.geometry("400x500")

        # Form fields
        fields = ["name", "author", "publish_date", "cost", "genre_tags"]
        entries = {}

        for f in fields:
            Label(top, text=f).pack()
            e = Entry(top)
            e.pack()

            if f == "genre_tags":
                e.insert(0, ", ".join(stats[f]))
            else:
                e.insert(0, stats[f])

            entries[f] = e

        def save_changes():
            new_name = entries["name"].get()
            new_author = entries["author"].get()
            new_year = entries["publish_date"].get()
            new_cost = entries["cost"].get()
            new_genre = [g.strip() for g in entries["genre_tags"].get().split(",") if g.strip()]

            self.controller.library.edit_book(
                book_id,
                name=new_name,
                author=new_author,
                publish_date=new_year,
                cost=new_cost,
                genre=new_genre
            )

            self.load_inventory()
            top.destroy()

        Button(top, text="Save Changes", bg="#c7e6fa", command=save_changes).pack(pady=15)
