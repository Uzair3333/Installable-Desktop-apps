"""
gui/reports.py - Reports and export page
View and export products, invoices, and sales data
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from export_utils import ExportManager
import os


class ReportsPage:
    def __init__(self, parent, db, colors):
        self.parent = parent
        self.db = db
        self.colors = colors
        self.export_manager = ExportManager()
        
        self.create_reports_page()
    
    def create_reports_page(self):
        """Create reports page layout"""
        
        # Title
        title = tk.Label(
            self.parent,
            text="Reports & Export",
            font=('Arial', 24, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        title.pack(pady=20)
        
        # Main container
        main_container = tk.Frame(self.parent, bg=self.colors['white'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Create sections
        self.create_products_section(main_container)
        self.create_invoices_section(main_container)
        self.create_sales_summary_section(main_container)
    
    def create_products_section(self, parent):
        """Create products export section"""
        
        section = tk.LabelFrame(
            parent,
            text="Export Products",
            font=('Arial', 14, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary'],
            relief=tk.RIDGE,
            borderwidth=2
        )
        section.pack(fill=tk.X, pady=10)
        
        # Info
        info = tk.Label(
            section,
            text="Export all products data to your preferred format",
            font=('Arial', 10),
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        info.pack(pady=10)
        
        # Buttons frame
        btn_frame = tk.Frame(section, bg=self.colors['white'])
        btn_frame.pack(pady=10)
        
        # CSV button
        csv_btn = tk.Button(
            btn_frame,
            text="Export to CSV",
            command=lambda: self.export_products('csv'),
            bg=self.colors['success'],
            fg=self.colors['white'],
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            width=15,
            pady=10
        )
        csv_btn.pack(side=tk.LEFT, padx=10)
        
        # Excel button
        excel_btn = tk.Button(
            btn_frame,
            text="Export to Excel",
            command=lambda: self.export_products('excel'),
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            width=15,
            pady=10
        )
        excel_btn.pack(side=tk.LEFT, padx=10)
        
        # TXT button
        txt_btn = tk.Button(
            btn_frame,
            text="Export to TXT",
            command=lambda: self.export_products('txt'),
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            width=15,
            pady=10
        )
        txt_btn.pack(side=tk.LEFT, padx=10)
    
    def create_invoices_section(self, parent):
        """Create invoices export section"""
        
        section = tk.LabelFrame(
            parent,
            text="Export Invoices",
            font=('Arial', 14, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary'],
            relief=tk.RIDGE,
            borderwidth=2
        )
        section.pack(fill=tk.X, pady=10)
        
        # Info
        info = tk.Label(
            section,
            text="Export all invoices data to your preferred format",
            font=('Arial', 10),
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        info.pack(pady=10)
        
        # Buttons frame
        btn_frame = tk.Frame(section, bg=self.colors['white'])
        btn_frame.pack(pady=10)
        
        # CSV button
        csv_btn = tk.Button(
            btn_frame,
            text="Export to CSV",
            command=lambda: self.export_invoices('csv'),
            bg=self.colors['success'],
            fg=self.colors['white'],
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            width=15,
            pady=10
        )
        csv_btn.pack(side=tk.LEFT, padx=10)
        # Bind Enter key
        csv_btn.bind('<Return>', lambda e: self.export_products('csv'))
        
        # Excel button
        excel_btn = tk.Button(
            btn_frame,
            text="Export to Excel",
            command=lambda: self.export_invoices('excel'),
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            width=15,
            pady=10
        )
        excel_btn.pack(side=tk.LEFT, padx=10)
        # Bind Enter key
        excel_btn.bind('<Return>', lambda e: self.export_invoices('excel'))
        
        # TXT button
        txt_btn = tk.Button(
            btn_frame,
            text="Export to TXT",
            command=lambda: self.export_invoices('txt'),
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            width=15,
            pady=10
        )
        txt_btn.pack(side=tk.LEFT, padx=10)
        # Blind Enter Key
        txt_btn.bind('<Return>', lambda e: self.export_invoices('txt'))
    
    def create_sales_summary_section(self, parent):
        """Create sales summary section"""
        
        section = tk.LabelFrame(
            parent,
            text="Sales Summary",
            font=('Arial', 14, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary'],
            relief=tk.RIDGE,
            borderwidth=2
        )
        section.pack(fill=tk.X, pady=10)
        
        # Info
        info = tk.Label(
            section,
            text="Generate detailed sales summary report",
            font=('Arial', 10),
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        info.pack(pady=10)
        
        # Button
        summary_btn = tk.Button(
            section,
            text="Generate Sales Summary",
            command=self.export_sales_summary,
            bg=self.colors['warning'],
            fg=self.colors['text'],
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            width=25,
            pady=10
        )
        summary_btn.pack(pady=10)
        
        # Statistics frame
        stats_frame = tk.Frame(section, bg=self.colors['sidebar'], relief=tk.SUNKEN, borderwidth=2)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Get current statistics
        total_products = self.db.get_total_products()
        total_invoices = self.db.get_total_invoices()
        today_sales = self.db.get_today_sales()
        
        # Display statistics
        stats_title = tk.Label(
            stats_frame,
            text="Quick Statistics",
            font=('Arial', 12, 'bold'),
            bg=self.colors['sidebar'],
            fg=self.colors['primary']
        )
        stats_title.pack(pady=10)
        
        stats_text = f"""
        Total Products in Database: {total_products}
        Total Invoices Generated: {total_invoices}
        Today's Sales: ₹{today_sales:,.2f}
        """
        
        stats_label = tk.Label(
            stats_frame,
            text=stats_text,
            font=('Arial', 11),
            bg=self.colors['sidebar'],
            justify=tk.LEFT
        )
        stats_label.pack(pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            section,
            text="🔄 Refresh Statistics",
            command=self.refresh_stats,
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            width=20
        )
        refresh_btn.pack(pady=10)
    
    def export_products(self, format_type):
        """Export products to specified format"""
        
        # Get products from database
        products = self.db.get_all_products()
        
        if not products:
            messagebox.showinfo("Info", "No products to export")
            return
        
        # Ask for save location
        if format_type == 'csv':
            filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
            default_ext = ".csv"
        elif format_type == 'excel':
            filetypes = [("Excel files", "*.xlsx"), ("All files", "*.*")]
            default_ext = ".xlsx"
        else:  # txt
            filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
            default_ext = ".txt"
        
        filename = filedialog.asksaveasfilename(
            title="Save Products Export",
            defaultextension=default_ext,
            filetypes=filetypes
        )
        
        if not filename:
            return
        
        # Export based on format
        if format_type == 'csv':
            success, message, filepath = self.export_manager.export_products_to_csv(products, filename)
        elif format_type == 'excel':
            success, message, filepath = self.export_manager.export_products_to_excel(products, filename)
        else:  # txt
            success, message, filepath = self.export_manager.export_products_to_txt(products, filename)
        
        # Show result
        if success:
            result = messagebox.askyesno(
                "Success",
                f"{message}\n\nFile saved: {filepath}\n\nDo you want to open the file location?"
            )
            if result:
                self.open_file_location(filepath)
        else:
            messagebox.showerror("Error", message)
    
    def export_invoices(self, format_type):
        """Export invoices to specified format"""
        
        # Get invoices from database
        invoices = self.db.get_all_invoices()
        
        if not invoices:
            messagebox.showinfo("Info", "No invoices to export")
            return
        
        # Ask for save location
        if format_type == 'csv':
            filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
            default_ext = ".csv"
        elif format_type == 'excel':
            filetypes = [("Excel files", "*.xlsx"), ("All files", "*.*")]
            default_ext = ".xlsx"
        else:  # txt
            filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
            default_ext = ".txt"
        
        filename = filedialog.asksaveasfilename(
            title="Save Invoices Export",
            defaultextension=default_ext,
            filetypes=filetypes
        )
        
        if not filename:
            return
        
        # Export based on format
        if format_type == 'csv':
            success, message, filepath = self.export_manager.export_invoices_to_csv(invoices, filename)
        elif format_type == 'excel':
            success, message, filepath = self.export_manager.export_invoices_to_excel(invoices, filename)
        else:  # txt
            success, message, filepath = self.export_manager.export_invoices_to_txt(invoices, filename)
        
        # Show result
        if success:
            result = messagebox.askyesno(
                "Success",
                f"{message}\n\nFile saved: {filepath}\n\nDo you want to open the file location?"
            )
            if result:
                self.open_file_location(filepath)
        else:
            messagebox.showerror("Error", message)
    
    def export_sales_summary(self):
        """Export sales summary report"""
        
        # Get invoices for summary
        invoices = self.db.get_all_invoices()
        
        if not invoices:
            messagebox.showinfo("Info", "No sales data available")
            return
        
        # Ask for save location
        filename = filedialog.asksaveasfilename(
            title="Save Sales Summary",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        # Generate summary
        success, message, filepath = self.export_manager.export_sales_summary(invoices, filename)
        
        # Show result
        if success:
            result = messagebox.askyesno(
                "Success",
                f"{message}\n\nFile saved: {filepath}\n\nDo you want to open the file location?"
            )
            if result:
                self.open_file_location(filepath)
        else:
            messagebox.showerror("Error", message)
    
    def open_file_location(self, filepath):
        """Open file location in file explorer"""
        try:
            folder_path = os.path.dirname(os.path.abspath(filepath))
            
            # Open folder based on OS
            import platform
            if platform.system() == 'Windows':
                os.startfile(folder_path)
            elif platform.system() == 'Darwin':  # macOS
                os.system(f'open "{folder_path}"')
            else:  # Linux
                os.system(f'xdg-open "{folder_path}"')
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file location:\n{e}")
    
    def refresh_stats(self):
        """Refresh statistics display"""
        # Recreate the reports page to refresh stats
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        self.create_reports_page()
        messagebox.showinfo("Success", "Statistics refreshed!")