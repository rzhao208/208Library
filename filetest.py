import shelve
import pickle
import json
import dbm


class Book:
    """
    A book object that holds info similar to a book irl
    """
    def __init__(self, name, author, publish_date, cost, ID, genre_tags=()):
        """
        name: name of the book
        author: author of the book
        publish_date: publish date of the book
        cost: a generic cost value, I don't know what we will do with it
        genre_tags: tags that can be searched through, default of (), pass through iterables
        """
        self.name = name
        self.author = author
        self.publish_date = publish_date
        self.cost = cost
        self.ID = ID
        self.genre_tags = []
        if genre_tags:
            for i in genre_tags:
                self.genre_tags.append(i)

    def __str__(self):
        """
        when using print() on a book object, it will return the following:
        """
        return (f"ID: {self.ID}, {self.name} by {self.author}. Published in {self.publish_date} and costs {self.cost}."
                f"It is in the {self.genre_tags} genre(s)")


class Library:
    def __init__(self, file_name):
        """
        shelve_file: a direct link to the shelf file on the computer (which by default is in the same folder as the program)
        inventory: a dictionary that stores the same files as the shelf. It's basically a cache where changes are made before
                the shelf gets updated in a single batch
        filtered_inventory: a dictionary that stores a subset of the main inventory after applying search filters. Updated
                after each time the apply_filter() function is called
        current_ID: an internal counter for managing the IDs of books
        """
        self.shelve_file = shelve.open(file_name)
        self.inventory = dict(self.shelve_file)
        self.filtered_inventory = {}
        self.current_ID = 0

    def add_book(self, name, author, publish, cost, genre_tags=()):
        # finds next free ID
        if str(self.current_ID) in self.shelve_file:
            while str(self.current_ID) in self.shelve_file:
                self.current_ID += 1
        new_book = Book(name, author, publish, cost, self.current_ID, genre_tags)
        self.inventory[str(self.current_ID)] = new_book
        self.shelve_file.update(self.inventory)
        print(f"{new_book}. has been added to library")

    def delete_book(self, book_id):
        try:
            del self.shelve_file[str(book_id)]
            del self.inventory[str(book_id)]
            print(f"deleted book {book_id}")
            return True
        except:
            print("delete attempt failed")
            return False

    def print_books(self):
        # prints all books out, use for debugging
        for i in dict(self.shelve_file):
            print(f'{dict(self.shelve_file)[i]}')

    def print_filtered_books(self):
        for i in self.filtered_inventory:
            print(f'{dict(self.shelve_file)[i]}')

    def edit_book(self, book_id, name=False, author=False, publish_date=False, cost=False, genre=False):
        # edits a book
        if str(book_id) not in dict(self.shelve_file):
            print("edit attempt failed, book not found in library")
            return False
        if name:
            self.inventory[str(book_id)].name = name
        if author:
            self.inventory[str(book_id)].author = author
        if publish_date:
            self.inventory[str(book_id)].publish_date = publish_date
        if cost:
            self.inventory[str(book_id)].cost = cost
        if genre:
            self.inventory[str(book_id)].genre_tags = genre
        self.shelve_file.update(self.inventory)

    def apply_filter(self, name=False, author=False, publish=False, cost=False, genre_tags=False):
        """
        filters are used for searching
        name filter: finds all books that include a certain substring
        author filter: same as name filter but applies to authors
        publish: finds books with matching publish dates
        cost: finds books with matching costs
        genre_tags: finds books with at least 1 matching genre tags

        a book must pass all 6 filters to be eligible, although certain filters can be left
        """
        self.inventory = dict(self.shelve_file)
        self.filtered_inventory = {}
        for i in self.inventory:
            valid = True
            if name and not (name.lower() in self.inventory[i].name.lower()):
                valid = False
            if author and not (author.lower() in self.inventory[i].author.lower()):
                valid = False
            if publish and not (publish == self.inventory[i].publish_date):
                valid = False
            if cost and not (cost == self.inventory[i].cost):
                valid = False
            if genre_tags and not (len(list(set(genre_tags + self.inventory[i].genre_tags))) < len(genre_tags) + len(self.inventory[i].genre_tags)):
                valid = False
            if valid:
                self.filtered_inventory[i] = self.inventory[i]

    def stats_tags(self, use_filter=False):
        """
        returns a dictionary with the keys being genre tags and the contents being an int indicating how many times that
        genre tag appears

        by default, this searches through inventory (every book kept in this library), setting use_filter to True makes
        it search through the filtered inventory instead
        """
        tags = {}
        if use_filter:
            pool = self.filtered_inventory
        else:
            pool = self.inventory

        for i in pool:
            for j in pool[i].genre_tags:
                if j not in tags:
                    tags[j] = 1
                else:
                    tags[j] += 1
        return tags

    def stats_books(self, use_filter=False):
        """
        returns a dictionary with the keys being book titles and the contents being an int indicating how many times
        that book appears

        by default, this searches through inventory (every book kept in this library), setting use_filter to True makes
        it search through the filtered inventory instead
        """
        books = {}
        if use_filter:
            pool = self.filtered_inventory
        else:
            pool = self.inventory

        for i in pool:
            if pool[i].name not in books:
                books[pool[i].name] = 1
            else:
                books[pool[i].name] += 1
        return books

    def stats_inventory(self, use_filter=False):
        """
        returns the inventory

        by default, this returns inventory (every book kept in this library), setting use_filter to True makes
        it return the filtered inventory instead
        """
        if use_filter:
            return self.filtered_inventory
        return self.inventory

    def stats_book_count(self, use_filter=False):
        """
        returns total number of books

        by default, this searches through inventory (every book kept in this library), setting use_filter to True makes
        it search through the filtered inventory instead
        """
        if use_filter:
            return len(self.filtered_inventory)
        else:
            return len(self.inventory)

    def create_sample(self):
        """
        creates a small sample of books based on wikipedia's all-time best-selling books section
        """
        self.add_book("A Tale of Two Cities", "Charles Dickens", 1859, 200, ["historical fiction"])
        self.add_book("The Little Prince", "Antoine de Saint-Exupery", 1943, 200, ["fantasy"])
        self.add_book("The Alchemist", "Paulo Coelho", 1988, 150, ["fantasy"])
        self.add_book("Harry Potter and the Philosopher's Stone", "J. K. Rowling", 1997, 120, ["fantasy"])
        self.add_book("And Then There Were None", "Agatha Christie", 1939, 100, ["mystery"])
        self.add_book("Dream of the Red Chamber", "Cao Xueqin", 1791, 100, ["family saga"])
        self.add_book("The Hobbit", "J. R. R. Tolkien", 1937, 100, ["fantasy", "children's fiction"])
        self.add_book("Alice's Adventures in Wonderland", "Lewis Carroll", 1865, 100, ["fantasy", "absurdist fiction"])

    def delete_all_books(self):
        """
        deletes all books
        """
        temp = dict(self.inventory)
        for i in temp:
            self.delete_book(i)


l = Library("books")
l.print_books()


