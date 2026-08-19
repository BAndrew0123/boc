import os
import sqlite3
import csv
import sys
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def get_db_connection():
    if not os.path.exists(DB_PATH):
        messagebox.showerror("Error", f"Database not found at {DB_PATH}. Please run app.py first.")
        return None
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class BOCAdminApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Body of Christ Centre - Advanced Staff Control Panel")
        self.geometry("1180x750")
        self.configure(bg="#0f172a")

        # Graceful Window Close Handler
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Custom Styling
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        # Configure Colors & Fonts
        self.style.configure('.', font=('Helvetica', 10))
        self.style.configure('TNotebook', background='#0f172a', borderwidth=0)
        self.style.configure('TNotebook.Tab', padding=[16, 8], font=('Helvetica', 10, 'bold'), background='#1e293b', foreground='#94a3b8')
        self.style.map('TNotebook.Tab', background=[('selected', '#df5311')], foreground=[('selected', '#ffffff')])
        
        self.style.configure('Treeview', rowheight=28, font=('Helvetica', 9), background='#ffffff', fieldbackground='#ffffff')
        self.style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'), background='#0f172a', foreground='#ffffff')

        # Start with Login Screen Frame
        self.show_login_screen()

    def on_close(self):
        self.destroy()

    def show_login_screen(self):
        self.login_frame = tk.Frame(self, bg="#0f172a")
        self.login_frame.pack(fill="both", expand=True)

        card = tk.Frame(self.login_frame, bg="#1e293b", highlightbackground="#334155", highlightthickness=1, bd=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=440, height=340)

        lbl_icon = tk.Label(card, text="🔒", font=("Helvetica", 36), bg="#1e293b", fg="#df5311")
        lbl_icon.pack(pady=(25, 5))

        lbl_title = tk.Label(card, text="BOC Staff Desktop Authorization", font=("Helvetica", 14, "bold"), bg="#1e293b", fg="#ffffff")
        lbl_title.pack(pady=2)

        lbl_sub = tk.Label(card, text="Enter staff security passcode to access ledger & controls:", font=("Helvetica", 9), bg="#1e293b", fg="#94a3b8")
        lbl_sub.pack(pady=(0, 15))

        self.pass_entry = tk.Entry(card, show="*", font=("Helvetica", 13), width=22, justify="center", bg="#0f172a", fg="#ffffff", insertbackground="#ffffff", relief="flat")
        self.pass_entry.pack(pady=5, ipady=6)
        self.pass_entry.focus()
        self.pass_entry.bind("<Return>", self.verify_passcode)

        lbl_hint = tk.Label(card, text="Default Passcode: admin123", font=("Helvetica", 8, "italic"), bg="#1e293b", fg="#64748b")
        lbl_hint.pack(pady=(2, 15))

        btn_login = tk.Button(card, text="LOG IN TO DESKTOP PANEL", font=("Helvetica", 10, "bold"), bg="#df5311", fg="#ffffff", activebackground="#c2410c", activeforeground="#ffffff", relief="flat", command=self.verify_passcode, cursor="hand2")
        btn_login.pack(ipadx=15, ipady=6)

    def verify_passcode(self, event=None):
        entered = self.pass_entry.get()
        if entered == "admin123":
            self.login_frame.destroy()
            self.build_ui()
            self.load_data()
        else:
            messagebox.showerror("Access Denied", "Incorrect Security Passcode!")
            self.pass_entry.delete(0, tk.END)

    def build_ui(self):
        # Header Banner
        header = tk.Frame(self, bg="#0f172a", height=70)
        header.pack(fill="x", padx=20, pady=10)

        title = tk.Label(header, text="BODY OF CHRIST CENTRE — DESKTOP MANAGEMENT SUITE", font=("Helvetica", 15, "bold"), bg="#0f172a", fg="#ffffff")
        title.pack(side="left")

        btn_refresh = tk.Button(header, text="🔄 Refresh All Data", font=("Helvetica", 9, "bold"), bg="#1e293b", fg="#df5311", relief="flat", command=self.load_data, cursor="hand2")
        btn_refresh.pack(side="right", padx=5)

        # Tabbed Container
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Tabs Definition
        self.tab_stats = tk.Frame(self.notebook, bg="#f8fafc")
        self.tab_donations = tk.Frame(self.notebook, bg="#f8fafc")
        self.tab_activities = tk.Frame(self.notebook, bg="#f8fafc")
        self.tab_projects = tk.Frame(self.notebook, bg="#f8fafc")
        self.tab_gallery = tk.Frame(self.notebook, bg="#f8fafc")
        self.tab_messages = tk.Frame(self.notebook, bg="#f8fafc")

        self.notebook.add(self.tab_stats, text=" 📊 Financial Summary ")
        self.notebook.add(self.tab_donations, text=" 📜 Donations Ledger ")
        self.notebook.add(self.tab_activities, text=" 📅 Events & Volunteers ")
        self.notebook.add(self.tab_projects, text=" 🎓 Children & Projects ")
        self.notebook.add(self.tab_gallery, text=" 📸 Media Gallery ")
        self.notebook.add(self.tab_messages, text=" 📬 Inquiries Inbox ")

        self.setup_stats_tab()
        self.setup_donations_tab()
        self.setup_activities_tab()
        self.setup_projects_tab()
        self.setup_gallery_tab()
        self.setup_messages_tab()

    # ---------------- TAB 1: STATS ----------------
    def setup_stats_tab(self):
        cards_frame = tk.Frame(self.tab_stats, bg="#f8fafc")
        cards_frame.pack(fill="x", padx=20, pady=20)

        self.lbl_stat_total = self.create_card(cards_frame, "Total Verified Raised", "KES 0", "#df5311", 0)
        self.lbl_stat_mpesa = self.create_card(cards_frame, "M-Pesa Ledger Total", "KES 0", "#10b981", 1)
        self.lbl_stat_card = self.create_card(cards_frame, "Bank / Offline Total", "KES 0", "#0284c7", 2)
        self.lbl_stat_volunteers = self.create_card(cards_frame, "Volunteers Count", "0", "#9333ea", 3)
        self.lbl_stat_children = self.create_card(cards_frame, "Children Tracked", "0", "#334155", 4)

    def create_card(self, parent, title, val, color, col):
        card = tk.Frame(parent, bg="#ffffff", highlightbackground="#e2e8f0", highlightthickness=1, bd=0)
        card.grid(row=0, column=col, padx=8, pady=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)

        tk.Label(card, text=title.upper(), font=("Helvetica", 8, "bold"), fg="#64748b", bg="#ffffff").pack(anchor="w", padx=15, pady=(15, 2))
        lbl_val = tk.Label(card, text=val, font=("Helvetica", 15, "bold"), fg=color, bg="#ffffff")
        lbl_val.pack(anchor="w", padx=15, pady=(0, 15))
        return lbl_val

    # ---------------- TAB 2: DONATIONS LEDGER ----------------
    def setup_donations_tab(self):
        toolbar = tk.Frame(self.tab_donations, bg="#f8fafc")
        toolbar.pack(fill="x", padx=15, pady=10)

        tk.Label(toolbar, text="Search Ledger:", font=("Helvetica", 10, "bold"), bg="#f8fafc").pack(side="left", padx=(0, 5))
        self.entry_search = tk.Entry(toolbar, font=("Helvetica", 10), width=25)
        self.entry_search.pack(side="left", padx=5)
        self.entry_search.bind("<KeyRelease>", self.filter_donations)

        btn_delete_don = tk.Button(toolbar, text="🗑️ Delete Selected Record", font=("Helvetica", 9, "bold"), bg="#ef4444", fg="#ffffff", relief="flat", command=self.delete_selected_donation, cursor="hand2")
        btn_delete_don.pack(side="right", padx=5)

        btn_csv = tk.Button(toolbar, text="📥 Export CSV", font=("Helvetica", 9, "bold"), bg="#10b981", fg="#ffffff", relief="flat", command=self.export_csv, cursor="hand2")
        btn_csv.pack(side="right", padx=5)

        btn_cash = tk.Button(toolbar, text="➕ Record Cash Donation", font=("Helvetica", 9, "bold"), bg="#df5311", fg="#ffffff", relief="flat", command=self.modal_add_offline_donation, cursor="hand2")
        btn_cash.pack(side="right", padx=5)

        # Treeview Table
        tree_frame = tk.Frame(self.tab_donations)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        columns = ("id", "code", "donor", "phone", "amount", "method", "cause", "status", "date")
        self.tree_donations = ttk.Treeview(tree_frame, columns=columns, show="headings")

        self.tree_donations.heading("id", text="ID")
        self.tree_donations.heading("code", text="Ref / M-Pesa Code")
        self.tree_donations.heading("donor", text="Donor Name")
        self.tree_donations.heading("phone", text="Phone / Contact")
        self.tree_donations.heading("amount", text="Amount (KES)")
        self.tree_donations.heading("method", text="Payment Method")
        self.tree_donations.heading("cause", text="Target Cause")
        self.tree_donations.heading("status", text="Status")
        self.tree_donations.heading("date", text="Timestamp")

        self.tree_donations.column("id", width=40, anchor="center")
        self.tree_donations.column("code", width=130, anchor="center")
        self.tree_donations.column("donor", width=150)
        self.tree_donations.column("phone", width=120)
        self.tree_donations.column("amount", width=110, anchor="e")
        self.tree_donations.column("method", width=110, anchor="center")
        self.tree_donations.column("cause", width=160)
        self.tree_donations.column("status", width=90, anchor="center")
        self.tree_donations.column("date", width=140, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_donations.yview)
        self.tree_donations.configure(yscroll=scrollbar.set)

        self.tree_donations.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ---------------- TAB 3: ACTIVITIES & VOLUNTEERS ----------------
    def setup_activities_tab(self):
        container = tk.Frame(self.tab_activities, bg="#f8fafc")
        container.pack(fill="both", expand=True, padx=15, pady=15)

        form_frame = tk.LabelFrame(container, text=" Add New Community Activity ", font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#0f172a", bd=1)
        form_frame.pack(side="left", fill="both", expand=False, padx=(0, 10), ipadx=10, ipady=10)

        tk.Label(form_frame, text="Event Title:", bg="#ffffff").pack(anchor="w", pady=(5, 0))
        self.act_title = tk.Entry(form_frame, width=30)
        self.act_title.pack(anchor="w", pady=2)

        tk.Label(form_frame, text="Category:", bg="#ffffff").pack(anchor="w", pady=(5, 0))
        self.act_cat = ttk.Combobox(form_frame, values=["Education", "Health", "Community Outreach", "Spiritual"], width=28)
        self.act_cat.set("Education")
        self.act_cat.pack(anchor="w", pady=2)

        tk.Label(form_frame, text="Event Date (YYYY-MM-DD):", bg="#ffffff").pack(anchor="w", pady=(5, 0))
        self.act_date = tk.Entry(form_frame, width=30)
        self.act_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.act_date.pack(anchor="w", pady=2)

        tk.Label(form_frame, text="Location:", bg="#ffffff").pack(anchor="w", pady=(5, 0))
        self.act_loc = tk.Entry(form_frame, width=30)
        self.act_loc.insert(0, "Body of Christ Centre, Limuru")
        self.act_loc.pack(anchor="w", pady=2)

        tk.Label(form_frame, text="Description:", bg="#ffffff").pack(anchor="w", pady=(5, 0))
        self.act_desc = tk.Text(form_frame, width=30, height=4)
        self.act_desc.pack(anchor="w", pady=2)

        btn_save_act = tk.Button(form_frame, text="Publish Activity", bg="#df5311", fg="#ffffff", font=("Helvetica", 9, "bold"), relief="flat", command=self.save_activity, cursor="hand2")
        btn_save_act.pack(anchor="w", pady=10, fill="x")

        # Right Column: List of Activities + Actions
        list_frame = tk.LabelFrame(container, text=" Published Events & Volunteer Control ", font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#0f172a", bd=1)
        list_frame.pack(side="right", fill="both", expand=True)

        act_toolbar = tk.Frame(list_frame, bg="#ffffff")
        act_toolbar.pack(fill="x", padx=5, pady=5)

        btn_view_vols = tk.Button(act_toolbar, text="👥 View Signed-Up Volunteers", font=("Helvetica", 9, "bold"), bg="#10b981", fg="#ffffff", relief="flat", command=self.view_registered_volunteers, cursor="hand2")
        btn_view_vols.pack(side="left", padx=2)

        btn_del_act = tk.Button(act_toolbar, text="🗑️ Delete Selected Event", font=("Helvetica", 9, "bold"), bg="#ef4444", fg="#ffffff", relief="flat", command=self.delete_selected_activity, cursor="hand2")
        btn_del_act.pack(side="right", padx=2)

        self.tree_activities = ttk.Treeview(list_frame, columns=("id", "title", "cat", "date", "loc", "volunteers"), show="headings")
        self.tree_activities.heading("id", text="ID")
        self.tree_activities.heading("title", text="Event Title")
        self.tree_activities.heading("cat", text="Category")
        self.tree_activities.heading("date", text="Date")
        self.tree_activities.heading("loc", text="Location")
        self.tree_activities.heading("volunteers", text="Signups")

        self.tree_activities.column("id", width=30, anchor="center")
        self.tree_activities.column("title", width=200)
        self.tree_activities.column("cat", width=120)
        self.tree_activities.column("date", width=100, anchor="center")
        self.tree_activities.column("loc", width=150)
        self.tree_activities.column("volunteers", width=80, anchor="center")

        self.tree_activities.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree_activities.bind("<Double-1>", lambda e: self.view_registered_volunteers())

    # ---------------- TAB 4: CHILDREN & PROJECTS ----------------
    def setup_projects_tab(self):
        container = tk.Frame(self.tab_projects, bg="#f8fafc")
        container.pack(fill="both", expand=True, padx=15, pady=15)

        form_frame = tk.LabelFrame(container, text=" Add Child / Project Profile ", font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#0f172a", bd=1)
        form_frame.pack(side="left", fill="both", expand=False, padx=(0, 10), ipadx=10, ipady=10)

        tk.Label(form_frame, text="Name:", bg="#ffffff").pack(anchor="w", pady=(5, 0))
        self.proj_name = tk.Entry(form_frame, width=30)
        self.proj_name.pack(anchor="w", pady=2)

        tk.Label(form_frame, text="Type:", bg="#ffffff").pack(anchor="w", pady=(5, 0))
        self.proj_type = ttk.Combobox(form_frame, values=["Child", "Project"], width=28)
        self.proj_type.set("Child")
        self.proj_type.pack(anchor="w", pady=2)

        tk.Label(form_frame, text="Academic Year / Subtitle:", bg="#ffffff").pack(anchor="w", pady=(5, 0))
        self.proj_year = tk.Entry(form_frame, width=30)
        self.proj_year.pack(anchor="w", pady=2)

        tk.Label(form_frame, text="Target Amount (KES):", bg="#ffffff").pack(anchor="w", pady=(5, 0))
        self.proj_target = tk.Entry(form_frame, width=30)
        self.proj_target.insert(0, "100000")
        self.proj_target.pack(anchor="w", pady=2)

        tk.Label(form_frame, text="Description:", bg="#ffffff").pack(anchor="w", pady=(5, 0))
        self.proj_desc = tk.Text(form_frame, width=30, height=4)
        self.proj_desc.pack(anchor="w", pady=2)

        btn_save_proj = tk.Button(form_frame, text="Add Profile Target", bg="#0f172a", fg="#ffffff", font=("Helvetica", 9, "bold"), relief="flat", command=self.save_project, cursor="hand2")
        btn_save_proj.pack(anchor="w", pady=10, fill="x")

        list_frame = tk.LabelFrame(container, text=" Children Sponsorship & Infrastructure Projects ", font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#0f172a", bd=1)
        list_frame.pack(side="right", fill="both", expand=True)

        proj_toolbar = tk.Frame(list_frame, bg="#ffffff")
        proj_toolbar.pack(fill="x", padx=5, pady=5)

        btn_del_proj = tk.Button(proj_toolbar, text="🗑️ Delete Selected Profile", font=("Helvetica", 9, "bold"), bg="#ef4444", fg="#ffffff", relief="flat", command=self.delete_selected_project, cursor="hand2")
        btn_del_proj.pack(side="right", padx=2)

        self.tree_projects = ttk.Treeview(list_frame, columns=("id", "name", "type", "year", "raised", "target"), show="headings")
        self.tree_projects.heading("id", text="ID")
        self.tree_projects.heading("name", text="Profile Name")
        self.tree_projects.heading("type", text="Type")
        self.tree_projects.heading("year", text="Academic/Subtitle")
        self.tree_projects.heading("raised", text="Raised (KES)")
        self.tree_projects.heading("target", text="Target (KES)")

        self.tree_projects.column("id", width=30, anchor="center")
        self.tree_projects.column("name", width=180)
        self.tree_projects.column("type", width=80, anchor="center")
        self.tree_projects.column("year", width=120)
        self.tree_projects.column("raised", width=110, anchor="e")
        self.tree_projects.column("target", width=110, anchor="e")

        self.tree_projects.pack(fill="both", expand=True, padx=5, pady=5)

    # ---------------- TAB 5: GALLERY MANAGER ----------------
    def setup_gallery_tab(self):
        container = tk.Frame(self.tab_gallery, bg="#f8fafc")
        container.pack(fill="both", expand=True, padx=15, pady=15)

        form_frame = tk.LabelFrame(container, text=" Add Media Photo ", font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#0f172a", bd=1)
        form_frame.pack(side="left", fill="both", expand=False, padx=(0, 10), ipadx=10, ipady=10)

        tk.Label(form_frame, text="Photo Title:", bg="#ffffff").pack(anchor="w", pady=(5, 0))
        self.gal_title = tk.Entry(form_frame, width=30)
        self.gal_title.pack(anchor="w", pady=2)

        tk.Label(form_frame, text="Category:", bg="#ffffff").pack(anchor="w", pady=(5, 0))
        self.gal_cat = ttk.Combobox(form_frame, values=["Events", "Campus", "School", "Community", "Health"], width=28)
        self.gal_cat.set("Events")
        self.gal_cat.pack(anchor="w", pady=2)

        tk.Label(form_frame, text="Image URL:", bg="#ffffff").pack(anchor="w", pady=(5, 0))
        self.gal_url = tk.Entry(form_frame, width=30)
        self.gal_url.insert(0, "https://bodyofchristcentre.co.ke/wp-content/uploads/2024/01/event-2.jpg")
        self.gal_url.pack(anchor="w", pady=2)

        tk.Label(form_frame, text="Caption:", bg="#ffffff").pack(anchor="w", pady=(5, 0))
        self.gal_caption = tk.Entry(form_frame, width=30)
        self.gal_caption.pack(anchor="w", pady=2)

        btn_save_gal = tk.Button(form_frame, text="Add to Website Gallery", bg="#df5311", fg="#ffffff", font=("Helvetica", 9, "bold"), relief="flat", command=self.save_gallery_photo, cursor="hand2")
        btn_save_gal.pack(anchor="w", pady=10, fill="x")

        list_frame = tk.LabelFrame(container, text=" Media Gallery Photos ", font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#0f172a", bd=1)
        list_frame.pack(side="right", fill="both", expand=True)

        gal_toolbar = tk.Frame(list_frame, bg="#ffffff")
        gal_toolbar.pack(fill="x", padx=5, pady=5)

        btn_del_gal = tk.Button(gal_toolbar, text="🗑️ Delete Photo", font=("Helvetica", 9, "bold"), bg="#ef4444", fg="#ffffff", relief="flat", command=self.delete_selected_gallery, cursor="hand2")
        btn_del_gal.pack(side="right", padx=2)

        self.tree_gallery = ttk.Treeview(list_frame, columns=("id", "title", "cat", "url", "caption"), show="headings")
        self.tree_gallery.heading("id", text="ID")
        self.tree_gallery.heading("title", text="Photo Title")
        self.tree_gallery.heading("cat", text="Category")
        self.tree_gallery.heading("url", text="Image URL")
        self.tree_gallery.heading("caption", text="Caption")

        self.tree_gallery.column("id", width=30, anchor="center")
        self.tree_gallery.column("title", width=160)
        self.tree_gallery.column("cat", width=100, anchor="center")
        self.tree_gallery.column("url", width=250)
        self.tree_gallery.column("caption", width=200)

        self.tree_gallery.pack(fill="both", expand=True, padx=5, pady=5)

    # ---------------- TAB 6: MESSAGES INBOX ----------------
    def setup_messages_tab(self):
        container = tk.Frame(self.tab_messages, bg="#f8fafc")
        container.pack(fill="both", expand=True, padx=15, pady=15)

        toolbar = tk.Frame(container, bg="#f8fafc")
        toolbar.pack(fill="x", pady=(0, 10))

        btn_del_msg = tk.Button(toolbar, text="🗑️ Delete Selected Message", font=("Helvetica", 9, "bold"), bg="#ef4444", fg="#ffffff", relief="flat", command=self.delete_selected_message, cursor="hand2")
        btn_del_msg.pack(side="right", padx=2)

        self.tree_messages = ttk.Treeview(container, columns=("id", "name", "email", "phone", "subject", "message", "date"), show="headings")
        self.tree_messages.heading("id", text="ID")
        self.tree_messages.heading("name", text="Sender Name")
        self.tree_messages.heading("email", text="Email")
        self.tree_messages.heading("phone", text="Phone")
        self.tree_messages.heading("subject", text="Subject")
        self.tree_messages.heading("message", text="Message Content")
        self.tree_messages.heading("date", text="Received Date")

        self.tree_messages.column("id", width=30, anchor="center")
        self.tree_messages.column("name", width=140)
        self.tree_messages.column("email", width=150)
        self.tree_messages.column("phone", width=110)
        self.tree_messages.column("subject", width=160)
        self.tree_messages.column("message", width=300)
        self.tree_messages.column("date", width=140, anchor="center")

        self.tree_messages.pack(fill="both", expand=True)

    # ---------------- DATA LOADER ----------------
    def load_data(self):
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()

        # Stats
        cursor.execute("SELECT SUM(amount) FROM donations WHERE status IN ('VERIFIED', 'COMPLETED')")
        tot = cursor.fetchone()[0] or 0.0
        self.lbl_stat_total.config(text=f"KES {tot:,.0f}")

        cursor.execute("SELECT SUM(amount) FROM donations WHERE payment_method LIKE 'MPESA%' AND status IN ('VERIFIED', 'COMPLETED')")
        mp = cursor.fetchone()[0] or 0.0
        self.lbl_stat_mpesa.config(text=f"KES {mp:,.0f}")

        cursor.execute("SELECT SUM(amount) FROM donations WHERE payment_method!='MPESA_PAYBILL' AND status IN ('VERIFIED', 'COMPLETED')")
        cd = cursor.fetchone()[0] or 0.0
        self.lbl_stat_card.config(text=f"KES {cd:,.0f}")

        cursor.execute("SELECT COUNT(*) FROM volunteer_signups")
        self.lbl_stat_volunteers.config(text=str(cursor.fetchone()[0]))

        cursor.execute("SELECT COUNT(*) FROM children_projects WHERE type='Child'")
        self.lbl_stat_children.config(text=str(cursor.fetchone()[0]))

        # Donations Ledger
        for item in self.tree_donations.get_children():
            self.tree_donations.delete(item)

        cursor.execute("SELECT * FROM donations ORDER BY id DESC")
        for row in cursor.fetchall():
            self.tree_donations.insert("", "end", values=(
                row["id"],
                row["mpesa_code"] or f"REF-{row['id']}",
                row["donor_name"],
                row["donor_phone"],
                f"{row['amount']:,.2f}",
                row["payment_method"],
                row["cause_title"],
                row["status"],
                row["created_at"]
            ))

        # Activities
        for item in self.tree_activities.get_children():
            self.tree_activities.delete(item)

        cursor.execute("SELECT a.*, COUNT(v.id) as signups FROM activities a LEFT JOIN volunteer_signups v ON a.id=v.activity_id GROUP BY a.id ORDER BY a.id DESC")
        for row in cursor.fetchall():
            self.tree_activities.insert("", "end", values=(
                row["id"], row["title"], row["category"], row["event_date"], row["location"], row["signups"]
            ))

        # Projects
        for item in self.tree_projects.get_children():
            self.tree_projects.delete(item)

        cursor.execute("SELECT * FROM children_projects ORDER BY id DESC")
        for row in cursor.fetchall():
            self.tree_projects.insert("", "end", values=(
                row["id"], row["name"], row["type"], row["age_or_year"], f"{row['raised_amount']:,.0f}", f"{row['target_amount']:,.0f}"
            ))

        # Gallery
        for item in self.tree_gallery.get_children():
            self.tree_gallery.delete(item)

        cursor.execute("SELECT * FROM gallery ORDER BY id DESC")
        for row in cursor.fetchall():
            self.tree_gallery.insert("", "end", values=(
                row["id"], row["title"], row["category"], row["image_url"], row["caption"] or ""
            ))

        # Messages
        for item in self.tree_messages.get_children():
            self.tree_messages.delete(item)

        cursor.execute("SELECT * FROM contact_messages ORDER BY id DESC")
        for row in cursor.fetchall():
            self.tree_messages.insert("", "end", values=(
                row["id"], row["name"], row["email"], row["phone"], row["subject"], row["message"], row["created_at"]
            ))

        conn.close()

    # ---------------- ADVANCED ACTIONS & VOLUNTEER ROSTER ----------------
    def view_registered_volunteers(self):
        selected = self.tree_activities.selection()
        if not selected:
            messagebox.showwarning("Select Event", "Please select an activity from the list to view registered volunteers.")
            return

        item_vals = self.tree_activities.item(selected[0])["values"]
        activity_id = item_vals[0]
        event_title = item_vals[1]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM volunteer_signups WHERE activity_id=? ORDER BY id DESC", (activity_id,))
        vols = cursor.fetchall()
        conn.close()

        v_win = tk.Toplevel(self)
        v_win.title(f"Volunteers Roster — {event_title}")
        v_win.geometry("750x450")
        v_win.configure(bg="#0f172a")

        header_frame = tk.Frame(v_win, bg="#0f172a")
        header_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(header_frame, text=f"Volunteers Roster ({len(vols)} Signed Up)", font=("Helvetica", 13, "bold"), fg="#ffffff", bg="#0f172a").pack(side="left")
        tk.Label(header_frame, text=f"Event: {event_title}", font=("Helvetica", 10), fg="#df5311", bg="#0f172a").pack(side="left", padx=15)

        # Export Volunteer CSV
        def export_vols_csv():
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], initialfile=f"volunteers_{activity_id}.csv")
            if not file_path: return
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Email", "Phone", "Skills/Notes", "Date Signed Up"])
                for v in vols:
                    writer.writerow([v["id"], v["name"], v["email"], v["phone"], v["notes"] or "", v["created_at"]])
            messagebox.showinfo("Exported", f"Volunteers roster saved to:\n{file_path}", parent=v_win)

        btn_exp_vols = tk.Button(header_frame, text="📥 Export Roster CSV", bg="#10b981", fg="#ffffff", font=("Helvetica", 9, "bold"), relief="flat", command=export_vols_csv, cursor="hand2")
        btn_exp_vols.pack(side="right")

        tree_v = ttk.Treeview(v_win, columns=("id", "name", "email", "phone", "notes", "date"), show="headings")
        tree_v.heading("id", text="ID")
        tree_v.heading("name", text="Volunteer Name")
        tree_v.heading("email", text="Email")
        tree_v.heading("phone", text="Phone Number")
        tree_v.heading("notes", text="Notes / Special Skills")
        tree_v.heading("date", text="Date Signed Up")

        tree_v.column("id", width=30, anchor="center")
        tree_v.column("name", width=150)
        tree_v.column("email", width=160)
        tree_v.column("phone", width=120)
        tree_v.column("notes", width=180)
        tree_v.column("date", width=120, anchor="center")

        for v in vols:
            tree_v.insert("", "end", values=(v["id"], v["name"], v["email"], v["phone"], v["notes"] or "-", v["created_at"]))

        tree_v.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def delete_selected_activity(self):
        selected = self.tree_activities.selection()
        if not selected:
            messagebox.showwarning("Select Event", "Please select an activity to delete.")
            return

        activity_id = self.tree_activities.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this event and remove its volunteer signups?"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM activities WHERE id=?", (activity_id,))
            cursor.execute("DELETE FROM volunteer_signups WHERE activity_id=?", (activity_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Event removed successfully!")
            self.load_data()

    def delete_selected_project(self):
        selected = self.tree_projects.selection()
        if not selected:
            messagebox.showwarning("Select Profile", "Please select a child/project profile to delete.")
            return

        proj_id = self.tree_projects.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm Delete", "Delete this child/project profile?"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM children_projects WHERE id=?", (proj_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Profile removed successfully!")
            self.load_data()

    def delete_selected_donation(self):
        selected = self.tree_donations.selection()
        if not selected:
            messagebox.showwarning("Select Donation", "Please select a donation record to delete.")
            return

        don_id = self.tree_donations.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm Delete", "Delete this donation entry from the ledger?"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM donations WHERE id=?", (don_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Donation record deleted!")
            self.load_data()

    def delete_selected_gallery(self):
        selected = self.tree_gallery.selection()
        if not selected:
            messagebox.showwarning("Select Photo", "Please select a photo to delete.")
            return

        gal_id = self.tree_gallery.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm Delete", "Delete this photo from website gallery?"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM gallery WHERE id=?", (gal_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Photo removed!")
            self.load_data()

    def delete_selected_message(self):
        selected = self.tree_messages.selection()
        if not selected:
            messagebox.showwarning("Select Message", "Please select a message to delete.")
            return

        msg_id = self.tree_messages.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm Delete", "Delete this inquiry message?"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contact_messages WHERE id=?", (msg_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Message deleted!")
            self.load_data()

    def filter_donations(self, event=None):
        query = self.entry_search.get().lower()
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor()

        for item in self.tree_donations.get_children():
            self.tree_donations.delete(item)

        cursor.execute("SELECT * FROM donations ORDER BY id DESC")
        for row in cursor.fetchall():
            code = (row["mpesa_code"] or "").lower()
            name = row["donor_name"].lower()
            cause = row["cause_title"].lower()

            if query in code or query in name or query in cause:
                self.tree_donations.insert("", "end", values=(
                    row["id"],
                    row["mpesa_code"] or f"REF-{row['id']}",
                    row["donor_name"],
                    row["donor_phone"],
                    f"{row['amount']:,.2f}",
                    row["payment_method"],
                    row["cause_title"],
                    row["status"],
                    row["created_at"]
                ))

        conn.close()

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], initialfile="boc_donations_ledger.csv")
        if not file_path:
            return

        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor()
        cursor.execute("SELECT id, donor_name, donor_email, donor_phone, amount, payment_method, mpesa_code, cause_title, status, created_at FROM donations ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Donor Name", "Email", "Phone", "Amount (KES)", "Method", "M-Pesa Ref", "Cause", "Status", "Timestamp"])
            for r in rows:
                writer.writerow([r["id"], r["donor_name"], r["donor_email"], r["donor_phone"], r["amount"], r["payment_method"], r["mpesa_code"] or "", r["cause_title"], r["status"], r["created_at"]])

        messagebox.showinfo("Export Successful", f"Donations ledger exported successfully to:\n{file_path}")

    def modal_add_offline_donation(self):
        win = tk.Toplevel(self)
        win.title("Record Cash / Bank Donation")
        win.geometry("380x380")
        win.configure(bg="#ffffff")

        tk.Label(win, text="Donor Name:", bg="#ffffff").pack(anchor="w", padx=20, pady=(15, 0))
        e_name = tk.Entry(win, width=35)
        e_name.pack(padx=20, pady=2)

        tk.Label(win, text="Phone Number:", bg="#ffffff").pack(anchor="w", padx=20, pady=(5, 0))
        e_phone = tk.Entry(win, width=35)
        e_phone.pack(padx=20, pady=2)

        tk.Label(win, text="Amount (KES):", bg="#ffffff").pack(anchor="w", padx=20, pady=(5, 0))
        e_amount = tk.Entry(win, width=35, font=("Helvetica", 10, "bold"))
        e_amount.pack(padx=20, pady=2)

        tk.Label(win, text="Payment Type:", bg="#ffffff").pack(anchor="w", padx=20, pady=(5, 0))
        cb_type = ttk.Combobox(win, values=["OFFLINE", "BANK_TRANSFER", "CHEQUE"], width=33)
        cb_type.set("OFFLINE")
        cb_type.pack(padx=20, pady=2)

        tk.Label(win, text="Cause / Target:", bg="#ffffff").pack(anchor="w", padx=20, pady=(5, 0))
        e_cause = tk.Entry(win, width=35)
        e_cause.insert(0, "General Children Care & Nutrition")
        e_cause.pack(padx=20, pady=2)

        def save():
            try:
                amt = float(e_amount.get())
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO donations (donor_name, donor_phone, amount, payment_method, cause_title, status)
                    VALUES (?, ?, ?, ?, ?, 'VERIFIED')
                ''', (e_name.get() or 'Cash Donor', e_phone.get() or '', amt, cb_type.get(), e_cause.get()))
                cursor.execute("UPDATE children_projects SET raised_amount = raised_amount + ? WHERE name = ?", (amt, e_cause.get()))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Offline donation recorded successfully!")
                win.destroy()
                self.load_data()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid numeric amount.")

        btn = tk.Button(win, text="SAVE DONATION", bg="#10b981", fg="#ffffff", font=("Helvetica", 10, "bold"), relief="flat", command=save, cursor="hand2")
        btn.pack(padx=20, pady=20, fill="x")

    def save_activity(self):
        title = self.act_title.get()
        if not title:
            messagebox.showwarning("Warning", "Title is required!")
            return
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO activities (title, category, event_date, location, description, image_url)
            VALUES (?, ?, ?, ?, ?, 'https://bodyofchristcentre.co.ke/wp-content/uploads/2024/01/event-2.jpg')
        ''', (title, self.act_cat.get(), self.act_date.get(), self.act_loc.get(), self.act_desc.get("1.0", tk.END).strip()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Activity published successfully!")
        self.load_data()

    def save_project(self):
        name = self.proj_name.get()
        if not name:
            messagebox.showwarning("Warning", "Name is required!")
            return
        try:
            target = float(self.proj_target.get())
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO children_projects (name, type, age_or_year, description, target_amount, image_url)
                VALUES (?, ?, ?, ?, ?, 'https://bodyofchristcentre.co.ke/wp-content/uploads/2024/01/event-5.jpg')
            ''', (name, self.proj_type.get(), self.proj_year.get(), self.proj_desc.get("1.0", tk.END).strip(), target))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Profile target added successfully!")
            self.load_data()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric target amount.")

    def save_gallery_photo(self):
        title = self.gal_title.get()
        url = self.gal_url.get()
        if not title or not url:
            messagebox.showwarning("Warning", "Photo title and Image URL are required!")
            return
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO gallery (title, category, image_url, caption)
            VALUES (?, ?, ?, ?)
        ''', (title, self.gal_cat.get(), url, self.gal_caption.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Photo added to website gallery!")
        self.load_data()

if __name__ == "__main__":
    try:
        app = BOCAdminApp()
        app.mainloop()
    except KeyboardInterrupt:
        sys.exit(0)
