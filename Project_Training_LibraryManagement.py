import tkinter as tk
from tkinter import messagebox
import mysql.connector

class LibraryManagement:
    def __init__(self, master):
        self.master = master
        self.master.title("Library Management System")
        self.master.geometry("400x400")
        self.master.config(bg='#708090')

        self.db_connection = self.connect_to_db()
        self.create_tables()

        # Labels
        self.login_label = tk.Label(self.master, text="Library Management System", font=("Helvetica", 16), bg='#708090', fg='white')
        self.login_label.pack()
        self.username_label = tk.Label(self.master, text="Username", font=("Helvetica", 12), bg='#708090', fg='white')
        self.username_label.pack()
        self.username_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.username_entry.pack()
        self.password_label = tk.Label(self.master, text="Password", font=("Helvetica", 12), bg='#708090', fg='white')
        self.password_label.pack()
        self.password_entry = tk.Entry(self.master, font=("Helvetica", 12), show="*")
        self.password_entry.pack()

        # Login
        self.login_button = tk.Button(self.master, text="Login", command=self.login, font=("Helvetica", 12))
        self.login_button.pack()

        # Register
        self.register_button = tk.Button(self.master, text="Register", command=self.register, font=("Helvetica", 12))
        self.register_button.pack()

        self.username = ""
        self.password = ""

    def connect_to_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="#Rishi1234",
            database="library"
        )

    def create_tables(self):
        cursor = self.db_connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS librarians (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL
        )
        """)
        self.db_connection.commit()
        cursor.close()

    def login(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM librarians WHERE username=%s AND password=%s", (self.username, self.password))
        result = cursor.fetchone()
        cursor.close()
        if result:
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.login_label.destroy()
            self.username_label.destroy()
            self.username_entry.destroy()
            self.password_label.destroy()
            self.password_entry.destroy()
            self.login_button.destroy()
            self.register_button.destroy()
            self.library_management_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO librarians (username, password) VALUES (%s, %s)", (self.username, self.password))
        self.db_connection.commit()
        cursor.close()
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Registered successfully")

    def library_management_screen(self):
        self.add_book_label = tk.Label(self.master, text="Add Book", font=("Helvetica", 16), bg='#708090', fg='white')
        self.add_book_label.pack()
        self.add_book_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.add_book_entry.pack()
        self.add_book_button = tk.Button(self.master, text="Add Book", command=self.add_book, font=("Helvetica", 12))
        self.add_book_button.pack()
        self.remove_book_label = tk.Label(self.master, text="Remove Book", font=("Helvetica", 16), bg='#708090', fg='white')
        self.remove_book_label.pack()
        self.remove_book_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.remove_book_entry.pack()
        self.remove_book_button = tk.Button(self.master, text="Remove Book", command=self.remove_book, font=("Helvetica", 12))
        self.remove_book_button.pack()
        self.issue_book_label = tk.Label(self.master, text="Issue Book", font=("Helvetica", 16), bg='#708090', fg='white')
        self.issue_book_label.pack()
        self.issue_book_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.issue_book_entry.pack()
        self.issue_book_button = tk.Button(self.master, text="Issue Book", command=self.issue_book, font=("Helvetica", 12))
        self.issue_book_button.pack()
        self.view_books_button = tk.Button(self.master, text="View Books", command=self.view_books, font=("Helvetica", 12))
        self.view_books_button.pack()

    def add_book(self):
        book = self.add_book_entry.get()
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO books (title) VALUES (%s)", (book,))
        self.db_connection.commit()
        cursor.close()
        messagebox.showinfo("Success", "Book added successfully")
        self.add_book_entry.delete(0, tk.END)

    def remove_book(self):
        book = self.remove_book_entry.get()
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM books WHERE title=%s", (book,))
        self.db_connection.commit()
        cursor.close()
        messagebox.showinfo("Success", "Book removed successfully")
        self.remove_book_entry.delete(0, tk.END)

    def issue_book(self):
        book = self.issue_book_entry.get()
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM books WHERE title=%s", (book,))
        self.db_connection.commit()
        cursor.close()
        messagebox.showinfo("Success", "Book issued successfully")
        self.issue_book_entry.delete(0, tk.END)

    def view_books(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT title FROM books")
        books = cursor.fetchall()
        cursor.close()
        message = "\n".join(book[0] for book in books)
        messagebox.showinfo("Books", message)

    def __del__(self):
        self.db_connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagement(root)
    root.mainloop()
