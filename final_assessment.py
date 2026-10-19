import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

class CondoMaintenanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Premium Condominium Management")
        self.root.state("zoomed")
        
        # Modern dark theme
        self.BG = "#0F172A"
        self.BG_LIGHT = "#36549B"
        self.PRIMARY = "#3B82F6"
        self.HOVER = "#2563EB"
        self.SUCCESS = "#10B981"
        self.WARNING = "#F59E0B"
        self.TEXT = "#F1F5F9"
        self.TEXT_GRAY = "#94A3B8"
        self.CARD = "#1E293B"
        
        self.root.configure(bg=self.BG)
        
        # Sample data with more incidents
        self.incidents = [
            {"id": "INC-001", "date": "2025-12-24", "title": "Leaking Pipe", "category": "Plumbing", 
             "location": "Unit 12-03", "status": "In Progress", "assigned": "Plumbing Team", "priority": "High"},
            {"id": "INC-002", "date": "2025-12-23", "title": "Flickering Light", "category": "Electrical", 
             "location": "Lobby", "status": "Pending", "assigned": "-", "priority": "Medium"},
            {"id": "INC-003", "date": "2025-12-22", "title": "Lift Malfunction", "category": "Lift", 
             "location": "Block B", "status": "Resolved", "assigned": "Lift Vendor", "priority": "Critical"},
            {"id": "INC-004", "date": "2025-12-21", "title": "AC Not Working", "category": "HVAC", 
             "location": "Unit 8-05", "status": "In Progress", "assigned": "HVAC Team", "priority": "High"},
            {"id": "INC-005", "date": "2025-12-20", "title": "Broken Window", "category": "Facilities", 
             "location": "Gym Area", "status": "Pending", "assigned": "-", "priority": "Low"},
            {"id": "INC-006", "date": "2025-12-19", "title": "Water Heater Issue", "category": "Plumbing", 
             "location": "Unit 5-12", "status": "Resolved", "assigned": "Plumbing Team", "priority": "Medium"},
        ]
        self.incident_counter = 7
        
        # Track status updates for automatic report generation
        self.daily_status_updates = 0
        self.status_update_log = []
        self.last_report_date = datetime.now().strftime("%Y-%m-%d")
        
        self.setup_style()
        self.root.attributes("-alpha", 0.0)
        self.fade_in()
        
        # Set window close protocol to show exit confirmation
        self.root.protocol("WM_DELETE_WINDOW", self.exit_application)
        
        self.create_sidebar()
        self.create_main_content()
        self.show_dashboard()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Card.TFrame", background=self.CARD)
        style.configure("Primary.TButton", font=("Segoe UI", 11, "bold"), padding=12,
                       background=self.PRIMARY, foreground="white", borderwidth=0)
        style.map("Primary.TButton", background=[('active', self.HOVER)])
        
        style.configure("Dash.Treeview", background=self.BG_LIGHT, foreground=self.TEXT,
                       fieldbackground=self.BG_LIGHT, borderwidth=0, font=("Segoe UI", 10))
        style.configure("Dash.Treeview.Heading", background=self.CARD, foreground=self.TEXT,
                       borderwidth=0, font=("Segoe UI", 11, "bold"))
        style.map("Dash.Treeview", background=[("selected", self.PRIMARY)])

    def fade_in(self, alpha=0.0):
        if alpha < 1.0:
            alpha += 0.08
            self.root.attributes("-alpha", alpha)
            self.root.after(20, lambda: self.fade_in(alpha))

    def check_daily_reset(self):
        """Reset counter when a new day begins"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        if current_date != self.last_report_date:
            self.daily_status_updates = 0
            self.status_update_log = []
            self.last_report_date = current_date

    def log_status_update(self, incident_id, old_status, new_status):
        """Records each status change and triggers automatic report at 10 updates"""
        self.check_daily_reset()
        
        update_entry = {
            "incident_id": incident_id,
            "old_status": old_status,
            "new_status": new_status,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.status_update_log.append(update_entry)
        self.daily_status_updates += 1
        
        # Trigger automatic report generation when 10+ updates
        if self.daily_status_updates >= 10:
            self.generate_automatic_report()

    def generate_automatic_report(self):
        """Creates and displays comprehensive automatic report in a popup window"""
        report_content = f"""
AUTOMATIC SUMMARY REPORT - TRIGGERED
{'='*70}

Report Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}
Trigger: 10 or more status updates detected ({self.daily_status_updates} updates today)

{'='*70}

DAILY STATISTICS
{'-'*70}
Total Incidents Reported Today:     {len(self.incidents)}
Total Status Updates Today:         {self.daily_status_updates}

Current Status Distribution:
- Pending:                          {len([i for i in self.incidents if i["status"]=="Pending"])}
- Awaiting Quote:                   {len([i for i in self.incidents if i["status"]=="Awaiting Quote"])}
- In Progress:                      {len([i for i in self.incidents if i["status"]=="In Progress"])}
- Resolved:                         {len([i for i in self.incidents if i["status"]=="Resolved"])}
- Closed:                           {len([i for i in self.incidents if i["status"]=="Closed"])}

