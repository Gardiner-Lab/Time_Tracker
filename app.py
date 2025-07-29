import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from tkinter import font
import tkinter.font as tkfont
import requests
import threading
import time
import csv
import os
import shutil
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

BASE_URL = "http://localhost:5000"

class TimeTrackerApp:
    def __init__(self, root):
        # Configure styles
        self.style = ttk.Style()
        
        # Apply modern theme
        self.style.theme_use("clam")
        
        # Configure colors
        self.bg_color = "#2d2d30"
        self.fg_color = "#e1e1e1"
        self.accent_color = "#007acc"
        self.secondary_color = "#3e3e42"
        self.header_color = "#252526"
        
        # Configure root window
        root.configure(bg=self.bg_color)

        # Create menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Export CSV", command=self.export_csv)
        self.file_menu.add_command(label="Backup Database", command=self.backup_database)
        self.file_menu.add_command(label="Restore Database", command=self.restore_database)
        
        # Academic periods menu
        self.period_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Period Manager", menu=self.period_menu)
        self.period_menu.add_command(label="Manage Periods", command=self.manage_periods)
        
        # Configure global styles
        self.style.configure(".", 
                            background=self.bg_color,
                            foreground=self.fg_color,
                            font=("Segoe UI", 10))
        
        # Configure specific elements
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        self.style.configure("TLabelframe", background=self.bg_color, relief="flat")
        self.style.configure("TLabelframe.Label", background=self.header_color, foreground=self.fg_color)
        
        # Configure Treeview
        self.style.configure("Treeview", 
                            background=self.secondary_color,
                            fieldbackground=self.secondary_color,
                            foreground=self.fg_color,
                            rowheight=30)
        
        self.style.configure("Treeview.Heading", 
                            background=self.header_color,
                            foreground=self.fg_color,
                            font=("Segoe UI", 10, "bold"),
                            relief="flat")
        
        self.style.map("Treeview", 
                      background=[("selected", self.accent_color)],
                      foreground=[("selected", "white")])
        
        # Configure buttons
        self.style.configure("TButton",
                            background=self.secondary_color,
                            foreground=self.fg_color,
                            font=("Segoe UI", 10),
                            borderwidth=1)
        
        self.style.map("TButton",
                      background=[("active", self.accent_color), ("disabled", self.bg_color)])
        
        self.style.configure("Big.TButton", 
                           font=("Segoe UI", 12, "bold"), 
                           padding=15,
                           background=self.accent_color,
                           foreground="white")
        
        self.root = root
        self.root.title("Task Time Tracker")
        self.root.geometry("1000x800")  # Set initial window size
        self.current_timer_id = None
        self.running = False
        
        # Create main container
        main_container = ttk.Frame(root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create paned window for resizable panels
        paned_window = ttk.PanedWindow(main_container, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Left panel for groups and tasks
        left_panel = ttk.Frame(paned_window)
        paned_window.add(left_panel, weight=1)
        
        # Right panel for timer and history
        right_panel = ttk.Frame(paned_window)
        paned_window.add(right_panel, weight=1)
        
        # Configure fonts
        timer_font = ("Segoe UI", 28, "bold")
        heading_font = ("Segoe UI", 11, "bold")
        
        # Group controls
        self.group_frame = ttk.LabelFrame(left_panel, text="Task Groups", style="TLabelframe")
        self.group_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.task_frame = ttk.LabelFrame(left_panel, text="Tasks", style="TLabelframe")
        self.task_frame.pack(padx=5, pady=5, fill="both", expand=True)
        
        self.timer_frame = ttk.LabelFrame(right_panel, text="Timer", style="TLabelframe")
        self.timer_frame.pack(padx=5, pady=5, fill="x")
        
        # Group controls
        group_btn_frame = ttk.Frame(self.group_frame)
        group_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(group_btn_frame, text="Add Group", command=self.add_group).pack(side=tk.LEFT)
        
        # Add scrollbar for group tree
        group_scroll = ttk.Scrollbar(self.group_frame)
        group_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.group_tree = ttk.Treeview(self.group_frame, columns=("id",), show="tree", height=5,
                                      yscrollcommand=group_scroll.set)
        self.group_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        group_scroll.config(command=self.group_tree.yview)
        self.group_tree.heading("#0", text="Group Name")
        self.group_tree.bind("<<TreeviewSelect>>", self.load_tasks)
        self.group_tree.bind("<Button-3>", self.show_group_context_menu)
        
        # Task controls
        task_btn_frame = ttk.Frame(self.task_frame)
        task_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(task_btn_frame, text="Add Task", command=self.add_task).pack(side=tk.LEFT)
        ttk.Button(task_btn_frame, text="Refresh", command=self.load_tasks).pack(side=tk.LEFT, padx=5)
        
        # Add scrollbars for task tree
        task_scroll_y = ttk.Scrollbar(self.task_frame)
        task_scroll_x = ttk.Scrollbar(self.task_frame, orient=tk.HORIZONTAL)
        task_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        task_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.task_list = ttk.Treeview(self.task_frame, 
                                     columns=("id", "name", "total_hours", "hours_per_week"), 
                                     show="headings", height=10,
                                     yscrollcommand=task_scroll_y.set,
                                     xscrollcommand=task_scroll_x.set)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        task_scroll_y.config(command=self.task_list.yview)
        task_scroll_x.config(command=self.task_list.xview)
        
        self.task_list.heading("id", text="ID")
        self.task_list.heading("name", text="Task Name")
        self.task_list.heading("total_hours", text="Total Hours")
        self.task_list.heading("hours_per_week", text="Hours/Week")
        self.task_list.column("id", width=50, anchor=tk.CENTER)
        self.task_list.column("name", width=150)
        self.task_list.column("total_hours", width=100, anchor=tk.CENTER)
        self.task_list.column("hours_per_week", width=100, anchor=tk.CENTER)
        self.task_list.bind("<<TreeviewSelect>>", self.load_history)
        self.task_list.bind("<Button-3>", self.show_task_context_menu)
        
        # Timer controls
        self.timer_label = ttk.Label(
            self.timer_frame, 
            text="00:00:00", 
            font=timer_font,
            foreground=self.accent_color
        )
        self.timer_label.pack(pady=20)
        
        # Create a frame for buttons to center them
        button_frame = ttk.Frame(self.timer_frame)
        button_frame.pack(pady=10)
        
        self.start_btn = ttk.Button(
            button_frame, 
            text="START", 
            command=self.start_timer, 
            style="Big.TButton"
        )
        self.start_btn.pack(side="left", padx=40)
        
        self.stop_btn = ttk.Button(
            button_frame, 
            text="STOP", 
            command=self.stop_timer, 
            state="disabled", 
            style="Big.TButton"
        )
        self.stop_btn.pack(side="left", padx=40)
        
        # History display
        self.history_frame = ttk.LabelFrame(right_panel, text="Time Entries")
        self.history_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbars for history tree
        hist_scroll_y = ttk.Scrollbar(self.history_frame)
        hist_scroll_x = ttk.Scrollbar(self.history_frame, orient=tk.HORIZONTAL)
        hist_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        hist_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.history_tree = ttk.Treeview(self.history_frame, 
                                        columns=("id", "date", "duration", "note"),
                                        show="headings", 
                                        height=5,
                                        yscrollcommand=hist_scroll_y.set,
                                        xscrollcommand=hist_scroll_x.set)
        self.history_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        hist_scroll_y.config(command=self.history_tree.yview)
        hist_scroll_x.config(command=self.history_tree.xview)
        
        self.history_tree.heading("id", text="ID")
        self.history_tree.heading("date", text="Date")
        self.history_tree.heading("duration", text="Duration")
        self.history_tree.heading("note", text="Note")
        
        self.history_tree.column("id", width=0, stretch=tk.NO, minwidth=0)
        self.history_tree.column("date", width=100, anchor=tk.CENTER)
        self.history_tree.column("duration", width=100, anchor=tk.CENTER)
        self.history_tree.column("note", width=400)
        self.history_tree.bind("<Button-3>", self.show_history_context_menu)
        
        # Visualization controls
        self.vis_frame = ttk.LabelFrame(right_panel, text="Time Distribution", style="TLabelframe")
        self.vis_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Mode selector
        vis_control_frame = ttk.Frame(self.vis_frame)
        vis_control_frame.pack(fill=tk.X, padx=5, pady=5)

        # Period selector
        ttk.Label(vis_control_frame, text="Period:").pack(side=tk.LEFT, padx=(10, 5))
        
        self.period_var = tk.StringVar()
        self.period_combo = ttk.Combobox(vis_control_frame, 
                                        textvariable=self.period_var,
                                        state="readonly",
                                        width=15)
        self.period_combo.pack(side=tk.LEFT, padx=5)
        self.period_combo.bind("<<ComboboxSelected>>", self.update_visualization)
        
        self.periods = {}  # Will store period id: name mapping
        
        ttk.Label(vis_control_frame, text="View by:").pack(side=tk.LEFT, padx=5)
        
        self.vis_mode = tk.StringVar(value="group")
        ttk.Radiobutton(
            vis_control_frame, text="Group", 
            variable=self.vis_mode, value="group",
            command=self.update_visualization
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            vis_control_frame, text="Task", 
            variable=self.vis_mode, value="task",
            command=self.update_visualization
        ).pack(side=tk.LEFT, padx=5)
        
        # Chart canvas
        self.chart_frame = ttk.Frame(self.vis_frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initialize visualization
        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor=self.secondary_color)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(self.secondary_color)
        self.chart_canvas = FigureCanvasTkAgg(self.fig, self.chart_frame)
        self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Set text colors to match theme
        self.ax.title.set_color(self.fg_color)
        for text in self.ax.get_xticklabels() + self.ax.get_yticklabels():
            text.set_color(self.fg_color)
        
        # Initial update
        self.update_visualization()
        
        self.load_groups()
        
        # Bind spacebar to toggle timer
        self.root.bind("<space>", self.toggle_timer)
    
    def add_group(self):
        name = simpledialog.askstring("New Group", "Enter group name:")
        if name:
            threading.Thread(target=lambda: requests.post(f"{BASE_URL}/groups", json={"name": name})).start()
            self.load_groups()
            self.load_tasks()
    
    def add_task(self):
        group = self.get_selected_group()
        if not group: return
        
        name = simpledialog.askstring("New Task", "Enter task name:")
        if name:
            try:
                response = requests.post(
                    f"{BASE_URL}/tasks", 
                    json={"name": name, "group_id": group["id"]}
                )
                response.raise_for_status()
                self.load_tasks()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add task: {str(e)}")
    
    def start_timer(self):
        task = self.get_selected_task()
        if not task: return
        
        response = requests.post(f"{BASE_URL}/timer/start", json={"task_id": task["id"]})
        if response.status_code == 200:
            self.current_timer_id = response.json()["id"]
            self.running = True
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            self.start_time = time.time()
            self.update_timer()
    
    def stop_timer(self):
        if not self.running: return
        
        note = simpledialog.askstring("Session Note", 
                                    "What did you work on?",
                                    parent=self.root)
        
        requests.post(f"{BASE_URL}/timer/stop", 
                    json={"id": self.current_timer_id, "note": note or ""})
        
        self.running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.timer_label.config(text="00:00:00")
        
        # Refresh data with a small delay
        self.root.after(500, lambda: [
            self.load_history(),
            self.update_visualization(),
            self.load_tasks()
        ])
    
    def update_timer(self):
        if self.running:
            elapsed = time.time() - self.start_time
            self.timer_label.config(text=time.strftime("%H:%M:%S", time.gmtime(elapsed)))
            self.root.after(1000, self.update_timer)
    
    def load_groups(self):
        try:
            response = requests.get(f"{BASE_URL}/groups")
            response.raise_for_status()  # Raise error for bad status codes
            for item in self.group_tree.get_children():
                self.group_tree.delete(item)
                
            for group in response.json():
                self.group_tree.insert("", "end", text=group["name"], values=(group["id"],))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load groups: {str(e)}")
    
    def load_tasks(self, event=None):
        group = self.get_selected_group()
        if not group: return
        
        try:
            response = requests.get(f"{BASE_URL}/tasks", params={"group_id": group["id"]})
            response.raise_for_status()
            for item in self.task_list.get_children():
                self.task_list.delete(item)
                
            for task in response.json():
                self.task_list.insert("", "end", values=(
                    task["id"],
                    task["name"],
                    task["total_hours"],
                    task["hours_per_week"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
    
    def load_history(self, event=None):
        task = self.get_selected_task()
        if not task: return
        
        try:
            response = requests.get(f"{BASE_URL}/time_entries", params={"task_id": task["id"]})
            response.raise_for_status()
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
                
            for entry in response.json():
                # Format duration as H:M:S
                total_seconds = entry["duration"]
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                formatted_duration = f"{hours}h {minutes}m"
                
                self.history_tree.insert("", "end", values=(
                    entry["id"],  # Hidden ID in first position
                    entry["start_time"].split("T")[0],
                    formatted_duration,
                    entry.get("note", "")
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load time entries: {str(e)}")
    
    # Helper methods
    def get_selected_group(self, show_warning=True):
        selection = self.group_tree.selection()
        if not selection: 
            if show_warning:
                messagebox.showwarning("Warning", "No group selected")
            return None
        return {
            "id": self.group_tree.item(selection[0])["values"][0],
            "name": self.group_tree.item(selection[0])["text"]
        }
    
    def update_visualization(self, event=None):
        try:
            mode = self.vis_mode.get()
            period_name = self.period_combo.get()
            period_id = None
            period_obj = None
            
            # Handle "All Time" and period selection
            if period_name != "All Time":
                # Find period ID by name
                for pid, obj in self.periods.items():
                    if obj["name"] == period_name:
                        period_id = pid
                        period_obj = obj
                        break
            
            # Check if period is in the future
            if period_obj:
                from datetime import datetime
                today = datetime.now().date()
                try:
                    start_date = datetime.strptime(period_obj["start_date"], "%Y-%m-%d").date()
                    end_date = datetime.strptime(period_obj["end_date"], "%Y-%m-%d").date()
                    
                    if today < start_date:
                        # Period is in the future
                        self.ax.clear()
                        self.ax.text(0.5, 0.5, "This period is in the future\nNo data available", 
                                    ha='center', va='center', color=self.fg_color, fontsize=12)
                        self.ax.set_title("Period in Future", color=self.fg_color)
                        self.chart_canvas.draw()
                        return
                except Exception as e:
                    print(f"Error parsing dates: {e}")

            # Make API requests with period filtering
            if mode == "group":
                params = {}
                if period_id:
                    params["period_id"] = period_id
                response = requests.get(f"{BASE_URL}/time_by_group", params=params)
                title = "Time by Group"
            else:
                group = self.get_selected_group(show_warning=False)
                group_id = group["id"] if group else None
                params = {}
                if group_id:
                    params["group_id"] = group_id
                if period_id:
                    params["period_id"] = period_id
                response = requests.get(f"{BASE_URL}/time_by_task", params=params)
                title = "Time by Task"
                
            response.raise_for_status()
            data = response.json()
            
            # Clear previous chart
            self.ax.clear()
            
            if not data:
                self.ax.text(0.5, 0.5, "No data available", 
                            ha='center', va='center', color=self.fg_color)
                self.ax.set_title(title, color=self.fg_color)
                self.chart_canvas.draw()
                return
                
            # Prepare data
            labels = [item['name'] for item in data]
            sizes = [item['total_time'] for item in data]
            
            # Create pie chart
            colors = plt.cm.Paired.colors
            wedges, texts, autotexts = self.ax.pie(
                sizes, 
                labels=labels, 
                autopct='%1.1f%%',
                startangle=90,
                colors=colors[:len(labels)]
            )
            
            # Style the chart
            self.ax.set_title(title, color=self.fg_color, fontsize=12)
            self.ax.axis('equal')  # Equal aspect ratio ensures circular pie
            
            # Set text colors
            for text in texts + autotexts:
                text.set_color(self.fg_color)
                text.set_fontsize(10)
                
            # Draw the chart
            self.chart_canvas.draw()
            
        except Exception as e:
            # Show error message on chart
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Error: {str(e)}", 
                        ha='center', va='center', color='red')
            self.ax.set_title("Data Load Error", color='red')
            self.chart_canvas.draw()
            print(f"Error updating visualization: {e}")

    def toggle_timer(self, event=None):
        """Toggle timer with spacebar"""
        if self.running:
            self.stop_timer()
        else:
            self.start_timer()

    def manage_periods(self):
        """Open academic period management window"""
        period_window = tk.Toplevel(self.root)
        period_window.title("Manage Academic Periods")
        period_window.geometry("600x400")
        
        # Create a frame for buttons
        button_frame = ttk.Frame(period_window)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Add Period", command=self.add_period).pack(side=tk.LEFT)
        
        # Create a treeview to list periods
        columns = ("id", "name", "start_date", "end_date")
        self.period_tree = ttk.Treeview(period_window, columns=columns, show="headings", height=15)
        self.period_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.period_tree.heading("id", text="ID")
        self.period_tree.heading("name", text="Name")
        self.period_tree.heading("start_date", text="Start Date")
        self.period_tree.heading("end_date", text="End Date")
        
        self.period_tree.column("id", width=50, anchor=tk.CENTER)
        self.period_tree.column("name", width=150)
        self.period_tree.column("start_date", width=100, anchor=tk.CENTER)
        self.period_tree.column("end_date", width=100, anchor=tk.CENTER)
        self.period_tree.bind("<Button-3>", self.show_period_context_menu)
        
        # Load periods
        self.load_periods()

    def load_periods(self):
        """Load academic periods from server"""
        try:
            response = requests.get(f"{BASE_URL}/periods")
            response.raise_for_status()
            
            # Clear existing data
            for item in self.period_tree.get_children():
                self.period_tree.delete(item)
                
            self.periods = {}
            period_names = ["All Time"]  # Add "All Time" option
            
            for period in response.json():
                self.period_tree.insert("", "end", values=(
                    period["id"],
                    period["name"],
                    period["start_date"],
                    period["end_date"]
                ))
                # Store entire period object
                self.periods[period["id"]] = period
                period_names.append(period["name"])
            
            # Update combobox
            self.period_combo["values"] = period_names
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load periods: {str(e)}")

    def add_period(self):
        """Add a new academic period"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Academic Period")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Start Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        start_entry = ttk.Entry(dialog)
        start_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="End Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        end_entry = ttk.Entry(dialog)
        end_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def save_period():
            name = name_entry.get()
            start = start_entry.get()
            end = end_entry.get()
            
            if not name or not start or not end:
                messagebox.showwarning("Warning", "All fields are required")
                return
                
            try:
                response = requests.post(f"{BASE_URL}/periods", json={
                    "name": name,
                    "start_date": start,
                    "end_date": end
                })
                response.raise_for_status()
                self.load_periods()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add period: {str(e)}")
                
        ttk.Button(dialog, text="Save", command=save_period).grid(row=3, column=0, columnspan=2, pady=10)

    def show_group_context_menu(self, event):
        selection = self.group_tree.selection()
        if not selection: return
        
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Delete Group", command=self.delete_group)
        menu.tk_popup(event.x_root, event.y_root)

    def delete_group(self):
        group = self.get_selected_group()
        if not group: return
        
        if messagebox.askyesno("Confirm", f"Delete group '{group['name']}'? This will delete all its tasks and time entries!"):
            try:
                response = requests.delete(f"{BASE_URL}/groups/{group['id']}")
                response.raise_for_status()
                self.load_groups()
                self.update_visualization()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete group: {str(e)}")

    def show_task_context_menu(self, event):
        selection = self.task_list.selection()
        if not selection: return
        
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Delete Task", command=self.delete_task)
        menu.tk_popup(event.x_root, event.y_root)

    def delete_task(self):
        task = self.get_selected_task()
        if not task: return
        
        if messagebox.askyesno("Confirm", "Delete this task and all its time entries?"):
            try:
                response = requests.delete(f"{BASE_URL}/tasks/{task['id']}")
                response.raise_for_status()
                self.load_tasks()
                self.load_history()
                self.update_visualization()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete task: {str(e)}")

    def show_history_context_menu(self, event):
        selection = self.history_tree.selection()
        if not selection: return
        
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Delete Entry", command=self.delete_time_entry)
        menu.tk_popup(event.x_root, event.y_root)

    def delete_time_entry(self):
        selection = self.history_tree.selection()
        if not selection: return
        
        entry_id = self.history_tree.item(selection[0])["values"][0]  # Hidden ID
        if messagebox.askyesno("Confirm", "Delete this time entry?"):
            try:
                response = requests.delete(f"{BASE_URL}/time_entries/{entry_id}")
                response.raise_for_status()
                self.load_history()
                self.load_tasks()
                self.update_visualization()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete time entry: {str(e)}")

    def show_period_context_menu(self, event):
        selection = self.period_tree.selection()
        if not selection: return
        
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Delete Period", command=self.delete_period)
        menu.tk_popup(event.x_root, event.y_root)

    def delete_period(self):
        selection = self.period_tree.selection()
        if not selection: return
        
        period_id = self.period_tree.item(selection[0])["values"][0]
        period_name = self.period_tree.item(selection[0])["values"][1]
        
        if messagebox.askyesno("Confirm", f"Delete period '{period_name}'?"):
            try:
                response = requests.delete(f"{BASE_URL}/periods/{period_id}")
                response.raise_for_status()
                self.load_periods()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete period: {str(e)}")

    def get_selected_task(self):
        selection = self.task_list.selection()
        if not selection: 
            messagebox.showwarning("Warning", "No task selected")
            return None
        return {
            "id": self.task_list.item(selection[0])["values"][0]
        }

    def backup_database(self):
        """Create a backup of the database file"""
        try:
            # Create backups directory if it doesn't exist
            backup_dir = "backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # Generate timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"database_backup_{timestamp}.db")
            
            # Copy the database file
            shutil.copyfile("database.db", backup_file)
            messagebox.showinfo("Backup Successful", f"Database backup created:\n{backup_file}")
        except Exception as e:
            messagebox.showerror("Backup Failed", f"Error creating backup: {str(e)}")

    def restore_database(self):
        """Restore database from a backup file"""
        try:
            # Ask user to select backup file
            file_path = filedialog.askopenfilename(
                title="Select Backup File",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")]
            )
            if not file_path:
                return
                
            # Confirm restore operation
            if not messagebox.askyesno("Confirm Restore", 
                                      "This will replace your current database.\n"
                                      "Make sure the server is not running!\n\n"
                                      "Continue?"):
                return
                
            # Close server connection if possible
            try:
                requests.get(f"{BASE_URL}/shutdown", timeout=1)
            except:
                pass
                
            # Wait a moment for server to shut down
            time.sleep(1)
            
            # Replace database file
            shutil.copyfile(file_path, "database.db")
            
            # Restart server
            threading.Thread(target=self.start_server).start()
            
            # Wait for server to start
            time.sleep(1)
            
            # Reload all data
            self.load_groups()
            self.load_periods()
            self.update_visualization()
            
            messagebox.showinfo("Restore Successful", "Database restored successfully!")
        except Exception as e:
            messagebox.showerror("Restore Failed", f"Error restoring database: {str(e)}")

    def start_server(self):
        """Start the Node.js server"""
        try:
            os.system("node server.js")
        except Exception as e:
            print(f"Error starting server: {e}")

    def export_csv(self):
        """Export all data to CSV file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save Database Export"
        )
        if not file_path:
            return
            
        try:
            # Get all data from server
            groups = requests.get(f"{BASE_URL}/groups").json()
            tasks = requests.get(f"{BASE_URL}/all_tasks").json()
            time_entries = requests.get(f"{BASE_URL}/all_time_entries").json()
            periods = requests.get(f"{BASE_URL}/periods").json()
            
            # Write to CSV
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write groups
                writer.writerow(["Groups"])
                writer.writerow(["ID", "Name"])
                for group in groups:
                    writer.writerow([group["id"], group["name"]])
                
                # Write separator
                writer.writerow([])
                writer.writerow(["Tasks"])
                writer.writerow(["ID", "Name", "Group ID"])
                for task in tasks:
                    writer.writerow([task["id"], task["name"], task["group_id"]])
                
                # Write separator
                writer.writerow([])
                writer.writerow(["Time Entries"])
                writer.writerow(["ID", "Task ID", "Start Time", "End Time", "Duration", "Note", "Period ID"])
                for entry in time_entries:
                    writer.writerow([
                        entry["id"],
                        entry["task_id"],
                        entry["start_time"],
                        entry["end_time"],
                        entry["duration"],
                        entry.get("note", ""),
                        entry.get("period_id", "")
                    ])
                
                # Write separator
                writer.writerow([])
                writer.writerow(["Academic Periods"])
                writer.writerow(["ID", "Name", "Start Date", "End Date"])
                for period in periods:
                    writer.writerow([
                        period["id"],
                        period["name"],
                        period["start_date"],
                        period["end_date"]
                    ])
            
            messagebox.showinfo("Export Successful", f"Database exported to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Error exporting database: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()
