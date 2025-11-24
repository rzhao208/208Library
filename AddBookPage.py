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


    # Clear all fields
    def clear_fields(self):
        self.title_entry.delete(0, END)
        self.author_entry.delete(0, END)
        self.publish_entry.delete(0, END)
        self.cost_entry.delete(0, END)
        self.genre_entry.delete(0, END)

    # Confirm cancel
    def confirm_cancel(self):
        answer = messagebox.askyesno("Confirm Cancel", "Are you sure you want to cancel?")
        if answer:
            self.clear_fields()

    # Confirm return to dashboard
    def confirm_return(self):
        answer = messagebox.askyesno("Confirm Return", "Are you sure you want to return?")
        if answer:
            self.controller.show_frame(Dashboard)

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

        # Clear ONLY fields (not layout)
        self.clear_fields()
