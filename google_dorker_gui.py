#!/usr/bin/env python3
"""
Google Dorker GUI - Hacker Terminal Interface
============================================

A GUI version of Google Dorker with classic hacker aesthetic:
- Green text on black background
- Falling code animation
- Terminal-style interface
- Matrix-style visual effects

Author: Security Researcher
Version: 1.0
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import random
import string
import json
from google_dorker import GoogleDorker, DorkCategory
import urllib.parse

class MatrixRain:
    """Matrix-style falling code animation"""
    
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.drops = []
        self.chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
        self.init_drops()
    
    def init_drops(self):
        """Initialize falling drops"""
        font_size = 12
        columns = self.width // font_size
        for i in range(columns):
            self.drops.append({
                'x': i * font_size,
                'y': random.randint(-self.height, 0),
                'speed': random.uniform(1, 3),
                'chars': []
            })
    
    def update(self):
        """Update animation frame"""
        self.canvas.delete("matrix")
        
        for drop in self.drops:
            # Add new character
            if len(drop['chars']) < 20:
                drop['chars'].append(random.choice(self.chars))
            
            # Remove old characters
            if len(drop['chars']) > 15:
                drop['chars'].pop(0)
            
            # Draw characters
            for i, char in enumerate(drop['chars']):
                y = drop['y'] + (i * 20)
                if 0 <= y <= self.height:
                    color = "#00ff00" if i == len(drop['chars']) - 1 else "#004400"
                    self.canvas.create_text(
                        drop['x'], y, 
                        text=char, 
                        fill=color, 
                        font=("Courier", 10),
                        tags="matrix"
                    )
            
            # Move drop
            drop['y'] += drop['speed']
            if drop['y'] > self.height:
                drop['y'] = random.randint(-200, 0)
                drop['chars'] = []

class HackerTerminal:
    """Main GUI class with hacker aesthetic"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Google Dorker - Hacker Terminal")
        self.root.configure(bg='black')
        self.root.geometry("1200x800")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Initialize Google Dorker
        self.dorker = GoogleDorker()
        self.current_queries = []
        
        # Animation control
        self.animation_running = False
        self.animation_thread = None
        
        self.create_widgets()
        self.start_animation()
        
    def configure_styles(self):
        """Configure hacker-style colors"""
        self.style.configure('Hacker.TFrame', background='black')
        self.style.configure('Hacker.TLabel', 
                           background='black', 
                           foreground='#00ff00',
                           font=('Courier', 10))
        self.style.configure('Hacker.TButton',
                           background='black',
                           foreground='#00ff00',
                           font=('Courier', 9),
                           borderwidth=1,
                           relief='solid')
        self.style.configure('Hacker.TEntry',
                           background='black',
                           foreground='#00ff00',
                           font=('Courier', 10),
                           borderwidth=1,
                           relief='solid')
        self.style.configure('Hacker.TCombobox',
                           background='black',
                           foreground='#00ff00',
                           font=('Courier', 10))
    
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Hacker.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="GOOGLE DORKER - HACKER TERMINAL",
                               style='Hacker.TLabel',
                               font=('Courier', 16, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(main_frame,
                                  text="Advanced Reconnaissance Tool - Authorized Use Only",
                                  style='Hacker.TLabel',
                                  font=('Courier', 8))
        subtitle_label.pack(pady=(0, 20))
        
        # Control panel
        self.create_control_panel(main_frame)
        
        # Results area
        self.create_results_area(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
        
        # Matrix animation canvas
        self.create_matrix_canvas(main_frame)
    
    def create_control_panel(self, parent):
        """Create the control panel"""
        control_frame = ttk.Frame(parent, style='Hacker.TFrame')
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Target input
        target_frame = ttk.Frame(control_frame, style='Hacker.TFrame')
        target_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(target_frame, text="TARGET:", style='Hacker.TLabel').pack(side=tk.LEFT)
        self.target_entry = ttk.Entry(target_frame, style='Hacker.TEntry', width=30)
        self.target_entry.pack(side=tk.LEFT, padx=(10, 0))
        self.target_entry.insert(0, "example.com")
        
        # Category selection
        category_frame = ttk.Frame(control_frame, style='Hacker.TFrame')
        category_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(category_frame, text="CATEGORY:", style='Hacker.TLabel').pack(side=tk.LEFT)
        self.category_var = tk.StringVar(value="all")
        self.category_combo = ttk.Combobox(category_frame, 
                                          textvariable=self.category_var,
                                          style='Hacker.TCombobox',
                                          width=20,
                                          state='readonly')
        self.category_combo['values'] = ['all'] + [cat.value for cat in DorkCategory]
        self.category_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # Query count
        count_frame = ttk.Frame(control_frame, style='Hacker.TFrame')
        count_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(count_frame, text="COUNT:", style='Hacker.TLabel').pack(side=tk.LEFT)
        self.count_var = tk.StringVar(value="10")
        self.count_entry = ttk.Entry(count_frame, style='Hacker.TEntry', width=10)
        self.count_entry.pack(side=tk.LEFT, padx=(10, 0))
        self.count_entry.insert(0, "10")
        
        # Buttons
        button_frame = ttk.Frame(control_frame, style='Hacker.TFrame')
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.generate_btn = ttk.Button(button_frame, 
                                      text="GENERATE DORKS",
                                      style='Hacker.TButton',
                                      command=self.generate_dorks)
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(button_frame,
                                   text="CLEAR",
                                   style='Hacker.TButton',
                                   command=self.clear_results)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_btn = ttk.Button(button_frame,
                                  text="SAVE RESULTS",
                                  style='Hacker.TButton',
                                  command=self.save_results)
        self.save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.advanced_btn = ttk.Button(button_frame,
                                      text="ADVANCED",
                                      style='Hacker.TButton',
                                      command=self.show_advanced)
        self.advanced_btn.pack(side=tk.LEFT)
    
    def create_results_area(self, parent):
        """Create the results display area"""
        results_frame = ttk.Frame(parent, style='Hacker.TFrame')
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            bg='black',
            fg='#00ff00',
            font=('Courier', 9),
            insertbackground='#00ff00',
            selectbackground='#004400',
            selectforeground='#00ff00',
            wrap=tk.WORD,
            height=20
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for syntax highlighting
        self.results_text.tag_configure("header", foreground="#00ff00", font=('Courier', 10, 'bold'))
        self.results_text.tag_configure("query", foreground="#ffffff", font=('Courier', 9))
        self.results_text.tag_configure("description", foreground="#00aa00", font=('Courier', 8))
        self.results_text.tag_configure("risk_critical", foreground="#ff0000", font=('Courier', 8, 'bold'))
        self.results_text.tag_configure("risk_high", foreground="#ff8800", font=('Courier', 8, 'bold'))
        self.results_text.tag_configure("risk_medium", foreground="#ffff00", font=('Courier', 8, 'bold'))
        self.results_text.tag_configure("risk_low", foreground="#00ff00", font=('Courier', 8, 'bold'))
        self.results_text.tag_configure("url", foreground="#0088ff", font=('Courier', 8))
        self.results_text.tag_configure("separator", foreground="#444444", font=('Courier', 8))
    
    def create_status_bar(self, parent):
        """Create the status bar"""
        self.status_frame = ttk.Frame(parent, style='Hacker.TFrame')
        self.status_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.status_label = ttk.Label(self.status_frame, 
                                     text="READY - Enter target and generate dorks",
                                     style='Hacker.TLabel')
        self.status_label.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.status_frame, 
                                       mode='indeterminate',
                                       length=200)
        self.progress.pack(side=tk.RIGHT)
    
    def create_matrix_canvas(self, parent):
        """Create the matrix animation canvas"""
        self.matrix_canvas = tk.Canvas(parent, 
                                      bg='black', 
                                      height=100,
                                      highlightthickness=0)
        self.matrix_canvas.pack(fill=tk.X, pady=(5, 0))
        self.matrix_rain = MatrixRain(self.matrix_canvas, 1200, 100)
    
    def start_animation(self):
        """Start the matrix animation"""
        self.animation_running = True
        self.animation_thread = threading.Thread(target=self.animate, daemon=True)
        self.animation_thread.start()
    
    def animate(self):
        """Animation loop"""
        while self.animation_running:
            try:
                self.matrix_rain.update()
                time.sleep(0.1)
            except:
                break
    
    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def generate_dorks(self):
        """Generate dork queries"""
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Please enter a target domain")
            return
        
        # Get category
        category_str = self.category_var.get()
        category = None
        if category_str != "all":
            try:
                category = DorkCategory(category_str)
            except ValueError:
                messagebox.showerror("Error", f"Invalid category: {category_str}")
                return
        
        # Get count
        try:
            count = int(self.count_entry.get())
        except ValueError:
            count = 10
        
        # Start generation in thread
        self.generate_btn.config(state='disabled')
        self.progress.start()
        self.update_status("GENERATING DORKS...")
        
        thread = threading.Thread(target=self._generate_dorks_thread, 
                                 args=(target, category, count), daemon=True)
        thread.start()
    
    def _generate_dorks_thread(self, target, category, count):
        """Generate dorks in background thread"""
        try:
            # Generate queries
            if category:
                queries = self.dorker.generate_dork_queries(target, category, count)
            else:
                queries = self.dorker.generate_dork_queries(target, count=count)
            
            self.current_queries = queries
            
            # Update UI in main thread
            self.root.after(0, self._display_results, queries)
            
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
    
    def _display_results(self, queries):
        """Display results in the text area"""
        self.results_text.delete(1.0, tk.END)
        
        # Add header
        self.results_text.insert(tk.END, "GOOGLE DORKER RESULTS\n", "header")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n", "separator")
        
        # Add ethical warning
        self.results_text.insert(tk.END, "WARNING: Authorized use only!\n", "risk_critical")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n", "separator")
        
        # Add queries
        for i, dork in enumerate(queries, 1):
            # Header
            self.results_text.insert(tk.END, f"[{i}] {dork.category.value.upper()}\n", "header")
            
            # Query
            self.results_text.insert(tk.END, f"Query: {dork.query}\n", "query")
            
            # Description
            self.results_text.insert(tk.END, f"Description: {dork.description}\n", "description")
            
            # Risk level
            risk_tag = f"risk_{dork.risk_level.lower()}"
            self.results_text.insert(tk.END, f"Risk Level: {dork.risk_level}\n", risk_tag)
            
            # Use case
            self.results_text.insert(tk.END, f"Use Case: {dork.use_case}\n", "description")
            
            # Google URL
            google_url = f"https://www.google.com/search?q={urllib.parse.quote(dork.query)}"
            self.results_text.insert(tk.END, f"Google URL: {google_url}\n", "url")
            
            # Separator
            self.results_text.insert(tk.END, "-" * 80 + "\n", "separator")
        
        # Update status
        self.update_status(f"GENERATED {len(queries)} DORK QUERIES")
        
        # Re-enable button
        self.generate_btn.config(state='normal')
        self.progress.stop()
    
    def _show_error(self, error_msg):
        """Show error message"""
        self.update_status(f"ERROR: {error_msg}")
        self.generate_btn.config(state='normal')
        self.progress.stop()
        messagebox.showerror("Error", error_msg)
    
    def clear_results(self):
        """Clear results area"""
        self.results_text.delete(1.0, tk.END)
        self.current_queries = []
        self.update_status("RESULTS CLEARED")
    
    def save_results(self):
        """Save results to file"""
        if not self.current_queries:
            messagebox.showwarning("Warning", "No results to save")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.dorker.save_queries(self.current_queries, filename)
                self.update_status(f"RESULTS SAVED TO {filename}")
                messagebox.showinfo("Success", f"Results saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {e}")
    
    def show_advanced(self):
        """Show advanced options dialog"""
        dialog = AdvancedDialog(self.root, self.dorker)
        self.root.wait_window(dialog.dialog)
    
    def on_closing(self):
        """Handle window closing"""
        self.animation_running = False
        self.root.destroy()

class AdvancedDialog:
    """Advanced options dialog"""
    
    def __init__(self, parent, dorker):
        self.dorker = dorker
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Advanced Options")
        self.dialog.configure(bg='black')
        self.dialog.geometry("600x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Title
        title_label = tk.Label(self.dialog, 
                              text="ADVANCED DORK GENERATION",
                              bg='black',
                              fg='#00ff00',
                              font=('Courier', 14, 'bold'))
        title_label.pack(pady=20)
        
        # Target input
        target_frame = tk.Frame(self.dialog, bg='black')
        target_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(target_frame, text="Target:", bg='black', fg='#00ff00', font=('Courier', 10)).pack(side=tk.LEFT)
        self.target_entry = tk.Entry(target_frame, bg='black', fg='#00ff00', font=('Courier', 10))
        self.target_entry.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        self.target_entry.insert(0, "example.com")
        
        # Keywords input
        keywords_frame = tk.Frame(self.dialog, bg='black')
        keywords_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(keywords_frame, text="Keywords:", bg='black', fg='#00ff00', font=('Courier', 10)).pack(side=tk.LEFT)
        self.keywords_entry = tk.Entry(keywords_frame, bg='black', fg='#00ff00', font=('Courier', 10))
        self.keywords_entry.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        self.keywords_entry.insert(0, "admin,login,config,password")
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg='black')
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Button(button_frame, text="GENERATE ADVANCED", 
                 bg='black', fg='#00ff00', font=('Courier', 10),
                 command=self.generate_advanced).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="GENERATE OSINT", 
                 bg='black', fg='#00ff00', font=('Courier', 10),
                 command=self.generate_osint).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="CLOSE", 
                 bg='black', fg='#00ff00', font=('Courier', 10),
                 command=self.dialog.destroy).pack(side=tk.RIGHT)
        
        # Results area
        self.results_text = scrolledtext.ScrolledText(
            self.dialog,
            bg='black',
            fg='#00ff00',
            font=('Courier', 9),
            height=15
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
    
    def generate_advanced(self):
        """Generate advanced queries"""
        target = self.target_entry.get().strip()
        keywords_str = self.keywords_entry.get().strip()
        
        if not target:
            messagebox.showerror("Error", "Please enter a target")
            return
        
        keywords = [k.strip() for k in keywords_str.split(",")] if keywords_str else None
        
        try:
            queries = self.dorker.generate_advanced_queries(target, keywords)
            self.display_queries(queries, "ADVANCED QUERIES")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def generate_osint(self):
        """Generate OSINT queries"""
        target = self.target_entry.get().strip()
        
        if not target:
            messagebox.showerror("Error", "Please enter a target")
            return
        
        try:
            queries = self.dorker.generate_osint_queries(target)
            self.display_queries(queries, "OSINT QUERIES")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def display_queries(self, queries, title):
        """Display queries in results area"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"{title}\n", "header")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        
        for i, dork in enumerate(queries, 1):
            self.results_text.insert(tk.END, f"[{i}] {dork.query}\n")
            self.results_text.insert(tk.END, f"    {dork.description}\n")
            self.results_text.insert(tk.END, f"    Risk: {dork.risk_level}\n\n")

def main():
    """Main function"""
    app = HackerTerminal()
    app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.root.mainloop()

if __name__ == "__main__":
    main()
