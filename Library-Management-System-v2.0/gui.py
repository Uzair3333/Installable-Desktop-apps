import tkinter as tk
from tkinter import messagebox
from main import Book, Member, Library, User

# Initialize default users
User.create_default_users()

app = tk.Tk()
app.title("📚 Library Management System | v2.0")
app.geometry("600x500")
# app.iconbitmap("assets\icon.ico")

# Global variable to store logged-in user
current_user = None

# Create main canvas with scrollbar for entire app
main_canvas = tk.Canvas(app)
main_scrollbar = tk.Scrollbar(app, orient="vertical", command=main_canvas.yview)
scrollable_main = tk.Frame(main_canvas)

scrollable_main.bind(
    "<Configure>",
    lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
)

main_canvas.create_window((300, 0), window=scrollable_main, anchor="n") 
main_canvas.configure(yscrollcommand=main_scrollbar.set)

main_canvas.pack(side="left", fill="both", expand=True)
main_scrollbar.pack(side="right", fill="y")

# =====================
# Frame Switcher
# =====================
frames = {}

def show(frame):
    for f in frames.values():
        f.pack_forget()
    frames[frame].pack(expand=True)

def go_home():
    """Return to appropriate home screen based on user role"""
    if current_user:
        if current_user['role'] == 'admin':
            show('home_admin')
        elif current_user['role'] == 'librarian':
            show('home_librarian')
        else:
            show('home_member')
    else:
        show('login')

# =====================
# LOGIN SCREEN
# =====================
login_frame = tk.Frame(scrollable_main)
frames['login'] = login_frame

tk.Label(login_frame, text="🔐 Library Management System", font=("Arial", 18, "bold")).pack(pady=30)
tk.Label(login_frame, text="Login", font=("Arial", 14)).pack(pady=10)

tk.Label(login_frame, text="Username").pack()
username_entry = tk.Entry(login_frame, width=30)
username_entry.pack(pady=5)

tk.Label(login_frame, text="Password").pack()
password_entry = tk.Entry(login_frame, show="*", width=30)
password_entry.pack(pady=5)

def login_action():
    global current_user
    username = username_entry.get()
    password = password_entry.get()
    
    if not username or not password:
        messagebox.showerror("Error", "Please enter username and password")
        return
    
    user = User.authenticate(username, password)
    
    if user:
        current_user = user
        messagebox.showinfo("Success", f"Welcome {user['name']}!")
        
        # Clear login fields
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        
        # Show appropriate home screen based on role
        if user['role'] == 'admin':
            show('home_admin')
        elif user['role'] == 'librarian':
            show('home_librarian')
        else:  # member
            show('home_member')
    else:
        messagebox.showerror("Error", "Invalid username or password")

tk.Button(login_frame, text="Login", command=login_action, width=20, bg="#3498db", fg="white").pack(pady=20)


# =====================
# ADMIN HOME
# =====================
home_admin = tk.Frame(scrollable_main)
frames['home_admin'] = home_admin

def create_home_header(parent):
    """Create header showing logged-in user"""
    header = tk.Frame(parent)
    header.pack(pady=10)
    
    user_name = current_user['name'] if current_user else ''
    user_role = current_user['role'].upper() if current_user else ''
    
    tk.Label(header, text=f"Welcome, {user_name}", 
             font=("Arial", 12, "bold")).pack()
    tk.Label(header, text=f"Role: {user_role}", font=("Arial", 10), fg="blue").pack()

# Header for admin
admin_header_frame = tk.Frame(home_admin)
admin_header_frame.pack(pady=10)

tk.Label(home_admin, text="Library Management System", font=("Arial", 18, "bold")).pack(pady=10)
tk.Label(home_admin, text="Full Access Mode", font=("Arial", 10), fg="green").pack()

