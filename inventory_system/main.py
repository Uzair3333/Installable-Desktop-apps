"""
main.py - Smart Inventory & Billing System
Main application entry point with GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from gui.dashboard import DashboardPage
from gui.products import ProductsPage
from gui.billing import BillingPage
from gui.reports import ReportsPage
from gui.invoices import InvoicesPage


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Inventory & Billing System")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Initialize database
        try:
            self.db = Database()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to database:\n{e}")
            self.root.destroy()
            return
        
        # Configure colors
        self.colors = {
            'primary': '#2E75B6',
            'secondary': '#4472C4',
            'sidebar': '#F0F0F0',
            'white': '#FFFFFF',
            'text': '#333333',
            'success': '#28A745',
            'danger': '#DC3545',
            'warning': '#FFC107'
        }
        
        # Configure root background
        self.root.configure(bg=self.colors['white'])
        
        # Create main container
        self.create_layout()
        
        # Show dashboard by default
        self.show_dashboard()
    
    def create_layout(self):
        """Create the main layout with sidebar and content area"""
        
        # Create sidebar frame
        self.sidebar = tk.Frame(
            self.root, 
            bg=self.colors['sidebar'], 
            width=200,
            relief=tk.RAISED,
            borderwidth=1
        )
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Create header in sidebar
        header = tk.Label(
            self.sidebar,
            text="INVENTORY\nSYSTEM",
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Arial', 14, 'bold'),
            pady=20
        )
        header.pack(fill=tk.X)
        
        # Create navigation buttons
        self.create_nav_buttons()
        
        # Create content frame
        self.content_frame = tk.Frame(self.root, bg=self.colors['white'])
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    def create_nav_buttons(self):
        """Create navigation buttons in sidebar"""
        
        buttons_config = [
            ("📊 Dashboard", self.show_dashboard),
            ("📦 Products", self.show_products),
            ("🧾 Create Bill", self.show_billing),
            ("📄 Invoices", self.show_invoices),
            ("📈 Reports", self.show_reports),
        ]
        
        self.nav_buttons = []
        
        for text, command in buttons_config:
            btn = tk.Button(
                self.sidebar,
                text=text,
                command=command,
                bg=self.colors['sidebar'],
                fg=self.colors['text'],
                font=('Arial', 11),
                relief=tk.FLAT,
                cursor='hand2',
                anchor='w',
                padx=20,
                pady=15
            )
            btn.pack(fill=tk.X, pady=2)
            self.nav_buttons.append(btn)
            
            # Bind hover effects
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=self.colors['primary'], fg=self.colors['white']))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(bg=self.colors['sidebar'], fg=self.colors['text']))
        
        # Add exit button at bottom
        exit_btn = tk.Button(
            self.sidebar,
            text="🚪 Exit",
            command=self.exit_app,
            bg=self.colors['danger'],
            fg=self.colors['white'],
            font=('Arial', 11, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            pady=15
        )
        exit_btn.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)
    
    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show dashboard page"""
        self.clear_content()
        DashboardPage(self.content_frame, self.db, self.colors)
    
    def show_products(self):
        """Show products page"""
        self.clear_content()
        ProductsPage(self.content_frame, self.db, self.colors)
    
    def show_billing(self):
        """Show billing page"""
        self.clear_content()
        BillingPage(self.content_frame, self.db, self.colors)
    
    def show_invoices(self):
        """Show invoices page"""
        self.clear_content()
        InvoicesPage(self.content_frame, self.db, self.colors)
    
    def show_reports(self):
        """Show reports page"""
        self.clear_content()
        ReportsPage(self.content_frame, self.db, self.colors)
    
    def exit_app(self):
        """Exit application"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.db.close()
            self.root.destroy()
    
    def on_closing(self):
        """Handle window closing event"""
        self.exit_app()


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = InventoryApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()