import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os


class ViewInventoryScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

       
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

 
        self.back_btn = tk.Button(
            self,
            text="🏠︎ Back to Dashboard",
            bg="lightblue", fg="black",
            font=("Courier", 10),
            borderwidth=2, relief="ridge",
            command=self.open_dashboard
        )
        self.back_btn.grid(row=0, column=0, sticky="ne", padx=10, pady=10)

       
        self.title_label = tk.Label(
            self,
            text="Library Inventory",
            font=("Courier", 14, "bold"),
            bg="lightblue", fg="black",
            borderwidth=2, relief="ridge",
            padx=10, pady=5
        )
        self.title_label.grid(row=1, column=0, sticky="n", pady=10)

       
        search_frame = tk.Frame(self, bg="white")
        search_frame.grid(row=2, column=0, sticky="n", pady=5)

        tk.Label(
            search_frame, text="Search:", bg="white", fg="black",
            font=("Courier", 12)
        ).grid(row=0, column=0, padx=5)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame, textvariable=self.search_var,
            width=40, font=("Courier", 11)
        )
        self.search_entry.grid(row=0, column=1, padx=5)

        tk.Button(
            search_frame, text="🔍",
            bg="lightblue", fg="black",
            font=("Courier", 10),
            borderwidth=2, relief="ridge",
            command=self.search_items
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            search_frame, text="Clear",
            bg="lightblue", fg="black",
            font=("Courier", 10),
            borderwidth=2, relief="ridge",
            command=self.clear_search
        ).grid(row=0, column=3, padx=5)

    
        tree_frame = tk.Frame(self, bg="white")
        tree_frame.grid(row=3, column=0, sticky="n", pady=10)

        columns = ("Title", "Author", "Year", "Genre")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky="ns")

    
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.grid(row=4, column=0, pady=20)

        button_style = dict(
            bg="lightblue",
            fg="black",
            font=("Courier", 10),
            borderwidth=0,
            relief="flat",
            width=15
        )

        tk.Button(btn_frame, text="Add Book", command=self.add_book_form, **button_style)\
            .grid(row=0, column=0, padx=10)

        tk.Button(btn_frame, text="Edit Selected", command=self.edit_selected_form, **button_style)\
            .grid(row=0, column=1, padx=10)

        tk.Button(btn_frame, text="Delete Selected", command=self.delete_selected, **button_style)\
            .grid(row=0, column=2, padx=10)

        tk.Button(btn_frame, text="Return", command=self.open_dashboard, **button_style)\
            .grid(row=0, column=3, padx=10)

        # Load sample data
        self.load_data()

  
    def open_dashboard(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dashboard_path = os.path.join(current_dir, "dashboard.py")

        subprocess.Popen([sys.executable, dashboard_path])
        self.master.destroy()

    def load_data(self):
        sample = [
            ("Harry Potter", "J.K. Rowling", "1997", "Fantasy"),
            ("The Hobbit", "J.R.R. Tolkien", "1937", "Fantasy"),
            ("Atomic Habits", "James Clear", "2018", "Self-help")
        ]
        for row in sample:
            self.tree.insert("", "end", values=row)

  
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

 
    def add_book_form(self):
        form = tk.Toplevel(self)
        form.title("Add Book")
        form.geometry("350x300")
        form.config(bg="white")

        fields = ["Title", "Author", "Year", "Genre"]
        entries = {}

        for i, field in enumerate(fields):
            tk.Label(form, text=field + ":", bg="white", font=("Courier", 11))\
                .grid(row=i, column=0, padx=10, pady=8, sticky="e")
            entry = tk.Entry(form, font=("Courier", 11), width=25)
            entry.grid(row=i, column=1, pady=8)
            entries[field] = entry

        def save():
            values = [entries[f].get() for f in fields]
            if any(v == "" for v in values):
                messagebox.showerror("Error", "All fields required.")
                return

            self.tree.insert("", "end", values=values)
            form.destroy()

        tk.Button(
            form, text="Save",
            bg="lightblue", fg="black",
            font=("Courier", 10),
            borderwidth=2, relief="ridge",
            command=save
        ).grid(row=len(fields), column=0, columnspan=2, pady=15)


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
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("None selected", "Select a book to delete.")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?"):
            self.tree.delete(sel[0])

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Inventory Test Window")
    root.geometry("800x600")

    app = ViewInventoryScreen(root)
    app.pack(fill="both", expand=True)

    root.mainloop()
