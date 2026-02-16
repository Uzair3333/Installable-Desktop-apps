"""
gui/billing.py - Billing page for creating invoices
Create bills with cart, discounts, and generate invoices
"""

import tkinter as tk
from tkinter import ttk, messagebox
from billing_logic import BillingEngine


class BillingPage:
    def __init__(self, parent, db, colors):
        self.parent = parent
        self.db = db
        self.colors = colors
        self.billing = BillingEngine()
        
        # Cart items list
        self.cart_items = []
        
        self.create_billing_page()
        self.load_products_list()
    
    def create_billing_page(self):
        """Create billing page layout"""
        
        # Title
        title = tk.Label(
            self.parent,
            text="Create Invoice",
            font=('Arial', 24, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        title.pack(pady=20)
        
        # Main container
        main_container = tk.Frame(self.parent, bg=self.colors['white'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left side - Product selection
        self.create_product_selection(main_container)
        
        # Right side - Cart and total
        self.create_cart_section(main_container)
    
    def create_product_selection(self, parent):
        """Create product selection form"""
        
        form_frame = tk.Frame(parent, bg=self.colors['white'], relief=tk.RIDGE, borderwidth=2)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=10)
        
        # Form title
        form_title = tk.Label(
            form_frame,
            text="Add Product to Cart",
            font=('Arial', 14, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['white'],
            pady=10
        )
        form_title.pack(fill=tk.X)
        
        # Form fields
        fields_frame = tk.Frame(form_frame, bg=self.colors['white'])
        fields_frame.pack(padx=20, pady=20)
        
        # Product selection
        tk.Label(fields_frame, text="Select Product:", font=('Arial', 10, 'bold'),
                bg=self.colors['white']).grid(row=0, column=0, sticky='w', pady=10)
        
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(
            fields_frame, 
            textvariable=self.product_var,
            font=('Arial', 10),
            width=30,
            state='readonly'
        )
        self.product_combo.grid(row=0, column=1, pady=10, padx=10)
        self.product_combo.bind('<<ComboboxSelected>>', self.on_product_select)
        # Bind Enter to move to quantity
        self.product_combo.bind('<Return>', lambda e: self.quantity_entry.focus())
        
        # Product details display
        self.details_frame = tk.Frame(fields_frame, bg=self.colors['sidebar'], 
                                    relief=tk.SUNKEN, borderwidth=1)
        self.details_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky='ew')
        
        self.price_label = tk.Label(self.details_frame, text="Price: ₹0.00", 
                                    font=('Arial', 10), bg=self.colors['sidebar'])
        self.price_label.pack(anchor='w', padx=10, pady=5)
        
        self.stock_label = tk.Label(self.details_frame, text="Stock: 0", 
                                    font=('Arial', 10), bg=self.colors['sidebar'])
        self.stock_label.pack(anchor='w', padx=10, pady=5)
        
        # Quantity
        tk.Label(fields_frame, text="Quantity:", font=('Arial', 10, 'bold'),
                bg=self.colors['white']).grid(row=2, column=0, sticky='w', pady=10)
        
        self.quantity_entry = tk.Entry(fields_frame, font=('Arial', 10), width=32)
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.grid(row=2, column=1, pady=10, padx=10)
        # Bind Enter to move to discount
        self.quantity_entry.bind('<Return>', lambda e: self.discount_entry.focus())
        # Select all text when focused
        self.quantity_entry.bind('<FocusIn>', lambda e: self.quantity_entry.select_range(0, tk.END))
        
        # Discount
        tk.Label(fields_frame, text="Discount (₹):", font=('Arial', 10, 'bold'),
                bg=self.colors['white']).grid(row=3, column=0, sticky='w', pady=10)
        
        self.discount_entry = tk.Entry(fields_frame, font=('Arial', 10), width=32)
        self.discount_entry.insert(0, "0")
        self.discount_entry.grid(row=3, column=1, pady=10, padx=10)
        # Bind Enter to add to cart
        self.discount_entry.bind('<Return>', lambda e: self.add_to_cart())
        # Select all text when focused
        self.discount_entry.bind('<FocusIn>', lambda e: self.discount_entry.select_range(0, tk.END))
        
        # Add to cart button
        add_btn = tk.Button(
            fields_frame,
            text="Add to Cart (Enter)",
            command=self.add_to_cart,
            bg=self.colors['success'],
            fg=self.colors['white'],
            font=('Arial', 12, 'bold'),
            cursor='hand2',
            width=25,
            pady=10
        )
        add_btn.grid(row=4, column=0, columnspan=2, pady=20)
        # Bind Enter key to button
        add_btn.bind('<Return>', lambda e: self.add_to_cart())
        
        # Clear cart button
        clear_btn = tk.Button(
            fields_frame,
            text="Clear Cart",
            command=self.clear_cart,
            bg=self.colors['danger'],
            fg=self.colors['white'],
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            width=25,
            pady=8
        )
        clear_btn.grid(row=5, column=0, columnspan=2, pady=5)
        # Bind Enter key to button
        clear_btn.bind('<Return>', lambda e: self.clear_cart())
        
        # Set focus to product combo by default
        self.product_combo.focus()
    
    def create_cart_section(self, parent):
        """Create cart display and total section"""
        
        cart_frame = tk.Frame(parent, bg=self.colors['white'])
        cart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=10)
        
        # Cart title
        cart_title = tk.Label(
            cart_frame,
            text="Shopping Cart",
            font=('Arial', 16, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        cart_title.pack(pady=(0, 10))
        
        # Cart table frame
        table_frame = tk.Frame(cart_frame, bg=self.colors['white'])
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create cart treeview
        columns = ('Product', 'Price', 'Qty', 'Discount', 'Subtotal')
        self.cart_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        
        # Define headings
        self.cart_tree.heading('Product', text='Product Name')
        self.cart_tree.heading('Price', text='Price')
        self.cart_tree.heading('Qty', text='Quantity')
        self.cart_tree.heading('Discount', text='Discount')
        self.cart_tree.heading('Subtotal', text='Subtotal')
        
        # Define column widths
        self.cart_tree.column('Product', width=200)
        self.cart_tree.column('Price', width=100, anchor='e')
        self.cart_tree.column('Qty', width=80, anchor='center')
        self.cart_tree.column('Discount', width=100, anchor='e')
        self.cart_tree.column('Subtotal', width=120, anchor='e')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.cart_tree.yview)
        self.cart_tree.configure(yscroll=scrollbar.set)
        
        # Pack
        self.cart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Remove item button
        remove_btn = tk.Button(
            cart_frame,
            text="Remove Selected Item",
            command=self.remove_from_cart,
            bg=self.colors['danger'],
            fg=self.colors['white'],
            font=('Arial', 10, 'bold'),
            cursor='hand2'
        )
        remove_btn.pack(pady=10)
        
        # Total section
        total_frame = tk.Frame(cart_frame, bg=self.colors['sidebar'], 
                              relief=tk.RAISED, borderwidth=2)
        total_frame.pack(fill=tk.X, pady=10)
        
        # Items count
        self.items_label = tk.Label(
            total_frame,
            text="Items: 0",
            font=('Arial', 12, 'bold'),
            bg=self.colors['sidebar']
        )
        self.items_label.pack(anchor='w', padx=20, pady=5)
        
        # Total discount
        self.discount_label = tk.Label(
            total_frame,
            text="Total Discount: ₹0.00",
            font=('Arial', 12, 'bold'),
            bg=self.colors['sidebar']
        )
        self.discount_label.pack(anchor='w', padx=20, pady=5)
        
        # Grand total
        self.total_label = tk.Label(
            total_frame,
            text="Grand Total: ₹0.00",
            font=('Arial', 18, 'bold'),
            bg=self.colors['sidebar'],
            fg=self.colors['primary']
        )
        self.total_label.pack(anchor='w', padx=20, pady=10)
        
        # Generate invoice button
        invoice_btn = tk.Button(
            cart_frame,
            text="Generate Invoice",
            command=self.generate_invoice,
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Arial', 14, 'bold'),
            cursor='hand2',
            pady=15
        )
        invoice_btn.pack(fill=tk.X, padx=20, pady=10)
    
    def load_products_list(self):
        """Load products into combobox"""
        products = self.db.get_all_products()
        
        # Create list of product names with IDs
        self.products_dict = {}
        product_list = []
        
        for product in products:
            product_id = product[0]
            product_name = product[1]
            display_name = f"{product_name} (ID: {product_id})"
            product_list.append(display_name)
            self.products_dict[display_name] = product
        
        self.product_combo['values'] = product_list
    
    def on_product_select(self, event):
        """Handle product selection"""
        selected = self.product_var.get()
        
        if selected and selected in self.products_dict:
            product = self.products_dict[selected]
            # product: (id, name, category, price, stock, low_stock_limit, created_at)
            
            price = product[3]
            stock = product[4]
            
            self.price_label.config(text=f"Price: ₹{price:,.2f}")
            self.stock_label.config(text=f"Available Stock: {stock}")
            
            # Update details frame color based on stock
            if stock <= 0:
                self.details_frame.config(bg='#ffcccc')
                self.price_label.config(bg='#ffcccc')
                self.stock_label.config(bg='#ffcccc')
            elif stock <= product[5]:  # Low stock
                self.details_frame.config(bg='#fff3cd')
                self.price_label.config(bg='#fff3cd')
                self.stock_label.config(bg='#fff3cd')
            else:
                self.details_frame.config(bg=self.colors['sidebar'])
                self.price_label.config(bg=self.colors['sidebar'])
                self.stock_label.config(bg=self.colors['sidebar'])
    
    def add_to_cart(self):
        """Add selected product to cart"""
        selected = self.product_var.get()
        
        if not selected:
            messagebox.showerror("Error", "Please select a product")
            return
        
        if selected not in self.products_dict:
            messagebox.showerror("Error", "Invalid product selected")
            return
        
        product = self.products_dict[selected]
        product_id = product[0]
        product_name = product[1]
        price = product[3]
        stock = product[4]
        
        # Get quantity and discount
        try:
            quantity = int(self.quantity_entry.get())
            discount = float(self.discount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or discount")
            return
        
        # Validate quantity
        valid, msg = self.billing.validate_quantity(stock, quantity)
        if not valid:
            messagebox.showerror("Error", msg)
            return
        
        # Validate discount
        valid, msg = self.billing.validate_discount(price, quantity, discount)
        if not valid:
            messagebox.showerror("Error", msg)
            return
        
        # Create cart item
        cart_item = self.billing.create_cart_item(
            product_id, product_name, price, quantity, discount
        )
        
        # Check if product already in cart
        for i, item in enumerate(self.cart_items):
            if item['product_id'] == product_id:
                # Update quantity
                if messagebox.askyesno("Product Exists", 
                                      f"{product_name} is already in cart. Add more?"):
                    new_qty = item['quantity'] + quantity
                    new_discount = item['discount'] + discount
                    
                    # Validate new quantity
                    valid, msg = self.billing.validate_quantity(stock, new_qty)
                    if not valid:
                        messagebox.showerror("Error", msg)
                        return
                    
                    # Update item
                    self.cart_items[i] = self.billing.create_cart_item(
                        product_id, product_name, price, new_qty, new_discount
                    )
                    self.update_cart_display()
                    return
                else:
                    return
        
        # Add new item to cart
        self.cart_items.append(cart_item)
        self.update_cart_display()
        
        # Reset quantity and discount
        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.insert(0, "1")
        self.discount_entry.delete(0, tk.END)
        self.discount_entry.insert(0, "0")
        
        messagebox.showinfo("Success", f"{product_name} added to cart")
    
    def update_cart_display(self):
        """Update cart treeview and totals"""
        # Clear cart display
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Add items to cart display
        for item in self.cart_items:
            self.cart_tree.insert('', tk.END, values=(
                item['product_name'],
                self.billing.format_currency(item['price']),
                item['quantity'],
                self.billing.format_currency(item['discount']),
                self.billing.format_currency(item['subtotal'])
            ))
        
        # Update summary
        if self.cart_items:
            summary = self.billing.get_invoice_summary(self.cart_items)
            self.items_label.config(text=f"Items: {summary['items_count']}")
            self.discount_label.config(
                text=f"Total Discount: {self.billing.format_currency(summary['total_discount'])}"
            )
            self.total_label.config(
                text=f"Grand Total: {self.billing.format_currency(summary['final_amount'])}"
            )
        else:
            self.items_label.config(text="Items: 0")
            self.discount_label.config(text="Total Discount: ₹0.00")
            self.total_label.config(text="Grand Total: ₹0.00")
    
    def remove_from_cart(self):
        """Remove selected item from cart"""
        selection = self.cart_tree.selection()
        
        if not selection:
            messagebox.showerror("Error", "No item selected")
            return
        
        # Get selected item index
        item = self.cart_tree.item(selection[0])
        product_name = item['values'][0]
        
        # Find and remove from cart_items
        for i, cart_item in enumerate(self.cart_items):
            if cart_item['product_name'] == product_name:
                self.cart_items.pop(i)
                break
        
        self.update_cart_display()
        messagebox.showinfo("Success", f"{product_name} removed from cart")
    
    def clear_cart(self):
        """Clear all items from cart"""
        if not self.cart_items:
            messagebox.showinfo("Info", "Cart is already empty")
            return
        
        if messagebox.askyesno("Confirm", "Clear all items from cart?"):
            self.cart_items.clear()
            self.update_cart_display()
            messagebox.showinfo("Success", "Cart cleared")
    
    def generate_invoice(self):
        """Generate invoice and save to database"""
        if not self.cart_items:
            messagebox.showerror("Error", "Cart is empty. Add products first.")
            return
        
        # Confirm invoice generation
        summary = self.billing.get_invoice_summary(self.cart_items)
        confirm_msg = f"Generate invoice for {summary['items_count']} items?\n\n"
        confirm_msg += f"Total Amount: {self.billing.format_currency(summary['final_amount'])}"
        
        if not messagebox.askyesno("Confirm Invoice", confirm_msg):
            return
        
        # Create invoice in database
        success, invoice_number, message = self.db.create_invoice(self.cart_items)
        
        if success:
            messagebox.showinfo(
                "Success", 
                f"Invoice generated successfully!\n\nInvoice Number: {invoice_number}\n"
                f"Total Amount: {self.billing.format_currency(summary['final_amount'])}"
            )
            
            # Clear cart
            self.cart_items.clear()
            self.update_cart_display()
            
            # Refresh products list (stock updated)
            self.load_products_list()
        else:
            messagebox.showerror("Error", f"Failed to generate invoice:\n{message}")