"""
billing_logic.py - Billing calculations for Smart Inventory & Billing System
Handles all billing calculations including discounts and totals
"""


class BillingEngine:
    """Handle all billing calculations"""
    
    @staticmethod
    def calculate_item_subtotal(price, quantity, discount=0):
        """
        Calculate subtotal for a single item
        
        Args:
            price (float): Unit price of the product
            quantity (int): Quantity of items
            discount (float): Discount amount (not percentage)
        
        Returns:
            float: Subtotal after discount
        """
        subtotal = (price * quantity) - discount
        return round(subtotal, 2)
    
    @staticmethod
    def calculate_total(cart_items):
        """
        Calculate total amount for all items in cart
        
        Args:
            cart_items (list): List of dicts with 'subtotal' key
        
        Returns:
            float: Total amount
        """
        total = sum(item['subtotal'] for item in cart_items)
        return round(total, 2)
    
    @staticmethod
    def validate_discount(price, quantity, discount):
        """
        Validate that discount doesn't exceed item subtotal
        
        Args:
            price (float): Unit price
            quantity (int): Quantity
            discount (float): Discount amount
        
        Returns:
            tuple: (is_valid, error_message)
        """
        subtotal = price * quantity
        
        if discount < 0:
            return False, "Discount cannot be negative"
        
        if discount > subtotal:
            return False, f"Discount cannot exceed subtotal (₹{subtotal})"
        
        return True, ""
    
    @staticmethod
    def validate_quantity(stock, quantity):
        """
        Validate that quantity doesn't exceed available stock
        
        Args:
            stock (int): Available stock
            quantity (int): Requested quantity
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if quantity <= 0:
            return False, "Quantity must be at least 1"
        
        if quantity > stock:
            return False, f"Insufficient stock. Only {stock} available"
        
        return True, ""
    
    @staticmethod
    def format_currency(amount):
        """
        Format amount as Indian currency
        
        Args:
            amount (float): Amount to format
        
        Returns:
            str: Formatted currency string (e.g., "₹1,234.56")
        """
        return f"₹{amount:,.2f}"
    
    @staticmethod
    def create_cart_item(product_id, product_name, price, quantity, discount=0):
        """
        Create a cart item dictionary
        
        Args:
            product_id (int): Product ID
            product_name (str): Product name
            price (float): Unit price
            quantity (int): Quantity
            discount (float): Discount amount
        
        Returns:
            dict: Cart item with all necessary fields
        """
        subtotal = BillingEngine.calculate_item_subtotal(price, quantity, discount)
        
        return {
            'product_id': product_id,
            'product_name': product_name,
            'price': price,
            'quantity': quantity,
            'discount': discount,
            'subtotal': subtotal
        }
    
    @staticmethod
    def get_invoice_summary(cart_items):
        """
        Get summary of invoice for display
        
        Args:
            cart_items (list): List of cart item dicts
        
        Returns:
            dict: Summary with items count, total discount, final amount
        """
        items_count = len(cart_items)
        total_discount = sum(item['discount'] for item in cart_items)
        subtotal_before_discount = sum(item['price'] * item['quantity'] for item in cart_items)
        final_amount = BillingEngine.calculate_total(cart_items)
        
        return {
            'items_count': items_count,
            'subtotal': round(subtotal_before_discount, 2),
            'total_discount': round(total_discount, 2),
            'final_amount': final_amount
        }