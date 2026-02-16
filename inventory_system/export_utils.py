"""
export_utils.py - Export utilities for Smart Inventory & Billing System
Handles exporting data to CSV, Excel, and TXT formats
"""

import pandas as pd
from datetime import datetime
import os


class ExportManager:
    """Handle all data export operations"""
    
    @staticmethod
    def export_products_to_csv(products, filename=None):
        """
        Export products to CSV file
        
        Args:
            products (list): List of product tuples from database
            filename (str): Output filename (optional)
        
        Returns:
            tuple: (success, message, filepath)
        """
        try:
            if not filename:
                filename = f"products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Convert to DataFrame
            df = pd.DataFrame(products, columns=[
                'ID', 'Name', 'Category', 'Price', 'Stock', 'Low Stock Limit', 'Created At'
            ])
            
            # Export to CSV
            df.to_csv(filename, index=False)
            return True, "Products exported successfully", filename
            
        except Exception as e:
            return False, f"Error exporting products: {e}", None
    
    @staticmethod
    def export_products_to_excel(products, filename=None):
        """
        Export products to Excel file
        
        Args:
            products (list): List of product tuples from database
            filename (str): Output filename (optional)
        
        Returns:
            tuple: (success, message, filepath)
        """
        try:
            if not filename:
                filename = f"products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            # Convert to DataFrame
            df = pd.DataFrame(products, columns=[
                'ID', 'Name', 'Category', 'Price', 'Stock', 'Low Stock Limit', 'Created At'
            ])
            
            # Export to Excel
            df.to_excel(filename, index=False, sheet_name='Products')
            return True, "Products exported successfully", filename
            
        except Exception as e:
            return False, f"Error exporting products: {e}", None
    
    @staticmethod
    def export_products_to_txt(products, filename=None):
        """
        Export products to TXT file
        
        Args:
            products (list): List of product tuples from database
            filename (str): Output filename (optional)
        
        Returns:
            tuple: (success, message, filepath)
        """
        try:
            if not filename:
                filename = f"products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                # Write header
                f.write("=" * 80 + "\n")
                f.write("PRODUCTS REPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                # Write column headers
                f.write(f"{'ID':<5} {'Name':<25} {'Category':<15} {'Price':<10} {'Stock':<8} {'Low Limit':<10}\n")
                f.write("-" * 80 + "\n")
                
                # Write data
                for product in products:
                    f.write(f"{product[0]:<5} {product[1]:<25} {product[2]:<15} "
                           f"₹{product[3]:<9.2f} {product[4]:<8} {product[5]:<10}\n")
                
                f.write("\n" + "=" * 80 + "\n")
                f.write(f"Total Products: {len(products)}\n")
            
            return True, "Products exported successfully", filename
            
        except Exception as e:
            return False, f"Error exporting products: {e}", None
    
    @staticmethod
    def export_invoices_to_csv(invoices, filename=None):
        """
        Export invoices to CSV file
        
        Args:
            invoices (list): List of invoice tuples from database
            filename (str): Output filename (optional)
        
        Returns:
            tuple: (success, message, filepath)
        """
        try:
            if not filename:
                filename = f"invoices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Convert to DataFrame
            df = pd.DataFrame(invoices, columns=[
                'ID', 'Invoice Number', 'Total Amount', 'Date'
            ])
            
            # Export to CSV
            df.to_csv(filename, index=False)
            return True, "Invoices exported successfully", filename
            
        except Exception as e:
            return False, f"Error exporting invoices: {e}", None
    
    @staticmethod
    def export_invoices_to_excel(invoices, filename=None):
        """
        Export invoices to Excel file
        
        Args:
            invoices (list): List of invoice tuples from database
            filename (str): Output filename (optional)
        
        Returns:
            tuple: (success, message, filepath)
        """
        try:
            if not filename:
                filename = f"invoices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            # Convert to DataFrame
            df = pd.DataFrame(invoices, columns=[
                'ID', 'Invoice Number', 'Total Amount', 'Date'
            ])
            
            # Export to Excel
            df.to_excel(filename, index=False, sheet_name='Invoices')
            return True, "Invoices exported successfully", filename
            
        except Exception as e:
            return False, f"Error exporting invoices: {e}", None
    
    @staticmethod
    def export_invoices_to_txt(invoices, filename=None):
        """
        Export invoices to TXT file
        
        Args:
            invoices (list): List of invoice tuples from database
            filename (str): Output filename (optional)
        
        Returns:
            tuple: (success, message, filepath)
        """
        try:
            if not filename:
                filename = f"invoices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                # Write header
                f.write("=" * 80 + "\n")
                f.write("INVOICES REPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                # Write column headers
                f.write(f"{'ID':<5} {'Invoice Number':<15} {'Total Amount':<15} {'Date':<20}\n")
                f.write("-" * 80 + "\n")
                
                # Calculate total
                total_amount = 0
                
                # Write data
                for invoice in invoices:
                    f.write(f"{invoice[0]:<5} {invoice[1]:<15} ₹{invoice[2]:<14.2f} {invoice[3]:<20}\n")
                    total_amount += invoice[2]
                
                f.write("\n" + "=" * 80 + "\n")
                f.write(f"Total Invoices: {len(invoices)}\n")
                f.write(f"Total Sales: ₹{total_amount:,.2f}\n")
            
            return True, "Invoices exported successfully", filename
            
        except Exception as e:
            return False, f"Error exporting invoices: {e}", None
    
    @staticmethod
    def export_sales_summary(invoices, filename=None):
        """
        Export sales summary report
        
        Args:
            invoices (list): List of invoice tuples from database
            filename (str): Output filename (optional)
        
        Returns:
            tuple: (success, message, filepath)
        """
        try:
            if not filename:
                filename = f"sales_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            # Calculate statistics
            total_invoices = len(invoices)
            total_sales = sum(invoice[2] for invoice in invoices)
            avg_sale = total_sales / total_invoices if total_invoices > 0 else 0
            
            with open(filename, 'w', encoding='utf-8') as f:
                # Write header
                f.write("=" * 80 + "\n")
                f.write("SALES SUMMARY REPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                # Write summary
                f.write("SUMMARY\n")
                f.write("-" * 40 + "\n")
                f.write(f"Total Invoices:        {total_invoices}\n")
                f.write(f"Total Sales:           ₹{total_sales:,.2f}\n")
                f.write(f"Average Sale:          ₹{avg_sale:,.2f}\n")
                
                if invoices:
                    f.write(f"Highest Sale:          ₹{max(invoice[2] for invoice in invoices):,.2f}\n")
                    f.write(f"Lowest Sale:           ₹{min(invoice[2] for invoice in invoices):,.2f}\n")
                
                f.write("\n" + "=" * 80 + "\n")
            
            return True, "Sales summary exported successfully", filename
            
        except Exception as e:
            return False, f"Error exporting sales summary: {e}", None
    
    @staticmethod
    def get_export_formats():
        """
        Get list of available export formats
        
        Returns:
            list: Available formats
        """
        return ['CSV', 'Excel', 'TXT']