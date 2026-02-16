"""
gui/scrollable_frame.py - Scrollable frame widget
Provides a frame that can scroll its contents
"""

import tkinter as tk
from tkinter import ttk


class ScrollableFrame(tk.Frame):
    """A frame with a scrollbar that can contain other widgets"""
    
    def __init__(self, parent, **kwargs):
        """
        Initialize the scrollable frame
        
        Args:
            parent: Parent widget
            **kwargs: Other arguments to pass to tk.Frame
        """
        super().__init__(parent, **kwargs)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self, highlightthickness=0, bg=kwargs.get('bg', 'white'))
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Create inner frame to hold content
        self.scrollable_frame = tk.Frame(self, bg=kwargs.get('bg', 'white'))
        
        # Configure canvas to scroll the inner frame
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Create window in canvas for the frame
        self.window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configure canvas scrolling
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mousewheel events for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)  # Linux scroll up
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)  # Linux scroll down
        
        # Layout canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind canvas resize to update window width
        self.canvas.bind("<Configure>", self._on_canvas_configure)
    
    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
    
    def _on_canvas_configure(self, event):
        """Update the scrollable frame width to match canvas width"""
        self.canvas.itemconfig(self.window, width=event.width)