Category Breakdown:
- Plumbing:                         {len([i for i in self.incidents if i["category"]=="Plumbing"])}
- Electrical:                       {len([i for i in self.incidents if i["category"]=="Electrical"])}
- Lift:                             {len([i for i in self.incidents if i["category"]=="Lift"])}
- HVAC:                             {len([i for i in self.incidents if i["category"]=="HVAC"])}
- Facilities:                       {len([i for i in self.incidents if i["category"]=="Facilities"])}
- Security:                         {len([i for i in self.incidents if i["category"]=="Security"])}

{'='*70}

STATUS UPDATE LOG (Last {min(10, len(self.status_update_log))} updates)
{'-'*70}
"""
        # Add last 10 status updates to report
        for i, update in enumerate(self.status_update_log[-10:], 1):
            report_content += f"\n{i}. [{update['timestamp']}] {update['incident_id']}: "
            report_content += f"{update['old_status']} → {update['new_status']}"
        
        report_content += f"""

{'='*70}

Priority Distribution:
- Critical:                         {len([i for i in self.incidents if i["priority"]=="Critical"])}
- High:                             {len([i for i in self.incidents if i["priority"]=="High"])}
- Medium:                           {len([i for i in self.incidents if i["priority"]=="Medium"])}
- Low:                              {len([i for i in self.incidents if i["priority"]=="Low"])}

Unassigned Incidents:               {len([i for i in self.incidents if i["assigned"]=="-"])}

Notes:
- This report was automatically generated due to {self.daily_status_updates} status updates today
- System threshold: 10 status updates per day
- Report counter will reset at midnight