# Dashboard button
tk.Button(home_admin, text="📊 Dashboard", width=30, command=lambda: show('dashboard'), 
          bg="#3498db", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

# Admin buttons grid
admin_button_frame = tk.Frame(home_admin)
admin_button_frame.pack(pady=10)

# Row 1 - Book Operations
tk.Button(admin_button_frame, text="Add Book", width=20, command=lambda: show('add_book')).grid(row=0, column=0, padx=10, pady=5)
tk.Button(admin_button_frame, text="View All Books", width=20, command=lambda: show('view_books')).grid(row=0, column=1, padx=10, pady=5)
tk.Button(admin_button_frame, text="Search Books", width=20, command=lambda: show('search')).grid(row=0, column=2, padx=10, pady=5)

# Row 2 - Member Operations
tk.Button(admin_button_frame, text="Register Member", width=20, command=lambda: show('add_member')).grid(row=1, column=0, padx=10, pady=5)
tk.Button(admin_button_frame, text="View All Members", width=20, command=lambda: show('view_members')).grid(row=1, column=1, padx=10, pady=5)

# Row 3 - Transactions
tk.Button(admin_button_frame, text="Borrow Book", width=20, command=lambda: show('borrow')).grid(row=2, column=0, padx=10, pady=5)
tk.Button(admin_button_frame, text="Return Book", width=20, command=lambda: show('return')).grid(row=2, column=1, padx=10, pady=5)
tk.Button(admin_button_frame, text="Transactions", width=20, command=lambda: show('logs')).grid(row=2, column=2, padx=10, pady=5)

# Row 4 - Edit/Delete
tk.Button(admin_button_frame, text="Edit/Delete Books", width=20, command=lambda: show('edit_books')).grid(row=3, column=0, padx=10, pady=5)
tk.Button(admin_button_frame, text="Edit/Delete Members", width=20, command=lambda: show('edit_members')).grid(row=3, column=1, padx=10, pady=5)

# Row 5 - Overdue
tk.Button(admin_button_frame, text="⚠️ Overdue Books", width=20, command=lambda: show('overdue'), 
          bg="#e74c3c", fg="white").grid(row=4, column=0, padx=10, pady=5)
tk.Button(admin_button_frame, text="📖 Borrowed Books", width=20, command=lambda: show('borrowed')).grid(row=4, column=1, padx=10, pady=5)

# Logout button
tk.Button(home_admin, text="🚪 Logout", width=20, command=lambda: [globals().update(current_user=None), show('login')], 
          bg="#95a5a6", fg="white").pack(pady=20)

# =====================
# LIBRARIAN HOME
# =====================
home_librarian = tk.Frame(scrollable_main)
frames['home_librarian'] = home_librarian

librarian_header_frame = tk.Frame(home_librarian)
librarian_header_frame.pack(pady=10)

tk.Label(home_librarian, text="Library Management System", font=("Arial", 18, "bold")).pack(pady=10)
tk.Label(home_librarian, text="Librarian Access", font=("Arial", 10), fg="orange").pack()

# Dashboard button
tk.Button(home_librarian, text="📊 Dashboard", width=30, command=lambda: show('dashboard'), 
          bg="#3498db", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

# Librarian buttons grid
lib_button_frame = tk.Frame(home_librarian)
lib_button_frame.pack(pady=10)

# Row 1 - View Operations
tk.Button(lib_button_frame, text="View All Books", width=20, command=lambda: show('view_books')).grid(row=0, column=0, padx=10, pady=5)
tk.Button(lib_button_frame, text="Search Books", width=20, command=lambda: show('search')).grid(row=0, column=1, padx=10, pady=5)
tk.Button(lib_button_frame, text="View All Members", width=20, command=lambda: show('view_members')).grid(row=0, column=2, padx=10, pady=5)

# Row 2 - Transactions
tk.Button(lib_button_frame, text="Borrow Book", width=20, command=lambda: show('borrow')).grid(row=1, column=0, padx=10, pady=5)
tk.Button(lib_button_frame, text="Return Book", width=20, command=lambda: show('return')).grid(row=1, column=1, padx=10, pady=5)
tk.Button(lib_button_frame, text="Transactions", width=20, command=lambda: show('logs')).grid(row=1, column=2, padx=10, pady=5)

# Row 3 - Overdue
tk.Button(lib_button_frame, text="⚠️ Overdue Books", width=20, command=lambda: show('overdue'), 
          bg="#e74c3c", fg="white").grid(row=2, column=0, padx=10, pady=5)
tk.Button(lib_button_frame, text="📖 Borrowed Books", width=20, command=lambda: show('borrowed')).grid(row=2, column=1, padx=10, pady=5)

# Logout button
tk.Button(home_librarian, text="🚪 Logout", width=20, command=lambda: [globals().update(current_user=None), show('login')], 
          bg="#95a5a6", fg="white").pack(pady=20)

# =====================
# MEMBER HOME
# =====================
home_member = tk.Frame(scrollable_main)
frames['home_member'] = home_member

member_header_frame = tk.Frame(home_member)
member_header_frame.pack(pady=10)

tk.Label(home_member, text="Library Management System", font=("Arial", 18, "bold")).pack(pady=10)
tk.Label(home_member, text="Member Portal", font=("Arial", 10), fg="purple").pack()

# Member buttons
mem_button_frame = tk.Frame(home_member)
mem_button_frame.pack(pady=30)

tk.Button(mem_button_frame, text="📚 View Available Books", width=25, command=lambda: show('view_books')).pack(pady=10)
tk.Button(mem_button_frame, text="🔍 Search Books", width=25, command=lambda: show('search')).pack(pady=10)
tk.Button(mem_button_frame, text="📖 My Borrowed Books", width=25, command=lambda: show('my_books')).pack(pady=10)

# Logout button
tk.Button(home_member, text="🚪 Logout", width=20, command=lambda: [globals().update(current_user=None), show('login')], 
          bg="#95a5a6", fg="white").pack(pady=20)

# =====================
# MY BORROWED BOOKS (Member View)
# =====================
my_books_frame = tk.Frame(scrollable_main)
frames['my_books'] = my_books_frame

tk.Label(my_books_frame, text="📖 My Borrowed Books", font=("Arial", 14)).pack(pady=10)

my_books_listbox = tk.Listbox(my_books_frame, width=90, height=15, font=("Courier", 9))
my_books_listbox.pack(pady=10)

def load_my_books():
    my_books_listbox.delete(0, tk.END)
    
    if not current_user:
        my_books_listbox.insert(tk.END, "Please login first")
        return
    
    # Get borrowed books for current member
    borrowed_books = Library.get_all_borrowed_with_due()
    my_borrowed = [b for b in borrowed_books if b['member_id'] == current_user['username']]
    
    if not my_borrowed:
        my_books_listbox.insert(tk.END, "You have no borrowed books")
    else:
        my_books_listbox.insert(tk.END, f"{'BOOK TITLE':<35} | {'ISBN':<15} | {'DUE DATE':<12} | STATUS")
        my_books_listbox.insert(tk.END, "-" * 85)
        
        for item in my_borrowed:
            if item['is_overdue']:
                status = f"⚠️ OVERDUE by {abs(item['days_until_due'])} days"
            elif item['days_until_due'] <= 3:
                status = f"⏰ Due in {item['days_until_due']} days"
            else:
                status = f"✅ Due in {item['days_until_due']} days"
            
            my_books_listbox.insert(tk.END, 
                f"{item['book_title']:<35} | {item['isbn']:<15} | {item['due_date']:<12} | {status}")

tk.Button(my_books_frame, text="🔄 Refresh", command=load_my_books, width=15, bg="#3498db", fg="white").pack(pady=5)
tk.Button(my_books_frame, text="Back", command=go_home).pack()

# =====================
# ADD BOOK
# =====================
add_book = tk.Frame(scrollable_main)
frames['add_book'] = add_book

tk.Label(add_book, text="Add Book", font=("Arial", 14)).pack(pady=10)

tk.Label(add_book, text="Title").pack()
title = tk.Entry(add_book)
title.pack()

tk.Label(add_book, text="Author").pack()
author = tk.Entry(add_book)
author.pack()

tk.Label(add_book, text="ISBN (13 digits)").pack()
isbn = tk.Entry(add_book)
isbn.pack()

def add_book_action():
    try:
        if not title.get() or not author.get() or not isbn.get():
            raise Exception("All fields are required")

        if not isbn.get().isdigit() or len(isbn.get()) != 13:
            raise Exception("ISBN must be 13 digits")

        book = Book(title.get(), author.get(), isbn.get())
        book.append_book()

        messagebox.showinfo("Success", "Book added successfully")

        # CLEAR INPUTS AFTER SUCCESS
        title.delete(0, tk.END)
        author.delete(0, tk.END)
        isbn.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(add_book, text="Save", command=add_book_action).pack(pady=10)
tk.Button(add_book, text="Back", command=go_home).pack()

# =====================
# ADD MEMBER
# =====================
add_member = tk.Frame(scrollable_main)
frames['add_member'] = add_member

tk.Label(add_member, text="Register Member", font=("Arial", 14)).pack(pady=10)

tk.Label(add_member, text="Name").pack()
name = tk.Entry(add_member)
name.pack()

tk.Label(add_member, text="Member ID").pack()
mid = tk.Entry(add_member)
mid.pack()

tk.Label(add_member, text="Email").pack()
email = tk.Entry(add_member)
email.pack()

def add_member_action():
    try:
        if not name.get() or not mid.get() or not email.get():
            raise Exception("All fields are required")

        member = Member(name.get(), mid.get(), email.get())
        member.append_member()

        messagebox.showinfo("Success", "Member registered successfully")

        # CLEAR INPUTS AFTER SUCCESS
        name.delete(0, tk.END)
        mid.delete(0, tk.END)
        email.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(add_member, text="Save", command=add_member_action).pack(pady=10)
tk.Button(add_member, text="Back", command=go_home).pack()

# =====================
# BORROW
# =====================
borrow = tk.Frame(scrollable_main)
frames['borrow'] = borrow

tk.Label(borrow, text="Borrow Book", font=("Arial", 14)).pack(pady=10)

tk.Label(borrow, text="Member ID").pack()
bm = tk.Entry(borrow)
bm.pack()

tk.Label(borrow, text="Book ISBN").pack()
bi = tk.Entry(borrow)
bi.pack()

tk.Label(borrow, text="Due Days (default: 14)").pack()
due_days = tk.Entry(borrow)
due_days.insert(0, "14")
due_days.pack()

def borrow_action():
    try:
        if not bm.get() or not bi.get():
            raise Exception("Member ID and ISBN are required")
        
        days = int(due_days.get()) if due_days.get() else 14
        
        if days <= 0:
            raise Exception("Due days must be positive")
        
        Library.borrow_book(bm.get(), bi.get(), days)
        messagebox.showinfo("Success", f"Book issued successfully. Due in {days} days.")

        # CLEAR INPUTS AFTER SUCCESS
        bm.delete(0, tk.END)
        bi.delete(0, tk.END)
        due_days.delete(0, tk.END)
        due_days.insert(0, "14")

    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(borrow, text="Borrow", command=borrow_action).pack(pady=10)
tk.Button(borrow, text="Back", command=go_home).pack()

# =====================
# RETURN
# =====================
ret = tk.Frame(scrollable_main)
frames['return'] = ret

tk.Label(ret, text="Return Book", font=("Arial", 14)).pack(pady=10)

tk.Label(ret, text="Member ID").pack()
rm = tk.Entry(ret)
rm.pack()

tk.Label(ret, text="Book ISBN").pack()
ri = tk.Entry(ret)
ri.pack()

def return_action():
    try:
        if not rm.get() or not ri.get():
            raise Exception("All fields are required")

        Library.return_book(rm.get(), ri.get())
        messagebox.showinfo("Success", "Book returned successfully")

        # CLEAR INPUTS AFTER SUCCESS
        rm.delete(0, tk.END)
        ri.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(ret, text="Return", command=return_action).pack(pady=10)
tk.Button(ret, text="Back", command=go_home).pack()

# =====================
# TRANSACTIONS
# =====================
logs = tk.Frame(scrollable_main)
frames['logs'] = logs

tk.Label(logs, text="Transaction History", font=("Arial", 14)).pack()

box = tk.Listbox(logs, width=80)
box.pack()

def load_logs():
    box.delete(0, tk.END)
    for t in Library.view_transactions():
        box.insert(tk.END, f"{t['date']} | {t['member_id']} | {t['isbn']} | {t['action']}")

tk.Button(logs, text="Load", command=load_logs).pack(pady=10)
tk.Button(logs, text="Back", command=go_home).pack()

# =====================
# SEARCH BOOKS
# =====================
search_frame = tk.Frame(scrollable_main)
frames['search'] = search_frame

tk.Label(search_frame, text="Search Books", font=("Arial", 14)).pack(pady=10)

# Search input
tk.Label(search_frame, text="Search (Title/Author/ISBN)").pack()
search_query = tk.Entry(search_frame, width=40)
search_query.pack(pady=5)

# Filter dropdown
tk.Label(search_frame, text="Filter by").pack()
filter_var = tk.StringVar(value='all')
filter_menu = tk.OptionMenu(search_frame, filter_var, 'all', 'available', 'borrowed')
filter_menu.pack(pady=5)

# Results listbox
results_box = tk.Listbox(search_frame, width=80, height=15)
results_box.pack(pady=10)

def search_action():
    results_box.delete(0, tk.END)
    query = search_query.get()
    filter_type = filter_var.get()
    
    if not query:
        messagebox.showwarning("Warning", "Please enter a search term")
        return
    
    results = Library.search_books(query, filter_type)
    
    if not results:
        results_box.insert(tk.END, "No books found")
    else:
        for book in results:
            status = "✅ Available" if book['available'] == 'True' else "❌ Borrowed"
            results_box.insert(tk.END, 
                f"{book['title']} | {book['author']} | ISBN: {book['isbn']} | {status}")

tk.Button(search_frame, text="Search", command=search_action, width=15).pack(pady=5)
tk.Button(search_frame, text="Clear", command=lambda: [search_query.delete(0, tk.END), results_box.delete(0, tk.END)], width=15).pack(pady=5)
tk.Button(search_frame, text="Back", command=go_home).pack()

# =====================
# VIEW ALL BOOKS
# =====================
view_books_frame = tk.Frame(scrollable_main)
frames['view_books'] = view_books_frame

tk.Label(view_books_frame, text="All Books", font=("Arial", 14)).pack(pady=10)

books_listbox = tk.Listbox(view_books_frame, width=80, height=15)
books_listbox.pack(pady=10)

def load_all_books():
    books_listbox.delete(0, tk.END)
    books = Library.view_all_books()
    
    if not books:
        books_listbox.insert(tk.END, "No books in library")
    else:
        books_listbox.insert(tk.END, f"{'TITLE':<30} | {'AUTHOR':<20} | {'ISBN':<15} | STATUS")
        books_listbox.insert(tk.END, "-" * 80)
        for book in books:
            status = "✅ Available" if book['available'] == 'True' else "❌ Borrowed"
            books_listbox.insert(tk.END, 
                f"{book['title']:<30} | {book['author']:<20} | {book['isbn']:<15} | {status}")

tk.Button(view_books_frame, text="Refresh", command=load_all_books, width=15).pack(pady=5)
tk.Button(view_books_frame, text="Back", command=go_home).pack()

# Auto-load books when frame is shown
load_all_books()

# =====================
# VIEW ALL MEMBERS
# =====================
view_members_frame = tk.Frame(scrollable_main)
frames['view_members'] = view_members_frame

tk.Label(view_members_frame, text="All Members", font=("Arial", 14)).pack(pady=10)

members_listbox = tk.Listbox(view_members_frame, width=80, height=15)
members_listbox.pack(pady=10)

def load_all_members():
    members_listbox.delete(0, tk.END)
    members = Library.view_all_members()
    
    if not members:
        members_listbox.insert(tk.END, "No members registered")
    else:
        members_listbox.insert(tk.END, f"{'NAME':<25} | {'MEMBER ID':<15} | EMAIL")
        members_listbox.insert(tk.END, "-" * 80)
        for member in members:
            members_listbox.insert(tk.END, 
                f"{member['name']:<25} | {member['member_id']:<15} | {member['email']}")

tk.Button(view_members_frame, text="Refresh", command=load_all_members, width=15).pack(pady=5)
tk.Button(view_members_frame, text="Back", command=go_home).pack()

# Auto-load members when frame is shown
load_all_members()

# =====================
# EDIT/DELETE BOOKS
# =====================
edit_books_frame = tk.Frame(scrollable_main)
frames['edit_books'] = edit_books_frame

tk.Label(edit_books_frame, text="Edit/Delete Books", font=("Arial", 14)).pack(pady=10)

tk.Label(edit_books_frame, text="Enter ISBN").pack()
edit_book_isbn = tk.Entry(edit_books_frame, width=30)
edit_book_isbn.pack(pady=5)

tk.Label(edit_books_frame, text="New Title (leave empty to keep current)").pack()
edit_book_title = tk.Entry(edit_books_frame, width=30)
edit_book_title.pack(pady=5)

tk.Label(edit_books_frame, text="New Author (leave empty to keep current)").pack()
edit_book_author = tk.Entry(edit_books_frame, width=30)
edit_book_author.pack(pady=5)

def edit_book_action():
    try:
        isbn = edit_book_isbn.get()
        if not isbn:
            raise Exception("ISBN is required")
        
        title = edit_book_title.get() if edit_book_title.get() else None
        author = edit_book_author.get() if edit_book_author.get() else None
        
        if not title and not author:
            raise Exception("Please enter at least one field to update")
        
        Library.edit_book(isbn, title, author)
        messagebox.showinfo("Success", "Book updated successfully")
        
        # Clear inputs
        edit_book_isbn.delete(0, tk.END)
        edit_book_title.delete(0, tk.END)
        edit_book_author.delete(0, tk.END)
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_book_action():
    try:
        isbn = edit_book_isbn.get()
        if not isbn:
            raise Exception("ISBN is required")
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?"):
            Library.delete_book(isbn)
            messagebox.showinfo("Success", "Book deleted successfully")
            
            # Clear input
            edit_book_isbn.delete(0, tk.END)
            edit_book_title.delete(0, tk.END)
            edit_book_author.delete(0, tk.END)
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(edit_books_frame, text="Update Book", command=edit_book_action, width=15, bg="#4CAF50", fg="white").pack(pady=5)
tk.Button(edit_books_frame, text="Delete Book", command=delete_book_action, width=15, bg="#f44336", fg="white").pack(pady=5)
tk.Button(edit_books_frame, text="Back", command=go_home).pack(pady=5)

# =====================
# EDIT/DELETE MEMBERS
# =====================
edit_members_frame = tk.Frame(scrollable_main)
frames['edit_members'] = edit_members_frame

tk.Label(edit_members_frame, text="Edit/Delete Members", font=("Arial", 14)).pack(pady=10)

tk.Label(edit_members_frame, text="Enter Member ID").pack()
edit_member_id = tk.Entry(edit_members_frame, width=30)
edit_member_id.pack(pady=5)

tk.Label(edit_members_frame, text="New Name (leave empty to keep current)").pack()
edit_member_name = tk.Entry(edit_members_frame, width=30)
edit_member_name.pack(pady=5)

tk.Label(edit_members_frame, text="New Email (leave empty to keep current)").pack()
edit_member_email = tk.Entry(edit_members_frame, width=30)
edit_member_email.pack(pady=5)

def edit_member_action():
    try:
        member_id = edit_member_id.get()
        if not member_id:
            raise Exception("Member ID is required")
        
        name = edit_member_name.get() if edit_member_name.get() else None
        email = edit_member_email.get() if edit_member_email.get() else None
        
        if not name and not email:
            raise Exception("Please enter at least one field to update")
        
        Library.edit_member(member_id, name, email)
        messagebox.showinfo("Success", "Member updated successfully")
        
        # Clear inputs
        edit_member_id.delete(0, tk.END)
        edit_member_name.delete(0, tk.END)
        edit_member_email.delete(0, tk.END)
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_member_action():
    try:
        member_id = edit_member_id.get()
        if not member_id:
            raise Exception("Member ID is required")
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this member?"):
            Library.delete_member(member_id)
            messagebox.showinfo("Success", "Member deleted successfully")
            
            # Clear input
            edit_member_id.delete(0, tk.END)
            edit_member_name.delete(0, tk.END)
            edit_member_email.delete(0, tk.END)
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(edit_members_frame, text="Update Member", command=edit_member_action, width=15, bg="#4CAF50", fg="white").pack(pady=5)
tk.Button(edit_members_frame, text="Delete Member", command=delete_member_action, width=15, bg="#f44336", fg="white").pack(pady=5)
tk.Button(edit_members_frame, text="Back", command=go_home).pack(pady=5)

# =====================
# DASHBOARD
# =====================
dashboard_frame = tk.Frame(scrollable_main)
frames['dashboard'] = dashboard_frame

tk.Label(dashboard_frame, text="📊 Dashboard", font=("Arial", 18, "bold")).pack(pady=20)

# Create frames for stats cards
stats_container = tk.Frame(dashboard_frame)
stats_container.pack(pady=10)

# Stats display labels (will be updated dynamically)
stats_labels = {}

def create_stat_card(parent, row, col, title, value, color):
    """Create a colored stat card"""
    card = tk.Frame(parent, bg=color, relief="raised", borderwidth=2)
    card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
    
    tk.Label(card, text=title, font=("Arial", 10), bg=color, fg="white").pack(pady=5)
    value_label = tk.Label(card, text=str(value), font=("Arial", 24, "bold"), bg=color, fg="white")
    value_label.pack(pady=10)
    
    # Add some padding
    card.config(width=150, height=100)
    
    return value_label

def load_dashboard():
    """Load and display dashboard stats"""
    stats = Library.get_dashboard_stats()
    
    # Clear existing stats
    for widget in stats_container.winfo_children():
        widget.destroy()
    
    # Row 1 - Books Stats
    create_stat_card(stats_container, 0, 0, "📚 Total Books", stats['total_books'], "#3498db")
    create_stat_card(stats_container, 0, 1, "✅ Available Books", stats['available_books'], "#2ecc71")
    create_stat_card(stats_container, 0, 2, "❌ Borrowed Books", stats['borrowed_books'], "#e74c3c")
    
    # Row 2 - Members & Transactions
    create_stat_card(stats_container, 1, 0, "👥 Total Members", stats['total_members'], "#9b59b6")
    create_stat_card(stats_container, 1, 1, "📝 Total Transactions", stats['total_transactions'], "#f39c12")
    create_stat_card(stats_container, 1, 2, "📖 Currently Borrowed", stats['currently_borrowed'], "#e67e22")

# Summary section
summary_frame = tk.Frame(dashboard_frame)
summary_frame.pack(pady=20)

tk.Label(summary_frame, text="Quick Summary", font=("Arial", 12, "bold")).pack()

summary_text = tk.Text(summary_frame, width=60, height=8, font=("Arial", 10))
summary_text.pack(pady=10)

def update_summary():
    """Update summary text"""
    stats = Library.get_dashboard_stats()
    summary_text.delete(1.0, tk.END)
    
    summary = f"""
    📚 Library Overview:
    • Total Books in Collection: {stats['total_books']}
    • Books Available for Borrowing: {stats['available_books']}
    • Books Currently Out: {stats['borrowed_books']}
    
    👥 Member Statistics:
    • Registered Members: {stats['total_members']}
    • Total Borrow Transactions: {stats['total_borrows']}
    • Total Return Transactions: {stats['total_returns']}
    """
    
    summary_text.insert(1.0, summary)
    summary_text.config(state="disabled")  # Make read-only

# Buttons
button_container = tk.Frame(dashboard_frame)
button_container.pack(pady=10)

tk.Button(button_container, text="🔄 Refresh Dashboard", command=lambda: [load_dashboard(), update_summary()], 
          width=20, bg="#3498db", fg="white").pack(side="left", padx=5)
tk.Button(button_container, text="Back to Home", command=go_home, width=20).pack(side="left", padx=5)

# Load dashboard on frame show
load_dashboard()
update_summary()

# =====================
# OVERDUE BOOKS
# =====================
overdue_frame = tk.Frame(scrollable_main)
frames['overdue'] = overdue_frame

tk.Label(overdue_frame, text="⚠️ Overdue Books", font=("Arial", 14, "bold"), fg="red").pack(pady=10)

overdue_listbox = tk.Listbox(overdue_frame, width=90, height=15, font=("Courier", 9))
overdue_listbox.pack(pady=10)

def load_overdue():
    overdue_listbox.delete(0, tk.END)
    overdue_books = Library.get_overdue_books()
    
    if not overdue_books:
        overdue_listbox.insert(tk.END, "✅ No overdue books!")
    else:
        overdue_listbox.insert(tk.END, f"{'MEMBER ID':<15} | {'BOOK TITLE':<30} | {'ISBN':<15} | {'DUE DATE':<12} | DAYS OVERDUE")
        overdue_listbox.insert(tk.END, "-" * 95)
        
        for item in overdue_books:
            overdue_listbox.insert(tk.END, 
                f"{item['member_id']:<15} | {item['book_title']:<30} | {item['isbn']:<15} | {item['due_date']:<12} | ⚠️ {item['days_overdue']} days")

tk.Button(overdue_frame, text="🔄 Refresh", command=load_overdue, width=15, bg="#e74c3c", fg="white").pack(pady=5)
tk.Button(overdue_frame, text="Back", command=go_home).pack()

load_overdue()

# =====================
# CURRENTLY BORROWED BOOKS
# =====================
borrowed_frame = tk.Frame(scrollable_main)
frames['borrowed'] = borrowed_frame

tk.Label(borrowed_frame, text="📖 Currently Borrowed Books", font=("Arial", 14)).pack(pady=10)

borrowed_listbox = tk.Listbox(borrowed_frame, width=100, height=15, font=("Courier", 9))
borrowed_listbox.pack(pady=10)

def load_borrowed():
    borrowed_listbox.delete(0, tk.END)
    borrowed_books = Library.get_all_borrowed_with_due()
    
    if not borrowed_books:
        borrowed_listbox.insert(tk.END, "No books currently borrowed")
    else:
        borrowed_listbox.insert(tk.END, f"{'MEMBER ID':<15} | {'BOOK TITLE':<30} | {'ISBN':<15} | {'DUE DATE':<12} | STATUS")
        borrowed_listbox.insert(tk.END, "-" * 100)
        
        for item in borrowed_books:
            if item['is_overdue']:
                status = f"⚠️ OVERDUE by {abs(item['days_until_due'])} days"
            elif item['days_until_due'] <= 3:
                status = f"⏰ Due in {item['days_until_due']} days"
            else:
                status = f"✅ Due in {item['days_until_due']} days"
            
            borrowed_listbox.insert(tk.END, 
                f"{item['member_id']:<15} | {item['book_title']:<30} | {item['isbn']:<15} | {item['due_date']:<12} | {status}")

tk.Button(borrowed_frame, text="🔄 Refresh", command=load_borrowed, width=15, bg="#3498db", fg="white").pack(pady=5)
tk.Button(borrowed_frame, text="Back", command=go_home).pack()

load_borrowed()

# =====================
# Start with login screen
show('login')
app.mainloop()