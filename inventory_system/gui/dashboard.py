"""
gui/dashboard.py - Dashboard page for Smart Inventory & Billing System
Shows statistics and overview
"""

import tkinter as tk
from tkinter import ttk
from gui.scrollable_frame import ScrollableFrame


class DashboardPage:
    def __init__(self, parent, db, colors):
        self.parent = parent
        self.db = db
        self.colors = colors
        
        self.create_dashboard()
    
    def create_dashboard(self):
        """Create dashboard layout"""
        
        # Create scrollable container
        scroll_container = ScrollableFrame(self.parent, bg=self.colors['white'])
        scroll_container.pack(fill=tk.BOTH, expand=True)
        
        # Use scrollable_frame instead of parent
        container = scroll_container.scrollable_frame
        
        # Title
        title = tk.Label(
            container,
            text="Dashboard",
            font=('Arial', 24, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        title.pack(pady=20)
        
        # Stats container
        stats_frame = tk.Frame(container, bg=self.colors['white'])
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Get statistics from database
        total_products = self.db.get_total_products()
        today_sales = self.db.get_today_sales()
        total_invoices = self.db.get_total_invoices()
        low_stock_count = self.db.get_low_stock_count()
        
        # Create stat cards
        stats_data = [
            ("Total Products", total_products, self.colors['primary'], "📦"),
            ("Today's Sales", f"₹{today_sales:,.2f}", self.colors['success'], "💰"),
            ("Total Invoices", total_invoices, self.colors['secondary'], "📄"),
            ("Low Stock Items", low_stock_count, self.colors['danger'], "⚠️"),
        ]
        
        # Create cards in a grid
        for i, (title_text, value, color, icon) in enumerate(stats_data):
            row = i // 2
            col = i % 2
            self.create_stat_card(stats_frame, title_text, value, color, icon, row, col)
        
        # Low stock products section
        if low_stock_count > 0:
            self.create_low_stock_section(container)
        else:
            # Show a message when no low stock
            no_low_stock = tk.Label(
                container,
                text="✓ All products are well stocked!",
                font=('Arial', 14, 'bold'),
                bg=self.colors['white'],
                fg=self.colors['success']
            )
            no_low_stock.pack(pady=30)
    
    def create_stat_card(self, parent, title_text, value, color, icon, row, col):
        """Create a statistics card"""
        
        card = tk.Frame(
            parent,
            bg=color,
            relief=tk.RAISED,
            borderwidth=2
        )
        card.grid(row=row, column=col, padx=20, pady=20, sticky='nsew')
        
        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Icon
        icon_label = tk.Label(
            card,
            text=icon,
            font=('Arial', 40),
            bg=color,
            fg=self.colors['white']
        )
        icon_label.pack(pady=(20, 10))
        
        # Value
        value_label = tk.Label(
            card,
            text=str(value),
            font=('Arial', 28, 'bold'),
            bg=color,
            fg=self.colors['white']
        )
        value_label.pack()
        
        # Title
        title_label = tk.Label(
            card,
            text=title_text,
            font=('Arial', 12),
            bg=color,
            fg=self.colors['white']
        )
        title_label.pack(pady=(5, 20))
    
    def create_low_stock_section(self, container):
        """Create low stock products section"""
        
        # Section title
        section_title = tk.Label(
            container,
            text="⚠️ Low Stock Alert",
            font=('Arial', 16, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['danger']
        )
        section_title.pack(pady=(20, 10))
        
        # Frame for low stock table
        table_frame = tk.Frame(container, bg=self.colors['white'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 20))
        
        # Create treeview
        columns = ('ID', 'Name', 'Category', 'Stock', 'Limit')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        # Define headings
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Product Name')
        tree.heading('Category', text='Category')
        tree.heading('Stock', text='Current Stock')
        tree.heading('Limit', text='Low Stock Limit')
        
        # Define column widths
        tree.column('ID', width=50, anchor='center')
        tree.column('Name', width=250)
        tree.column('Category', width=150)
        tree.column('Stock', width=100, anchor='center')
        tree.column('Limit', width=120, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        # Pack tree and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Get low stock products
        low_stock_products = self.db.get_low_stock_products()
        
        # Insert data
        for product in low_stock_products:
            # product: (id, name, category, price, stock, low_stock_limit, created_at)
            
            # Add tag for color coding
            if product[4] == 0:
                tag = 'out_of_stock'
            elif product[4] <= product[5] / 2:
                tag = 'critical'
            else:
                tag = 'low'
            
            tree.insert('', tk.END, values=(
                product[0],  # ID
                product[1],  # Name
                product[2],  # Category
                product[4],  # Stock
                product[5]   # Low stock limit
            ), tags=(tag,))
        
        # Configure row colors
        tree.tag_configure('out_of_stock', background='#ffcccc')  # Red
        tree.tag_configure('critical', background='#ffe6cc')      # Orange
        tree.tag_configure('low', background='#fff3cd')           # Yellow
        
        # Add note
        note = tk.Label(
            container,
            text="💡 Tip: Restock these items soon to avoid running out!",
            font=('Arial', 10, 'italic'),
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        note.pack(pady=(0, 20))