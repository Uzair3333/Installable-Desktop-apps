"""
gui/products.py - Products management page
Add, Edit, Delete, and View products
"""

import tkinter as tk
from tkinter import ttk, messagebox


class ProductsPage:
    def __init__(self, parent, db, colors):
        self.parent = parent
        self.db = db
        self.colors = colors
        self.selected_product_id = None
        
        self.create_products_page()
        self.load_products()
    
    def create_products_page(self):
        """Create products page layout"""
        
        # Title
        title = tk.Label(
            self.parent,
            text="Product Management",
            font=('Arial', 24, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        title.pack(pady=20)
        
        # Main container
        main_container = tk.Frame(self.parent, bg=self.colors['white'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left side - Form
        self.create_form(main_container)
        
        # Right side - Table
        self.create_table(main_container)
    
    def create_form(self, parent):
        """Create product input form"""
        
        form_frame = tk.Frame(parent, bg=self.colors['white'], relief=tk.RIDGE, borderwidth=2)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=10)
        
        # Form title
        form_title = tk.Label(
            form_frame,
            text="Product Details",
            font=('Arial', 14, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['white'],
            pady=10
        )
        form_title.pack(fill=tk.X)
        
        # Form fields container
        fields_frame = tk.Frame(form_frame, bg=self.colors['white'])
        fields_frame.pack(padx=20, pady=20)
        
        # Product Name
        tk.Label(fields_frame, text="Product Name:", font=('Arial', 10, 'bold'), 
                bg=self.colors['white']).grid(row=0, column=0, sticky='w', pady=10)
        self.name_entry = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.name_entry.grid(row=0, column=1, pady=10, padx=10)
        # Bind Enter to move to next field
        self.name_entry.bind('<Return>', lambda e: self.category_entry.focus())
        
        # Category
        tk.Label(fields_frame, text="Category:", font=('Arial', 10, 'bold'), 
                bg=self.colors['white']).grid(row=1, column=0, sticky='w', pady=10)
        self.category_entry = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.category_entry.grid(row=1, column=1, pady=10, padx=10)
        # Bind Enter to move to next field
        self.category_entry.bind('<Return>', lambda e: self.price_entry.focus())
        
        # Price
        tk.Label(fields_frame, text="Price (₹):", font=('Arial', 10, 'bold'), 
                bg=self.colors['white']).grid(row=2, column=0, sticky='w', pady=10)
        self.price_entry = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.price_entry.grid(row=2, column=1, pady=10, padx=10)
        # Bind Enter to move to next field
        self.price_entry.bind('<Return>', lambda e: self.stock_entry.focus())
        
        # Stock
        tk.Label(fields_frame, text="Stock Quantity:", font=('Arial', 10, 'bold'), 
                bg=self.colors['white']).grid(row=3, column=0, sticky='w', pady=10)
        self.stock_entry = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.stock_entry.grid(row=3, column=1, pady=10, padx=10)
        # Bind Enter to move to next field
        self.stock_entry.bind('<Return>', lambda e: self.low_stock_entry.focus())
        
        # Low Stock Limit
        tk.Label(fields_frame, text="Low Stock Limit:", font=('Arial', 10, 'bold'), 
                bg=self.colors['white']).grid(row=4, column=0, sticky='w', pady=10)
        self.low_stock_entry = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.low_stock_entry.insert(0, "5")  # Default value
        self.low_stock_entry.grid(row=4, column=1, pady=10, padx=10)
        # Bind Enter to add/update product
        self.low_stock_entry.bind('<Return>', lambda e: self.add_product() if self.add_btn['state'] == 'normal' else self.update_product())
        
        # Buttons frame
        btn_frame = tk.Frame(fields_frame, bg=self.colors['white'])
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Add button
        self.add_btn = tk.Button(
            btn_frame,
            text="Add Product",
            command=self.add_product,
            bg=self.colors['success'],
            fg=self.colors['white'],
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            width=12,
            relief=tk.RAISED,
            borderwidth=2
        )
        self.add_btn.pack(side=tk.LEFT, padx=5)
        # Bind Enter key when button has focus
        self.add_btn.bind('<Return>', lambda e: self.add_product())
        
        # Update button
        self.update_btn = tk.Button(
            btn_frame,
            text="Update",
            command=self.update_product,
            bg=self.colors['warning'],
            fg=self.colors['text'],
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            width=12,
            relief=tk.RAISED,
            borderwidth=2,
            state=tk.DISABLED
        )
        self.update_btn.pack(side=tk.LEFT, padx=5)
        # Bind Enter key when button has focus
        self.update_btn.bind('<Return>', lambda e: self.update_product())
        
        # Clear button
        self.clear_btn = tk.Button(
            btn_frame,
            text="Clear",
            command=self.clear_form,
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            width=12,
            relief=tk.RAISED,
            borderwidth=2
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        # Bind Enter key when button has focus
        self.clear_btn.bind('<Return>', lambda e: self.clear_form())
        
        # Focus on name entry by default
        self.name_entry.focus()
        
    def create_table(self, parent):
        """Create products table"""
        
        table_frame = tk.Frame(parent, bg=self.colors['white'])
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=10)
        
        # Search frame
        search_frame = tk.Frame(table_frame, bg=self.colors['white'])
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", font=('Arial', 10, 'bold'), 
                bg=self.colors['white']).pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_products())
        
        search_btn = tk.Button(
            search_frame,
            text="Search",
            command=self.search_products,
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Arial', 9, 'bold'),
            cursor='hand2'
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(
            search_frame,
            text="Refresh",
            command=self.load_products,
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            font=('Arial', 9, 'bold'),
            cursor='hand2'
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Treeview frame
        tree_frame = tk.Frame(table_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview
        columns = ('ID', 'Name', 'Category', 'Price', 'Stock', 'Low Limit')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Product Name')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Price', text='Price (₹)')
        self.tree.heading('Stock', text='Stock')
        self.tree.heading('Low Limit', text='Low Stock Limit')
        
        # Define column widths
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Name', width=200)
        self.tree.column('Category', width=120)
        self.tree.column('Price', width=100, anchor='e')
        self.tree.column('Stock', width=80, anchor='center')
        self.tree.column('Low Limit', width=120, anchor='center')
        
        # Add scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        
        # Pack tree and scrollbars
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_product_select)
        
        # Action buttons frame
        action_frame = tk.Frame(table_frame, bg=self.colors['white'])
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        delete_btn = tk.Button(
            action_frame,
            text="Delete Selected",
            command=self.delete_product,
            bg=self.colors['danger'],
            fg=self.colors['white'],
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            width=15
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Product count label
        self.count_label = tk.Label(
            action_frame,
            text="Total Products: 0",
            font=('Arial', 10, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        self.count_label.pack(side=tk.RIGHT, padx=10)
    
    def load_products(self):
        """Load all products from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get products from database
        products = self.db.get_all_products()
        
        # Insert into treeview
        for product in products:
            self.tree.insert('', tk.END, values=(
                product[0],  # ID
                product[1],  # Name
                product[2],  # Category
                f"₹{product[3]:.2f}",  # Price
                product[4],  # Stock
                product[5]   # Low stock limit
            ))
        
        # Update count
        self.count_label.config(text=f"Total Products: {len(products)}")
        
        # Clear search
        self.search_entry.delete(0, tk.END)
    
    def search_products(self):
        """Search products by name or category"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            self.load_products()
            return
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Search in database
        products = self.db.search_products(search_term)
        
        # Insert results
        for product in products:
            self.tree.insert('', tk.END, values=(
                product[0],
                product[1],
                product[2],
                f"₹{product[3]:.2f}",
                product[4],
                product[5]
            ))
        
        # Update count
        self.count_label.config(text=f"Found: {len(products)} products")
    
    def add_product(self):
        """Add new product"""
        # Get values
        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        price = self.price_entry.get().strip()
        stock = self.stock_entry.get().strip()
        low_limit = self.low_stock_entry.get().strip()
        
        # Validate
        if not name:
            messagebox.showerror("Error", "Product name is required")
            return
        
        if not price or not stock:
            messagebox.showerror("Error", "Price and stock are required")
            return
        
        try:
            price = float(price)
            stock = int(stock)
            low_limit = int(low_limit) if low_limit else 5
            
            if price < 0 or stock < 0 or low_limit < 0:
                messagebox.showerror("Error", "Values cannot be negative")
                return
            
        except ValueError:
            messagebox.showerror("Error", "Invalid price, stock, or low limit value")
            return
        
        # Add to database
        success, message = self.db.add_product(name, category, price, stock, low_limit)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.load_products()
        else:
            messagebox.showerror("Error", message)
    
    def on_product_select(self, event):
        """Handle product selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            # Store product ID
            self.selected_product_id = values[0]
            
            # Fill form
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])
            
            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, values[2])
            
            self.price_entry.delete(0, tk.END)
            # Remove ₹ symbol and convert to float
            price_str = values[3].replace('₹', '').replace(',', '')
            self.price_entry.insert(0, price_str)
            
            self.stock_entry.delete(0, tk.END)
            self.stock_entry.insert(0, values[4])
            
            self.low_stock_entry.delete(0, tk.END)
            self.low_stock_entry.insert(0, values[5])
            
            # Enable update button
            self.update_btn.config(state=tk.NORMAL)
            self.add_btn.config(state=tk.DISABLED)
    
    def update_product(self):
        """Update selected product"""
        if not self.selected_product_id:
            messagebox.showerror("Error", "No product selected")
            return
        
        # Get values
        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        price = self.price_entry.get().strip()
        stock = self.stock_entry.get().strip()
        low_limit = self.low_stock_entry.get().strip()
        
        # Validate
        if not name or not price or not stock:
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            price = float(price)
            stock = int(stock)
            low_limit = int(low_limit) if low_limit else 5
            
            if price < 0 or stock < 0 or low_limit < 0:
                messagebox.showerror("Error", "Values cannot be negative")
                return
            
        except ValueError:
            messagebox.showerror("Error", "Invalid values")
            return
        
        # Update in database
        success, message = self.db.update_product(
            self.selected_product_id, name, category, price, stock, low_limit
        )
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.load_products()
        else:
            messagebox.showerror("Error", message)
    
    def delete_product(self):
        """Delete selected product"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Error", "No product selected")
            return
        
        item = self.tree.item(selection[0])
        product_id = item['values'][0]
        product_name = item['values'][1]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", 
                               f"Are you sure you want to delete '{product_name}'?"):
            success, message = self.db.delete_product(product_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.clear_form()
                self.load_products()
            else:
                messagebox.showerror("Error", message)
    
    def clear_form(self):
        """Clear all form fields"""
        self.name_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.low_stock_entry.delete(0, tk.END)
        self.low_stock_entry.insert(0, "5")
        
        self.selected_product_id = None
        self.update_btn.config(state=tk.DISABLED)
        self.add_btn.config(state=tk.NORMAL)
        
        # Clear selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)