import csv
import os
from datetime import datetime

# ==========================
# Paths & folders
# ==========================
DATA_DIR = "data"
BOOKS_FILE = os.path.join(DATA_DIR, "books.csv")
MEMBERS_FILE = os.path.join(DATA_DIR, "members.csv")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# ==========================
# 📚 Book Class
# ==========================
class Book:
    fieldnames = ['title', 'author', 'isbn', 'available']

    def __init__(self, title, author, isbn, available=True):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available

    def append_book(self):
        books = Book.load_books()

        for b in books:
            if b['isbn'] == self.isbn:
                raise Exception("Book with this ISBN already exists")

        with open(BOOKS_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=Book.fieldnames)
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow({
                'title': self.title,
                'author': self.author,
                'isbn': self.isbn,
                'available': str(self.available)
            })

    @staticmethod
    def load_books():
        if not os.path.exists(BOOKS_FILE):
            return []
        with open(BOOKS_FILE, 'r', newline='') as f:
            return list(csv.DictReader(f))

    @staticmethod
    def is_valid_isbn(isbn):
        return isbn.isdigit() and len(isbn) == 13


# ==========================
# 👤 Member Class
# ==========================
class Member:
    fieldnames = ['name', 'member_id', 'email']

    def __init__(self, name, member_id, email):
        self.name = name
        self.member_id = member_id
        self.email = email

    def append_member(self):
        members = Member.load_members()

        for m in members:
            if m['member_id'] == self.member_id:
                raise Exception("Member already exists")

        with open(MEMBERS_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=Member.fieldnames)
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(vars(self))

    @staticmethod
    def load_members():
        if not os.path.exists(MEMBERS_FILE):
            return []
        with open(MEMBERS_FILE, 'r', newline='') as f:
            return list(csv.DictReader(f))

# ==========================
# 🔐 User Class (for login)
# ==========================
class User:
    fieldnames = ['username', 'password', 'role', 'name']
    USERS_FILE = os.path.join(DATA_DIR, "users.csv")

    def __init__(self, username, password, role, name):
        self.username = username
        self.password = password
        self.role = role  # 'admin', 'librarian', 'member'
        self.name = name

    def append_user(self):
        users = User.load_users()

        for u in users:
            if u['username'] == self.username:
                raise Exception("Username already exists")

        with open(User.USERS_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=User.fieldnames)
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(vars(self))

    @staticmethod
    def load_users():
        if not os.path.exists(User.USERS_FILE):
            return []
        with open(User.USERS_FILE, 'r', newline='') as f:
            return list(csv.DictReader(f))

    @staticmethod
    def authenticate(username, password):
        """Verify login credentials"""
        users = User.load_users()
        
        for user in users:
            if user['username'] == username and user['password'] == password:
                return {
                    'username': user['username'],
                    'role': user['role'],
                    'name': user['name']
                }
        
        return None

    @staticmethod
    def create_default_users():
        """Create default users if none exist"""
        users = User.load_users()
        
        if not users:
            # Create default admin
            admin = User('admin', 'admin123', 'admin', 'Administrator')
            admin.append_user()
            
            # Create default librarian
            librarian = User('librarian', 'lib123', 'librarian', 'Librarian User')
            librarian.append_user()
            
            # Create default member
            member = User('member', 'mem123', 'member', 'Member User')
            member.append_user()