{'='*70}
End of Automatic Report
"""
        
        # Display the report in a popup window
        report_window = tk.Toplevel(self.root)
        report_window.title("🔔 Automatic Summary Report Generated")
        report_window.geometry("900x700")
        report_window.configure(bg=self.BG)
        
        header = tk.Frame(report_window, bg=self.BG)
        header.pack(fill="x", padx=20, pady=20)
        
        tk.Label(header, text="🔔 Automatic Report Generated", 
                font=("Segoe UI", 20, "bold"), bg=self.BG, fg=self.SUCCESS).pack(anchor="w")
        tk.Label(header, text=f"Triggered by {self.daily_status_updates} status updates today", 
                font=("Segoe UI", 11), bg=self.BG, fg=self.TEXT_GRAY).pack(anchor="w", pady=5)
        
        txt = scrolledtext.ScrolledText(report_window, font=("Consolas", 10), 
                                       bg=self.BG_LIGHT, fg=self.TEXT, padx=20, pady=15)
        txt.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        txt.insert("1.0", report_content.strip())
        txt.config(state="disabled")
        
        # Show confirmation message
        messagebox.showinfo("Report Generated", 
                          f"Automatic summary report has been generated!\n\n"
                          f"Trigger: {self.daily_status_updates} status updates detected today.\n"
                          f"The status update counter has been reset.")
        
        # Reset the counter after generating report
        self.daily_status_updates = 0
        self.status_update_log = []
        self.update_counter_display()

    def exit_application(self):
        """Exit the application with confirmation"""
        result = messagebox.askyesno("Exit Application", 
                                    "Are you sure you want to exit?\n\n"
                                    "All unsaved data will be lost.",
                                    icon='warning')
        if result:
            self.root.destroy()

    def create_sidebar(self):
        sidebar = tk.Frame(self.root, bg=self.BG_LIGHT, width=260)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Logo
        logo = tk.Frame(sidebar, bg=self.BG_LIGHT)
        logo.pack(pady=35, padx=20)
        tk.Label(logo, text="🏢", font=("Segoe UI", 36), bg=self.BG_LIGHT).pack()
        tk.Label(logo, text="Condo Manager", font=("Segoe UI", 16, "bold"), 
                bg=self.BG_LIGHT, fg=self.TEXT).pack(pady=5)
        tk.Label(logo, text="Professional Edition", font=("Segoe UI", 9), 
                bg=self.BG_LIGHT, fg=self.TEXT_GRAY).pack()
        
        # Nav buttons
        nav = tk.Frame(sidebar, bg=self.BG_LIGHT)
        nav.pack(fill="both", expand=True, padx=12, pady=20)
        
        navs = [("📊", "Dashboard", self.show_dashboard), ("➕", "Add Incident", self.show_add),
                ("🔍", "View All", self.show_view), ("👥", "Assign", self.show_assign),
                ("🔄", "Update Status", self.show_update), ("📈", "Reports", self.show_reports)]
        
        for icon, text, cmd in navs:
            self.nav_btn(nav, icon, text, cmd).pack(fill="x", pady=4)
        
        # ========================================================================
        # ✨ EXIT BUTTON - Red styled button with confirmation
        # ========================================================================
        exit_btn = tk.Frame(nav, bg="#EF4444", cursor="hand2", relief="ridge", bd=2)
        exit_inner = tk.Frame(exit_btn, bg="#EF4444")
        exit_inner.pack(fill="both", padx=12, pady=12)
        
        tk.Label(exit_inner, text="🚪", font=("Segoe UI", 18), bg="#EF4444", fg="white").pack(side="left", padx=(0, 12))
        tk.Label(exit_inner, text="Exit", font=("Segoe UI", 11, "bold"), bg="#EF4444", fg="white").pack(side="left")
        
        def exit_enter(e):
            for w in [exit_btn, exit_inner] + list(exit_inner.winfo_children()):
                w.configure(bg="#DC2626")
        def exit_leave(e):
            for w in [exit_btn, exit_inner] + list(exit_inner.winfo_children()):
                w.configure(bg="#EF4444")
        
        for w in [exit_btn, exit_inner] + list(exit_inner.winfo_children()):
            w.bind("<Enter>", exit_enter)
            w.bind("<Leave>", exit_leave)
            w.bind("<Button-1>", lambda e: self.exit_application())
        
        exit_btn.pack(fill="x", pady=(15, 4))
        # ========================================================================
        
        # Status update counter display
        counter_frame = tk.Frame(sidebar, bg=self.BG_LIGHT)
        counter_frame.pack(side="bottom", pady=10)
        
        tk.Label(counter_frame, text="📊 Daily Updates", font=("Segoe UI", 9, "bold"), 
                bg=self.BG_LIGHT, fg=self.TEXT_GRAY).pack()
        self.update_counter_label = tk.Label(counter_frame, 
                                            text=f"{self.daily_status_updates}/10", 
                                            font=("Segoe UI", 16, "bold"), 
                                            bg=self.BG_LIGHT, fg=self.SUCCESS)
        self.update_counter_label.pack(pady=2)
        tk.Label(counter_frame, text="Auto-report at 10", font=("Segoe UI", 8), 
                bg=self.BG_LIGHT, fg=self.TEXT_GRAY).pack()
        
        # Footer
        footer = tk.Frame(sidebar, bg=self.BG_LIGHT)
        footer.pack(side="bottom", pady=18)
        tk.Label(footer, text="© 2025 Condo A", font=("Segoe UI", 9), 
                bg=self.BG_LIGHT, fg=self.TEXT_GRAY).pack()

    def update_counter_display(self):
        """Updates the visual counter with color-coding"""
        if hasattr(self, 'update_counter_label'):
            self.update_counter_label.config(text=f"{self.daily_status_updates}/10")
            if self.daily_status_updates >= 8:
                self.update_counter_label.config(fg=self.WARNING)
            elif self.daily_status_updates >= 10:
                self.update_counter_label.config(fg=self.SUCCESS)
            else:
                self.update_counter_label.config(fg=self.TEXT)

    def nav_btn(self, parent, icon, text, cmd):
        btn = tk.Frame(parent, bg=self.BG_LIGHT, cursor="hand2")
        inner = tk.Frame(btn, bg=self.BG_LIGHT)
        inner.pack(fill="both", padx=12, pady=12)
        
        tk.Label(inner, text=icon, font=("Segoe UI", 18), bg=self.BG_LIGHT, fg=self.TEXT).pack(side="left", padx=(0, 12))
        tk.Label(inner, text=text, font=("Segoe UI", 11, "bold"), bg=self.BG_LIGHT, fg=self.TEXT).pack(side="left")
        
        def enter(e):
            for w in [btn, inner] + list(inner.winfo_children()):
                w.configure(bg=self.PRIMARY)
        def leave(e):
            for w in [btn, inner] + list(inner.winfo_children()):
                w.configure(bg=self.BG_LIGHT)
        
        for w in [btn, inner] + list(inner.winfo_children()):
            w.bind("<Enter>", enter)
            w.bind("<Leave>", leave)
            w.bind("<Button-1>", lambda e: cmd())
        
        return btn

    def create_main_content(self):
        self.main = tk.Frame(self.root, bg=self.BG)
        self.main.pack(side="right", fill="both", expand=True)

    def clear(self):
        for w in self.main.winfo_children():
            w.destroy()

    def show_dashboard(self):
        self.clear()
        
        # Header
        hdr = tk.Frame(self.main, bg=self.BG)
        hdr.pack(fill="x", padx=35, pady=28)
        tk.Label(hdr, text="Dashboard Overview", font=("Segoe UI", 30, "bold"), 
                bg=self.BG, fg=self.TEXT).pack(anchor="w")
        tk.Label(hdr, text=datetime.now().strftime("Today is %A, %B %d, %Y"), 
                font=("Segoe UI", 11), bg=self.BG, fg=self.TEXT_GRAY).pack(anchor="w", pady=4)
        
        # Stats
        stats = tk.Frame(self.main, bg=self.BG)
        stats.pack(fill="x", padx=35, pady=18)
        
        data = [("Total", len(self.incidents), "📋", self.PRIMARY),
                ("Pending", len([i for i in self.incidents if i["status"]=="Pending"]), "⏳", self.WARNING),
                ("Progress", len([i for i in self.incidents if i["status"]=="In Progress"]), "🔄", self.PRIMARY),
                ("Done", len([i for i in self.incidents if i["status"]=="Resolved"]), "✅", self.SUCCESS)]
        
        for i, (lbl, val, icon, clr) in enumerate(data):
            card = tk.Frame(stats, bg=self.CARD)
            card.grid(row=0, column=i, padx=8, sticky="ew")
            stats.columnconfigure(i, weight=1)
            
            tk.Label(card, text=icon, font=("Segoe UI", 32), bg=self.CARD).pack(pady=(18, 8))
            tk.Label(card, text=str(val), font=("Segoe UI", 28, "bold"), bg=self.CARD, fg=clr).pack()
            tk.Label(card, text=lbl, font=("Segoe UI", 10), bg=self.CARD, fg=self.TEXT_GRAY).pack(pady=(4, 18))
        
        # Recent
        recent = tk.Frame(self.main, bg=self.CARD)
        recent.pack(fill="both", expand=True, padx=35, pady=(0, 28))
        
        tk.Label(recent, text="📌 Recent Incidents", font=("Segoe UI", 18, "bold"), 
                bg=self.CARD, fg=self.TEXT).pack(anchor="w", padx=22, pady=(22, 12))
        
        tree_frame = tk.Frame(recent, bg=self.CARD)
        tree_frame.pack(fill="both", expand=True, padx=22, pady=(0, 22))
        
        cols = ("ID", "Date", "Title", "Category", "Priority", "Status")
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=10, style="Dash.Treeview")
        
        for col, w in zip(cols, [90, 100, 240, 110, 90, 110]):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center")
        
        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)
        
        for inc in self.incidents:
            tree.insert("", "end", values=(inc["id"], inc["date"], inc["title"], 
                                          inc["category"], inc["priority"], inc["status"]))

    def show_add(self):
        self.clear()
        
        hdr = tk.Frame(self.main, bg=self.BG)
        hdr.pack(fill="x", padx=35, pady=28)
        tk.Label(hdr, text="Report New Incident", font=("Segoe UI", 30, "bold"), 
                bg=self.BG, fg=self.TEXT).pack(anchor="w")
        tk.Label(hdr, text="Complete the form below to create a maintenance request", 
                font=("Segoe UI", 11), bg=self.BG, fg=self.TEXT_GRAY).pack(anchor="w", pady=4)
        
        card = tk.Frame(self.main, bg=self.CARD)
        card.pack(fill="both", expand=True, padx=35, pady=(0, 28))
        
        form = tk.Frame(card, bg=self.CARD)
        form.pack(padx=35, pady=35)
        
        self.entries = {}
        
        # Title - Entry (single line)
        tk.Label(form, text="Incident Title", font=("Segoe UI", 11, "bold"), 
                bg=self.CARD, fg=self.TEXT).grid(row=0, column=0, sticky="w", pady=(0, 6))
        title_entry = tk.Entry(form, font=("Segoe UI", 11), bg=self.BG_LIGHT, fg=self.TEXT, 
                              relief="flat", bd=10)
        title_entry.insert(0, "e.g., Leaking pipe in Unit 12-03")
        title_entry.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.entries["Title"] = title_entry
        
        # Category - Entry (single line)
        tk.Label(form, text="Category", font=("Segoe UI", 11, "bold"), 
                bg=self.CARD, fg=self.TEXT).grid(row=2, column=0, sticky="w", pady=(0, 6))
        cat_entry = tk.Entry(form, font=("Segoe UI", 11), bg=self.BG_LIGHT, fg=self.TEXT, 
                            relief="flat", bd=10)
        cat_entry.insert(0, "e.g., Plumbing")
        cat_entry.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        self.entries["Category"] = cat_entry
        
        tk.Label(form, text="💡 Options: Plumbing, Electrical, HVAC, Lift, Facilities, Security", 
                font=("Segoe UI", 9), bg=self.CARD, fg=self.TEXT_GRAY, wraplength=500, justify="left").grid(row=4, column=0, sticky="w", pady=(0, 20))
        
        # Priority - Entry (single line)
        tk.Label(form, text="Priority", font=("Segoe UI", 11, "bold"), 
                bg=self.CARD, fg=self.TEXT).grid(row=5, column=0, sticky="w", pady=(0, 6))
        priority_entry = tk.Entry(form, font=("Segoe UI", 11), bg=self.BG_LIGHT, fg=self.TEXT, 
                                 relief="flat", bd=10)
        priority_entry.insert(0, "e.g., Medium")
        priority_entry.grid(row=6, column=0, sticky="ew", pady=(0, 10))
        self.entries["Priority"] = priority_entry
        
        tk.Label(form, text="💡 Options: Low, Medium, High, Critical", 
                font=("Segoe UI", 9), bg=self.CARD, fg=self.TEXT_GRAY, wraplength=500, justify="left").grid(row=7, column=0, sticky="w", pady=(0, 20))
        
        # Location - Entry (single line)
        tk.Label(form, text="Location", font=("Segoe UI", 11, "bold"), 
                bg=self.CARD, fg=self.TEXT).grid(row=8, column=0, sticky="w", pady=(0, 6))
        loc_entry = tk.Entry(form, font=("Segoe UI", 11), bg=self.BG_LIGHT, fg=self.TEXT, 
                            relief="flat", bd=10)
        loc_entry.insert(0, "e.g., Block A, Level 15, Unit 03")
        loc_entry.grid(row=9, column=0, sticky="ew", pady=(0, 20))
        self.entries["Location"] = loc_entry
        
        # Description - Text (multi-line for detailed descriptions)
        tk.Label(form, text="Description", font=("Segoe UI", 11, "bold"), 
                bg=self.CARD, fg=self.TEXT).grid(row=10, column=0, sticky="w", pady=(0, 6))
        desc_txt = tk.Text(form, font=("Segoe UI", 10), bg=self.BG_LIGHT, fg=self.TEXT, 
                          height=5, relief="flat", bd=2, wrap="word")
        desc_txt.insert("1.0", "Describe the issue in detail...")
        desc_txt.grid(row=11, column=0, sticky="ew", pady=(0, 20))
        self.entries["Description"] = desc_txt
        
        form.columnconfigure(0, weight=1)
        
        tk.Button(form, text="Submit Report", font=("Segoe UI", 11, "bold"), 
                 bg=self.SUCCESS, fg="white", relief="flat", cursor="hand2",
                 command=self.submit, padx=35, pady=12).grid(row=12, column=0, pady=18)

    def submit(self):
        title = self.entries["Title"].get().strip()
        category = self.entries["Category"].get().strip()
        priority = self.entries["Priority"].get().strip()
        location = self.entries["Location"].get().strip()
        description = self.entries["Description"].get("1.0", "end-1c").strip()
        
        placeholders = ["e.g., Leaking pipe in Unit 12-03", "e.g., Plumbing", "e.g., Medium",
                       "e.g., Block A, Level 15, Unit 03", "Describe the issue in detail..."]
        
        valid_categories = ["Plumbing", "Electrical", "HVAC", "Lift", "Facilities", "Security"]
        valid_priorities = ["Low", "Medium", "High", "Critical"]
        
        if (not title or title == placeholders[0] or
            not category or category == placeholders[1] or
            not priority or priority == placeholders[2] or
            not location or location == placeholders[3] or
            not description or description == placeholders[4]):
            messagebox.showerror("Validation Error", "Please fill in all required fields!")
            return
        
        if category not in valid_categories:
            messagebox.showerror("Validation Error", f"Invalid category! Please use: {', '.join(valid_categories)}")
            return
        
        if priority not in valid_priorities:
            messagebox.showerror("Validation Error", f"Invalid priority! Please use: {', '.join(valid_priorities)}")
            return
        
        # Add new incident
        new_incident = {
            "id": f"INC-{str(self.incident_counter).zfill(3)}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "title": title,
            "category": category,
            "location": location,
            "status": "Pending",
            "assigned": "-",
            "priority": priority
        }
        self.incidents.append(new_incident)
        self.incident_counter += 1
        
        messagebox.showinfo("Success", f"Incident {new_incident['id']} reported successfully!")
        self.show_dashboard()

    def show_view(self):
        self.clear()
        
        hdr = tk.Frame(self.main, bg=self.BG)
        hdr.pack(fill="x", padx=35, pady=28)
        tk.Label(hdr, text="Search & View All Incidents", font=("Segoe UI", 30, "bold"), 
                bg=self.BG, fg=self.TEXT).pack(anchor="w")
        tk.Label(hdr, text=f"Search and filter through {len(self.incidents)} total incidents", 
                font=("Segoe UI", 11), bg=self.BG, fg=self.TEXT_GRAY).pack(anchor="w", pady=4)
        
        # Search section
        search_card = tk.Frame(self.main, bg=self.CARD)
        search_card.pack(fill="x", padx=35, pady=(0, 15))
        
        search_inner = tk.Frame(search_card, bg=self.CARD)
        search_inner.pack(padx=22, pady=22)
        
        tk.Label(search_inner, text="🔍 Search", font=("Segoe UI", 14, "bold"), 
                bg=self.CARD, fg=self.TEXT).pack(anchor="w", pady=(0, 10))
        
        search_frame = tk.Frame(search_inner, bg=self.CARD)
        search_frame.pack(fill="x")
        
        # Search Entry (single line)
        tk.Label(search_frame, text="Search by ID, title, category, location, or status:", font=("Segoe UI", 10), 
                bg=self.CARD, fg=self.TEXT_GRAY).grid(row=0, column=0, sticky="w", pady=(0, 5), columnspan=3)
        
        search_entry = tk.Entry(search_frame, font=("Segoe UI", 11), bg=self.BG_LIGHT, 
                               fg=self.TEXT, relief="flat", bd=10)
        search_entry.insert(0, "Enter search term...")
        search_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10), columnspan=3)
        search_frame.columnconfigure(0, weight=1)
        
        # Filter by status - Entry
        tk.Label(search_frame, text="Status Filter:", font=("Segoe UI", 10), 
                bg=self.CARD, fg=self.TEXT_GRAY).grid(row=2, column=0, sticky="w", pady=(15, 5))
        
        status_entry = tk.Entry(search_frame, font=("Segoe UI", 11), bg=self.BG_LIGHT, 
                               fg=self.TEXT, relief="flat", bd=10)
        status_entry.insert(0, "All")
        status_entry.grid(row=3, column=0, sticky="ew", padx=(0, 10))
        
        tk.Label(search_frame, text="💡 Options: All, Pending, In Progress, Resolved, Closed", 
                font=("Segoe UI", 8), bg=self.CARD, fg=self.TEXT_GRAY, wraplength=200).grid(row=4, column=0, sticky="w", pady=(2, 0))
        
        # Filter by priority - Entry
        tk.Label(search_frame, text="Priority Filter:", font=("Segoe UI", 10), 
                bg=self.CARD, fg=self.TEXT_GRAY).grid(row=2, column=1, sticky="w", pady=(15, 5))
        
        priority_entry = tk.Entry(search_frame, font=("Segoe UI", 11), bg=self.BG_LIGHT, 
                                 fg=self.TEXT, relief="flat", bd=10)
        priority_entry.insert(0, "All")
        priority_entry.grid(row=3, column=1, sticky="ew")
        
        tk.Label(search_frame, text="💡 Options: All, Low, Medium, High, Critical", 
                font=("Segoe UI", 8), bg=self.CARD, fg=self.TEXT_GRAY, wraplength=200).grid(row=4, column=1, sticky="w", pady=(2, 0))
        
        # Results table
        results_card = tk.Frame(self.main, bg=self.CARD)
        results_card.pack(fill="both", expand=True, padx=35, pady=(0, 28))
        
        tk.Label(results_card, text="📋 Search Results", font=("Segoe UI", 14, "bold"), 
                bg=self.CARD, fg=self.TEXT).pack(anchor="w", padx=22, pady=(22, 12))
        
        tree_frame = tk.Frame(results_card, bg=self.CARD)
        tree_frame.pack(fill="both", expand=True, padx=22, pady=(0, 22))
        
        cols = ("ID", "Date", "Title", "Category", "Location", "Priority", "Status", "Assigned")
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=12, style="Dash.Treeview")
        
        for col, w in zip(cols, [80, 95, 180, 95, 135, 75, 95, 120]):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center")
        
        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)
        
        # Result count label
        result_label = tk.Label(results_card, text=f"Found {len(self.incidents)} incident(s)", 
                               font=("Segoe UI", 10), bg=self.CARD, fg=self.TEXT_GRAY)
        result_label.pack(anchor="w", padx=22, pady=(0, 5))
        
        # Function to perform search
        def perform_search(*args):
            for item in tree.get_children():
                tree.delete(item)
            
            search_text = search_entry.get().strip().lower()
            status_val = status_entry.get().strip()
            priority_val = priority_entry.get().strip()
            
            filtered = self.incidents
            
            if search_text and search_text != "enter search term...":
                filtered = [inc for inc in filtered if 
                           search_text in inc["id"].lower() or
                           search_text in inc["title"].lower() or
                           search_text in inc["category"].lower() or
                           search_text in inc["location"].lower() or
                           search_text in inc["status"].lower()]
            
            if status_val and status_val != "All":
                filtered = [inc for inc in filtered if inc["status"] == status_val]
            
            if priority_val and priority_val != "All":
                filtered = [inc for inc in filtered if inc["priority"] == priority_val]
            
            for inc in reversed(filtered):
                tree.insert("", "end", values=(inc["id"], inc["date"], inc["title"], inc["category"],
                                              inc["location"], inc["priority"], inc["status"], inc["assigned"]))
            
            result_label.config(text=f"Found {len(filtered)} incident(s)")
        
        # Search button
        btn_frame = tk.Frame(search_inner, bg=self.CARD)
        btn_frame.pack(pady=(15, 0))
        
        tk.Button(btn_frame, text="🔍 Search", font=("Segoe UI", 10, "bold"), 
                 bg=self.PRIMARY, fg="white", relief="flat", cursor="hand2",
                 command=perform_search, padx=25, pady=10).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="↻ Clear Filters", font=("Segoe UI", 10, "bold"), 
                 bg=self.BG_LIGHT, fg=self.TEXT, relief="flat", cursor="hand2",
                 command=lambda: [search_entry.delete(0, "end"), search_entry.insert(0, "Enter search term..."),
                                 status_entry.delete(0, "end"), status_entry.insert(0, "All"),
                                 priority_entry.delete(0, "end"), priority_entry.insert(0, "All"),
                                 perform_search()],
                 padx=25, pady=10).pack(side="left", padx=5)
        
        perform_search()

    def show_assign(self):
        self.clear()
        
        hdr = tk.Frame(self.main, bg=self.BG)
        hdr.pack(fill="x", padx=35, pady=28)
        tk.Label(hdr, text="Assign Tasks", font=("Segoe UI", 30, "bold"), 
                bg=self.BG, fg=self.TEXT).pack(anchor="w")
        tk.Label(hdr, text="Assign incidents to maintenance teams or vendors", 
                font=("Segoe UI", 11), bg=self.BG, fg=self.TEXT_GRAY).pack(anchor="w", pady=4)
        
        card = tk.Frame(self.main, bg=self.CARD)
        card.pack(fill="both", expand=True, padx=35, pady=(0, 28))
        
        form = tk.Frame(card, bg=self.CARD)
        form.pack(padx=50, pady=50)
        
        tk.Label(form, text="Incident ID", font=("Segoe UI", 11, "bold"), 
                bg=self.CARD, fg=self.TEXT).grid(row=0, column=0, sticky="w", pady=(0, 6))
        
        id_entry = tk.Entry(form, font=("Segoe UI", 11), bg=self.BG_LIGHT, fg=self.TEXT, 
                           relief="flat", bd=10, width=50)
        id_entry.insert(0, "e.g., INC-001")
        id_entry.grid(row=1, column=0, pady=(0, 25))
        
        unassigned = [i["id"] for i in self.incidents if i["assigned"] == "-"]
        tk.Label(form, text=f"💡 Unassigned incidents: {', '.join(unassigned) if unassigned else 'None'}", 
                font=("Segoe UI", 9), bg=self.CARD, fg=self.TEXT_GRAY, wraplength=500, justify="left").grid(row=2, column=0, sticky="w", pady=(0, 15))
        
        tk.Label(form, text="Assign To (Team/Vendor)", font=("Segoe UI", 11, "bold"), 
                bg=self.CARD, fg=self.TEXT).grid(row=3, column=0, sticky="w", pady=(0, 6))
        
        team_entry = tk.Entry(form, font=("Segoe UI", 11), bg=self.BG_LIGHT, fg=self.TEXT, 
                             relief="flat", bd=10, width=50)
        team_entry.insert(0, "e.g., Plumbing Team")
        team_entry.grid(row=4, column=0, pady=(0, 15))
        
        tk.Label(form, text="💡 Available teams: Plumbing Team, Electrical Team, HVAC Team, Lift Maintenance, Facilities Team", 
                font=("Segoe UI", 9), bg=self.CARD, fg=self.TEXT_GRAY, wraplength=500, justify="left").grid(row=5, column=0, sticky="w", pady=(0, 30))
        
        def assign_task():
            inc_id = id_entry.get().strip()
            team = team_entry.get().strip()
            
            if not inc_id or inc_id == "e.g., INC-001":
                messagebox.showerror("Error", "Please enter an Incident ID!")
                return
            
            if not team or team == "e.g., Plumbing Team":
                messagebox.showerror("Error", "Please enter a team/vendor name!")
                return
            
            found = False
            for incident in self.incidents:
                if incident["id"] == inc_id:
                    old_status = incident["status"]
                    incident["assigned"] = team
                    incident["status"] = "In Progress"
                    
                    # Log the status update
                    self.log_status_update(inc_id, old_status, "In Progress")
                    self.update_counter_display()
                    
                    found = True
                    break
            
            if found:
                messagebox.showinfo("Success", f"Incident {inc_id} assigned to {team}!")
                self.show_dashboard()
            else:
                messagebox.showerror("Error", f"Incident ID '{inc_id}' not found!")
        
        tk.Button(form, text="Assign Task", font=("Segoe UI", 11, "bold"), 
                 bg=self.PRIMARY, fg="white", relief="flat", cursor="hand2",
                 command=assign_task, padx=35, pady=12).grid(row=6, column=0)

    def show_update(self):
        self.clear()
        
        hdr = tk.Frame(self.main, bg=self.BG)
        hdr.pack(fill="x", padx=35, pady=28)
        tk.Label(hdr, text="Update Status", font=("Segoe UI", 30, "bold"), 
                bg=self.BG, fg=self.TEXT).pack(anchor="w")
        tk.Label(hdr, text="Change the status of maintenance incidents", 
                font=("Segoe UI", 11), bg=self.BG, fg=self.TEXT_GRAY).pack(anchor="w", pady=4)
        
        card = tk.Frame(self.main, bg=self.CARD)
        card.pack(fill="both", expand=True, padx=35, pady=(0, 28))
        
        form = tk.Frame(card, bg=self.CARD)
        form.pack(padx=50, pady=50)
        
        tk.Label(form, text="Incident ID", font=("Segoe UI", 11, "bold"), 
                bg=self.CARD, fg=self.TEXT).grid(row=0, column=0, sticky="w", pady=(0, 6))
        
        id_entry = tk.Entry(form, font=("Segoe UI", 11), bg=self.BG_LIGHT, fg=self.TEXT, 
                           relief="flat", bd=10, width=50)
        id_entry.insert(0, "e.g., INC-001")
        id_entry.grid(row=1, column=0, pady=(0, 15))
        
        all_ids = [i["id"] for i in self.incidents]
        tk.Label(form, text=f"💡 Available incidents: {', '.join(all_ids)}", 
                font=("Segoe UI", 9), bg=self.CARD, fg=self.TEXT_GRAY, wraplength=500, justify="left").grid(row=2, column=0, sticky="w", pady=(0, 25))
        
        tk.Label(form, text="New Status", font=("Segoe UI", 11, "bold"), 
                bg=self.CARD, fg=self.TEXT).grid(row=3, column=0, sticky="w", pady=(0, 6))
        
        status_entry = tk.Entry(form, font=("Segoe UI", 11), bg=self.BG_LIGHT, fg=self.TEXT, 
                               relief="flat", bd=10, width=50)
        status_entry.insert(0, "e.g., In Progress")
        status_entry.grid(row=4, column=0, pady=(0, 15))
        
        tk.Label(form, text="💡 Valid statuses: Pending, Awaiting Quote, In Progress, Resolved, Closed", 
                font=("Segoe UI", 9), bg=self.CARD, fg=self.TEXT_GRAY, wraplength=500, justify="left").grid(row=5, column=0, sticky="w", pady=(0, 30))
        
        def update_status():
            inc_id = id_entry.get().strip()
            new_status = status_entry.get().strip()
            
            if not inc_id or inc_id == "e.g., INC-001":
                messagebox.showerror("Error", "Please enter an Incident ID!")
                return
            
            if not new_status or new_status == "e.g., In Progress":
                messagebox.showerror("Error", "Please enter a status!")
                return
            
            valid_statuses = ["Pending", "Awaiting Quote", "In Progress", "Resolved", "Closed"]
            if new_status not in valid_statuses:
                messagebox.showerror("Error", f"Invalid status! Please use one of: {', '.join(valid_statuses)}")
                return
            
            found = False
            for incident in self.incidents:
                if incident["id"] == inc_id:
                    old_status = incident["status"]
                    incident["status"] = new_status
                    
                    # Log the status update
                    self.log_status_update(inc_id, old_status, new_status)
                    self.update_counter_display()
                    
                    found = True
                    break
            
            if found:
                messagebox.showinfo("Success", f"Incident {inc_id} status updated to '{new_status}'!")
                self.show_dashboard()
            else:
                messagebox.showerror("Error", f"Incident ID '{inc_id}' not found!")
        
        tk.Button(form, text="Update Status", font=("Segoe UI", 11, "bold"), 
                 bg=self.SUCCESS, fg="white", relief="flat", cursor="hand2",
                 command=update_status, padx=35, pady=12).grid(row=6, column=0)

    def show_reports(self):
        self.clear()
        
        hdr = tk.Frame(self.main, bg=self.BG)
        hdr.pack(fill="x", padx=35, pady=28)
        tk.Label(hdr, text="Daily Summary Report", font=("Segoe UI", 30, "bold"), 
                bg=self.BG, fg=self.TEXT).pack(anchor="w")
        tk.Label(hdr, text=datetime.now().strftime("Generated on %B %d, %Y"), 
                font=("Segoe UI", 11), bg=self.BG, fg=self.TEXT_GRAY).pack(anchor="w", pady=4)
        
        card = tk.Frame(self.main, bg=self.CARD)
        card.pack(fill="both", expand=True, padx=35, pady=(0, 28))
        
        txt = scrolledtext.ScrolledText(card, font=("Consolas", 11), bg=self.BG_LIGHT, 
                                       fg=self.TEXT, padx=25, pady=20, relief="flat")
        txt.pack(fill="both", expand=True, padx=22, pady=22)
        
        report = f"""
