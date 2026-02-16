"""
database.py - Database management for Smart Inventory & Billing System
Handles SQLite database connection, table creation, and all database operations
"""

import sqlite3
from datetime import datetime
import os


class Database:
    def __init__(self, db_name='inventory.db'):
        """Initialize database connection"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            # Enable foreign keys
            self.cursor.execute("PRAGMA foreign_keys = ON")
        except sqlite3.Error as e:
            raise Exception(f"Database connection error: {e}")
    
    def create_tables(self):
        """Create all necessary tables if they don't exist"""
        try:
            # Products table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT,
                    price REAL NOT NULL CHECK(price >= 0),
                    stock INTEGER NOT NULL CHECK(stock >= 0),
                    low_stock_limit INTEGER DEFAULT 5,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Invoices table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS invoices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_number TEXT UNIQUE NOT NULL,
                    total_amount REAL NOT NULL,
                    date TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Invoice items table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS invoice_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL CHECK(quantity > 0),
                    price REAL NOT NULL,
                    discount REAL DEFAULT 0 CHECK(discount >= 0),
                    subtotal REAL NOT NULL,
                    FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            ''')
            
            self.conn.commit()
            
        except sqlite3.Error as e:
            raise Exception(f"Error creating tables: {e}")
    
    # ==================== PRODUCT OPERATIONS ====================
    
    def add_product(self, name, category, price, stock, low_stock_limit=5):
        """Add a new product to database"""
        try:
            self.cursor.execute('''
                INSERT INTO products (name, category, price, stock, low_stock_limit)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, category, price, stock, low_stock_limit))
            self.conn.commit()
            return True, "Product added successfully"
        except sqlite3.Error as e:
            return False, f"Error adding product: {e}"
    
    def get_all_products(self):
        """Retrieve all products"""
        try:
            self.cursor.execute('SELECT * FROM products ORDER BY id DESC')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            return []
    
    def get_product_by_id(self, product_id):
        """Get a single product by ID"""
        try:
            self.cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            return None
    
    def update_product(self, product_id, name, category, price, stock, low_stock_limit):
        """Update an existing product"""
        try:
            self.cursor.execute('''
                UPDATE products 
                SET name = ?, category = ?, price = ?, stock = ?, low_stock_limit = ?
                WHERE id = ?
            ''', (name, category, price, stock, low_stock_limit, product_id))
            self.conn.commit()
            return True, "Product updated successfully"
        except sqlite3.Error as e:
            return False, f"Error updating product: {e}"
    
    def delete_product(self, product_id):
        """Delete a product from database"""
        try:
            self.cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            self.conn.commit()
            return True, "Product deleted successfully"
        except sqlite3.Error as e:
            return False, f"Error deleting product: {e}"
    
    def search_products(self, search_term):
        """Search products by name or category"""
        try:
            self.cursor.execute('''
                SELECT * FROM products 
                WHERE name LIKE ? OR category LIKE ?
                ORDER BY name
            ''', (f'%{search_term}%', f'%{search_term}%'))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            return []
    
    def get_low_stock_products(self):
        """Get products with stock below low_stock_limit"""
        try:
            self.cursor.execute('''
                SELECT * FROM products 
                WHERE stock <= low_stock_limit
                ORDER BY stock ASC
            ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            return []
    
    def update_stock(self, product_id, quantity):
        """Update product stock (reduce after sale)"""
        try:
            self.cursor.execute('''
                UPDATE products 
                SET stock = stock - ?
                WHERE id = ?
            ''', (quantity, product_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            return False
    
    # ==================== INVOICE OPERATIONS ====================
    
    def generate_invoice_number(self):
        """Generate unique invoice number"""
        try:
            # Get the latest invoice number
            self.cursor.execute('SELECT invoice_number FROM invoices ORDER BY id DESC LIMIT 1')
            result = self.cursor.fetchone()
            
            if result:
                # Extract number from last invoice (e.g., INV-0001 -> 1)
                last_num = int(result[0].split('-')[1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            # Format as INV-0001, INV-0002, etc.
            return f"INV-{new_num:04d}"
        except Exception as e:
            return f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def create_invoice(self, cart_items):
        """
        Create invoice with items (Transaction-safe)
        cart_items: list of dicts with keys: product_id, quantity, price, discount, subtotal
        """
        try:
            # Start transaction
            self.conn.execute("BEGIN TRANSACTION")
            
            # Generate invoice number
            invoice_number = self.generate_invoice_number()
            
            # Calculate total amount
            total_amount = sum(item['subtotal'] for item in cart_items)
            
            # Insert invoice
            self.cursor.execute('''
                INSERT INTO invoices (invoice_number, total_amount)
                VALUES (?, ?)
            ''', (invoice_number, total_amount))
            
            invoice_id = self.cursor.lastrowid
            
            # Insert invoice items and update stock
            for item in cart_items:
                # Insert invoice item
                self.cursor.execute('''
                    INSERT INTO invoice_items 
                    (invoice_id, product_id, quantity, price, discount, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (invoice_id, item['product_id'], item['quantity'], 
                      item['price'], item['discount'], item['subtotal']))
                
                # Reduce stock
                self.update_stock(item['product_id'], item['quantity'])
            
            # Commit transaction
            self.conn.commit()
            return True, invoice_number, "Invoice created successfully"
            
        except sqlite3.Error as e:
            # Rollback on error
            self.conn.rollback()
            return False, None, f"Error creating invoice: {e}"
    
    def get_all_invoices(self):
        """Retrieve all invoices"""
        try:
            self.cursor.execute('SELECT * FROM invoices ORDER BY id DESC')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            return []
    
    def get_invoice_details(self, invoice_id):
        """Get invoice with all items"""
        try:
            # Get invoice header
            self.cursor.execute('SELECT * FROM invoices WHERE id = ?', (invoice_id,))
            invoice = self.cursor.fetchone()
            
            if not invoice:
                return None
            
            # Get invoice items with product names
            self.cursor.execute('''
                SELECT ii.*, p.name as product_name 
                FROM invoice_items ii
                JOIN products p ON ii.product_id = p.id
                WHERE ii.invoice_id = ?
            ''', (invoice_id,))
            items = self.cursor.fetchall()
            
            return {'invoice': invoice, 'items': items}
        except sqlite3.Error as e:
            return None
    
    def search_invoices(self, search_term):
        """Search invoices by invoice number or date"""
        try:
            self.cursor.execute('''
                SELECT * FROM invoices 
                WHERE invoice_number LIKE ? OR date LIKE ?
                ORDER BY date DESC
            ''', (f'%{search_term}%', f'%{search_term}%'))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            return []
    
    # ==================== STATISTICS & REPORTS ====================
    
    def get_total_products(self):
        """Get count of all products"""
        try:
            self.cursor.execute('SELECT COUNT(*) FROM products')
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            return 0
    
    def get_today_sales(self):
        """Get today's total sales"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            self.cursor.execute('''
                SELECT COALESCE(SUM(total_amount), 0) 
                FROM invoices 
                WHERE DATE(date) = ?
            ''', (today,))
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            return 0
    
    def get_total_invoices(self):
        """Get count of all invoices"""
        try:
            self.cursor.execute('SELECT COUNT(*) FROM invoices')
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            return 0
    
    def get_low_stock_count(self):
        """Get count of low stock products"""
        try:
            self.cursor.execute('SELECT COUNT(*) FROM products WHERE stock <= low_stock_limit')
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            return 0
    
    # ==================== DATABASE UTILITIES ====================
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()