# ==========================
# 🏛️ Library Class
# ==========================
class Library:

    @staticmethod
    def borrow_book(member_id, isbn, days=14):
        """Borrow a book with due date (default 14 days)"""
        # Check for overdue books first
        overdue = Library.get_overdue_books(member_id)
        if overdue:
            raise Exception(f"Member has {len(overdue)} overdue book(s). Please return them first.")
        
        books = Book.load_books()
        found = False

        for book in books:
            if book['isbn'] == isbn:
                found = True
                if book['available'] == 'False':
                    raise Exception("Book already issued")
                book['available'] = 'False'

        if not found:
            raise Exception("Book not found")

        Library._save_books(books)
        
        # Calculate due date
        from datetime import timedelta
        due_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        
        Library._log(member_id, isbn, "BORROW", due_date)

    @staticmethod
    def return_book(member_id, isbn):
        books = Book.load_books()
        found = False

        for book in books:
            if book['isbn'] == isbn:
                found = True
                book['available'] = 'True'

        if not found:
            raise Exception("Book not found")

        Library._save_books(books)
        Library._log(member_id, isbn, "RETURN")

    @staticmethod
    def view_transactions():
        if not os.path.exists(TRANSACTIONS_FILE):
            return []
        with open(TRANSACTIONS_FILE, 'r', newline='') as f:
            return list(csv.DictReader(f))

    @staticmethod
    def _save_books(books):
        with open(BOOKS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=Book.fieldnames)
            writer.writeheader()
            writer.writerows(books)

    @staticmethod
    def _log(member_id, isbn, action, due_date=None):
        with open(TRANSACTIONS_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['member_id', 'isbn', 'action', 'date', 'due_date']
            )
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow({
                'member_id': member_id,
                'isbn': isbn,
                'action': action,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'due_date': due_date if due_date else ''
            })

    @staticmethod
    def search_books(query, filter_by='all'):
        """
        Search books by query string
        filter_by: 'all', 'available', 'borrowed'
        """
        books = Book.load_books()
        results = []
        
        query = query.lower()
        
        for book in books:
            # Check if query matches title, author, or isbn
            if (query in book['title'].lower() or 
                query in book['author'].lower() or 
                query in book['isbn']):
                
                # Apply availability filter
                if filter_by == 'all':
                    results.append(book)
                elif filter_by == 'available' and book['available'] == 'True':
                    results.append(book)
                elif filter_by == 'borrowed' and book['available'] == 'False':
                    results.append(book)
        
        return results
    
    @staticmethod
    def view_all_books():
        """Return all books with formatted info"""
        return Book.load_books()

    @staticmethod
    def view_all_members():
        """Return all members"""
        return Member.load_members()
    
    @staticmethod
    def delete_book(isbn):
        """Delete a book by ISBN"""
        books = Book.load_books()
        found = False
        
        for book in books:
            if book['isbn'] == isbn:
                found = True
                if book['available'] == 'False':
                    raise Exception("Cannot delete: Book is currently borrowed")
                break
        
        if not found:
            raise Exception("Book not found")
        
        # Filter out the book to delete
        books = [b for b in books if b['isbn'] != isbn]
        Library._save_books(books)

    @staticmethod
    def edit_book(isbn, new_title=None, new_author=None):
        """Edit book details"""
        books = Book.load_books()
        found = False
        
        for book in books:
            if book['isbn'] == isbn:
                found = True
                if new_title:
                    book['title'] = new_title
                if new_author:
                    book['author'] = new_author
                break
        
        if not found:
            raise Exception("Book not found")
        
        Library._save_books(books)

    @staticmethod
    def delete_member(member_id):
        """Delete a member by ID"""
        members = Member.load_members()
        found = False
        
        for member in members:
            if member['member_id'] == member_id:
                found = True
                break
        
        if not found:
            raise Exception("Member not found")
        
        # Check if member has borrowed books
        transactions = Library.view_transactions()
        borrowed_books = []
        
        for t in transactions:
            if t['member_id'] == member_id and t['action'] == 'BORROW':
                # Check if book was returned
                returned = False
                for t2 in transactions:
                    if t2['member_id'] == member_id and t2['isbn'] == t['isbn'] and t2['action'] == 'RETURN':
                        returned = True
                        break
                if not returned:
                    borrowed_books.append(t['isbn'])
        
        if borrowed_books:
            raise Exception(f"Cannot delete: Member has {len(borrowed_books)} book(s) borrowed")
        
        # Filter out the member to delete
        members = [m for m in members if m['member_id'] != member_id]
        Library._save_members(members)

    @staticmethod
    def edit_member(member_id, new_name=None, new_email=None):
        """Edit member details"""
        members = Member.load_members()
        found = False
        
        for member in members:
            if member['member_id'] == member_id:
                found = True
                if new_name:
                    member['name'] = new_name
                if new_email:
                    member['email'] = new_email
                break
        
        if not found:
            raise Exception("Member not found")
        
        Library._save_members(members)

    @staticmethod
    def _save_members(members):
        """Helper method to save members to CSV"""
        with open(MEMBERS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=Member.fieldnames)
            writer.writeheader()
            writer.writerows(members)
    
    @staticmethod
    def get_dashboard_stats():
        """Get statistics for dashboard"""
        books = Book.load_books()
        members = Member.load_members()
        transactions = Library.view_transactions()
        
        total_books = len(books)
        available_books = sum(1 for b in books if b['available'] == 'True')
        borrowed_books = total_books - available_books
        total_members = len(members)
        
        # Count total borrows and returns
        total_borrows = sum(1 for t in transactions if t['action'] == 'BORROW')
        total_returns = sum(1 for t in transactions if t['action'] == 'RETURN')
        
        # Calculate currently borrowed (borrows - returns)
        currently_borrowed = total_borrows - total_returns
        
        return {
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books,
            'total_members': total_members,
            'total_transactions': len(transactions),
            'total_borrows': total_borrows,
            'total_returns': total_returns,
            'currently_borrowed': currently_borrowed
        }
    
    @staticmethod
    def get_overdue_books(member_id=None):
        """Get overdue books for a specific member or all members"""
        transactions = Library.view_transactions()
        books = Book.load_books()
        overdue_list = []
        
        # Track borrowed books with due dates
        borrowed_books = {}
        
        for t in transactions:
            if t['action'] == 'BORROW' and t.get('due_date'):
                key = f"{t['member_id']}_{t['isbn']}"
                borrowed_books[key] = {
                    'member_id': t['member_id'],
                    'isbn': t['isbn'],
                    'due_date': t['due_date'],
                    'borrow_date': t['date']
                }
            elif t['action'] == 'RETURN':
                key = f"{t['member_id']}_{t['isbn']}"
                if key in borrowed_books:
                    del borrowed_books[key]  # Book returned, remove from borrowed
        
        # Check which borrowed books are overdue
        today = datetime.now()
        
        for key, info in borrowed_books.items():
            if member_id and info['member_id'] != member_id:
                continue
            
            due_date = datetime.strptime(info['due_date'], "%Y-%m-%d")
            
            if today > due_date:
                # Find book title
                book_title = "Unknown"
                for book in books:
                    if book['isbn'] == info['isbn']:
                        book_title = book['title']
                        break
                
                days_overdue = (today - due_date).days
                
                overdue_list.append({
                    'member_id': info['member_id'],
                    'isbn': info['isbn'],
                    'book_title': book_title,
                    'due_date': info['due_date'],
                    'days_overdue': days_overdue
                })
        
        return overdue_list

    @staticmethod
    def get_all_borrowed_with_due():
        """Get all currently borrowed books with due dates"""
        transactions = Library.view_transactions()
        books = Book.load_books()
        borrowed_list = []
        
        # Track borrowed books with due dates
        borrowed_books = {}
        
        for t in transactions:
            if t['action'] == 'BORROW' and t.get('due_date'):
                key = f"{t['member_id']}_{t['isbn']}"
                borrowed_books[key] = {
                    'member_id': t['member_id'],
                    'isbn': t['isbn'],
                    'due_date': t['due_date'],
                    'borrow_date': t['date']
                }
            elif t['action'] == 'RETURN':
                key = f"{t['member_id']}_{t['isbn']}"
                if key in borrowed_books:
                    del borrowed_books[key]
        
        # Add book details
        today = datetime.now()
        
        for key, info in borrowed_books.items():
            book_title = "Unknown"
            for book in books:
                if book['isbn'] == info['isbn']:
                    book_title = book['title']
                    break
            
            due_date = datetime.strptime(info['due_date'], "%Y-%m-%d")
            days_until_due = (due_date - today).days
            is_overdue = days_until_due < 0
            
            borrowed_list.append({
                'member_id': info['member_id'],
                'isbn': info['isbn'],
                'book_title': book_title,
                'due_date': info['due_date'],
                'days_until_due': days_until_due,
                'is_overdue': is_overdue
            })
        
        return borrowed_list
    
    @staticmethod
    def add_user(username, password, role, name):
        """Add a new user (admin only)"""
        user = User(username, password, role, name)
        user.append_user()

    @staticmethod
    def get_all_users():
        """Get all users"""
        return User.load_users()