DAILY MAINTENANCE SUMMARY REPORT
{'='*65}

Date: {datetime.now().strftime('%B %d, %Y')}

Total Incidents Reported Today:     {len(self.incidents)}
Status Updates Today:               {self.daily_status_updates}
{'-'*65}
- Pending:                          {len([i for i in self.incidents if i["status"]=="Pending"])}
- In Progress:                      {len([i for i in self.incidents if i["status"]=="In Progress"])}
- Resolved:                         {len([i for i in self.incidents if i["status"]=="Resolved"])}

Category Breakdown:
- Plumbing:                         {len([i for i in self.incidents if i["category"]=="Plumbing"])}
- Electrical:                       {len([i for i in self.incidents if i["category"]=="Electrical"])}
- Lift:                             {len([i for i in self.incidents if i["category"]=="Lift"])}
- HVAC:                             {len([i for i in self.incidents if i["category"]=="HVAC"])}
- Facilities:                       {len([i for i in self.incidents if i["category"]=="Facilities"])}

Notes:
- All high-priority incidents assigned within 2 hours
- {len([i for i in self.incidents if i["status"]=="Resolved"])} incidents resolved today
- Excellent response time maintained
- Automatic report will trigger at 10 status updates

Report auto-generated at 23:59 daily.
        """
        txt.insert("end", report.strip())
        txt.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = CondoMaintenanceApp(root)
    root.mainloop()