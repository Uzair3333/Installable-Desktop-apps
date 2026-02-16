"""
gui/invoices.py - Invoices viewing page
View all invoices and their details
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gui.scrollable_frame import ScrollableFrame


class InvoicesPage:
    def __init__(self, parent, db, colors):
        self.parent = parent
        self.db = db
        self.colors = colors
        
        self.create_invoices_page()
        self.load_invoices()
    
    def create_invoices_page(self):
        """Create invoices page layout"""
        
        # Create scrollable container
        scroll_container = ScrollableFrame(self.parent, bg=self.colors['white'])
        scroll_container.pack(fill=tk.BOTH, expand=True)
        
        # Use scrollable_frame instead of parent
        container = scroll_container.scrollable_frame
        
        # Title
        title = tk.Label(
            container,
            text="Invoice History",
            font=('Arial', 24, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        title.pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(container, bg=self.colors['white'])
        search_frame.pack(fill=tk.X, padx=40, pady=(0, 10))
        
        tk.Label(
            search_frame, 
            text="Search:", 
            font=('Arial', 11, 'bold'),
            bg=self.colors['white']
        ).pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 11), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        # Bind Enter to search
        self.search_entry.bind('<Return>', lambda e: self.search_invoices())
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_invoices())
        
        search_btn = tk.Button(
            search_frame,
            text="Search",
            command=self.search_invoices,
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            width=10
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        search_btn.bind('<Return>', lambda e: self.search_invoices())
        
        refresh_btn = tk.Button(
            search_frame,
            text="Refresh",
            command=self.load_invoices,
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            width=10
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        refresh_btn.bind('<Return>', lambda e: self.load_invoices())
        
        # Invoices table frame
        table_frame = tk.Frame(container, bg=self.colors['white'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        # Create treeview
        columns = ('ID', 'Invoice Number', 'Total Amount', 'Date')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.tree.heading('ID', text='ID')
        self.tree.heading('Invoice Number', text='Invoice Number')
        self.tree.heading('Total Amount', text='Total Amount')
        self.tree.heading('Date', text='Date & Time')
        
        # Define column widths
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Invoice Number', width=150, anchor='center')
        self.tree.column('Total Amount', width=150, anchor='e')
        self.tree.column('Date', width=250)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        
        # Pack tree and scrollbars
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind double-click and Enter to view details
        self.tree.bind('<Double-Button-1>', self.view_invoice_details)
        self.tree.bind('<Return>', self.view_invoice_details)
        
        # Action buttons frame
        action_frame = tk.Frame(container, bg=self.colors['white'])
        action_frame.pack(fill=tk.X, padx=40, pady=10)
        
        view_btn = tk.Button(
            action_frame,
            text="View Details (Enter)",
            command=lambda: self.view_invoice_details(None),
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            width=20,
            pady=8
        )
        view_btn.pack(side=tk.LEFT, padx=5)
        view_btn.bind('<Return>', lambda e: self.view_invoice_details(None))
        
        # Invoice count label
        self.count_label = tk.Label(
            action_frame,
            text="Total Invoices: 0",
            font=('Arial', 11, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        self.count_label.pack(side=tk.RIGHT, padx=10)
        
        # Set focus to search
        self.search_entry.focus()
    
    # ... rest of the methods stay the same ...
    
    def load_invoices(self):
        """Load all invoices from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get invoices from database
        invoices = self.db.get_all_invoices()
        
        # Insert into treeview
        for invoice in invoices:
            self.tree.insert('', tk.END, values=(
                invoice[0],  # ID
                invoice[1],  # Invoice Number
                f"₹{invoice[2]:,.2f}",  # Total Amount
                invoice[3]   # Date
            ))
        
        # Update count
        self.count_label.config(text=f"Total Invoices: {len(invoices)}")
        
        # Clear search
        self.search_entry.delete(0, tk.END)
    
    def search_invoices(self):
        """Search invoices by invoice number or date"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            self.load_invoices()
            return
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Search in database
        invoices = self.db.search_invoices(search_term)
        
        # Insert results
        for invoice in invoices:
            self.tree.insert('', tk.END, values=(
                invoice[0],
                invoice[1],
                f"₹{invoice[2]:,.2f}",
                invoice[3]
            ))
        
        # Update count
        self.count_label.config(text=f"Found: {len(invoices)} invoices")
    
    def view_invoice_details(self, event):
        """View detailed invoice information"""
        selection = self.tree.selection()
        
        if not selection:
            messagebox.showerror("Error", "Please select an invoice to view")
            return
        
        item = self.tree.item(selection[0])
        invoice_id = item['values'][0]
        
        # Get invoice details
        invoice_data = self.db.get_invoice_details(invoice_id)
        
        if not invoice_data:
            messagebox.showerror("Error", "Could not load invoice details")
            return
        
        # Create details window
        self.show_invoice_details_window(invoice_data)
    
    def show_invoice_details_window(self, invoice_data):
        """Show invoice details in a new window"""
        invoice = invoice_data['invoice']
        items = invoice_data['items']
        
        # Create new window
        details_window = tk.Toplevel(self.parent)
        details_window.title(f"Invoice Details - {invoice[1]}")
        details_window.geometry("700x600")
        details_window.configure(bg=self.colors['white'])
        
        # Make it modal
        details_window.transient(self.parent)
        details_window.grab_set()
        
        # Header
        header = tk.Frame(details_window, bg=self.colors['primary'], pady=15)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text=f"Invoice: {invoice[1]}",
            font=('Arial', 18, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['white']
        ).pack()
        
        tk.Label(
            header,
            text=f"Date: {invoice[3]}",
            font=('Arial', 11),
            bg=self.colors['primary'],
            fg=self.colors['white']
        ).pack()
        
        # Items section
        items_frame = tk.Frame(details_window, bg=self.colors['white'])
        items_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            items_frame,
            text="Invoice Items",
            font=('Arial', 14, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(anchor='w', pady=(0, 10))
        
        # Items table
        columns = ('Product', 'Price', 'Qty', 'Discount', 'Subtotal')
        items_tree = ttk.Treeview(items_frame, columns=columns, show='headings', height=10)
        
        items_tree.heading('Product', text='Product Name')
        items_tree.heading('Price', text='Price')
        items_tree.heading('Qty', text='Quantity')
        items_tree.heading('Discount', text='Discount')
        items_tree.heading('Subtotal', text='Subtotal')
        
        items_tree.column('Product', width=250)
        items_tree.column('Price', width=100, anchor='e')
        items_tree.column('Qty', width=80, anchor='center')
        items_tree.column('Discount', width=100, anchor='e')
        items_tree.column('Subtotal', width=120, anchor='e')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(items_frame, orient=tk.VERTICAL, command=items_tree.yview)
        items_tree.configure(yscroll=scrollbar.set)
        
        items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert items
        for item in items:
            # item: (id, invoice_id, product_id, quantity, price, discount, subtotal, product_name)
            items_tree.insert('', tk.END, values=(
                item[7],  # product_name
                f"₹{item[4]:,.2f}",  # price
                item[3],  # quantity
                f"₹{item[5]:,.2f}",  # discount
                f"₹{item[6]:,.2f}"   # subtotal
            ))
        
        # Total section
        total_frame = tk.Frame(details_window, bg=self.colors['sidebar'], relief=tk.RAISED, borderwidth=2)
        total_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Calculate totals
        total_items = len(items)
        total_discount = sum(item[5] for item in items)
        subtotal = sum(item[4] * item[3] for item in items)
        
        tk.Label(
            total_frame,
            text=f"Total Items: {total_items}",
            font=('Arial', 12, 'bold'),
            bg=self.colors['sidebar']
        ).pack(anchor='w', padx=20, pady=5)
        
        tk.Label(
            total_frame,
            text=f"Subtotal: ₹{subtotal:,.2f}",
            font=('Arial', 12, 'bold'),
            bg=self.colors['sidebar']
        ).pack(anchor='w', padx=20, pady=5)
        
        tk.Label(
            total_frame,
            text=f"Total Discount: ₹{total_discount:,.2f}",
            font=('Arial', 12, 'bold'),
            bg=self.colors['sidebar']
        ).pack(anchor='w', padx=20, pady=5)
        
        tk.Label(
            total_frame,
            text=f"Grand Total: ₹{invoice[2]:,.2f}",
            font=('Arial', 16, 'bold'),
            bg=self.colors['sidebar'],
            fg=self.colors['primary']
        ).pack(anchor='w', padx=20, pady=10)
        
        # Close button
        close_btn = tk.Button(
            details_window,
            text="Close",
            command=details_window.destroy,
            bg=self.colors['danger'],
            fg=self.colors['white'],
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            width=15,
            pady=8
        )
        close_btn.pack(pady=(0, 20))