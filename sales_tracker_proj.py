import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta

# Advanced required packages for visualization and PDF printing
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# ==========================================
# 1. DATABASE MANAGEMENT & INITIALIZATION
# ==========================================
DB_NAME = "msme_sales.db"


def init_database():
    """Initializes the SQLite local database and seeds it with sample data if empty."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            gender TEXT NOT NULL,
            status TEXT NOT NULL,
            contact_info TEXT NOT NULL,
            created_date DATE NOT NULL,
            amount REAL NOT NULL
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM records")
    if cursor.fetchone()[0] == 0:
        base_date = datetime.now()
        sample_data = [
            ("Mariama Kallon", "Female", "Active", "+232-77-123456",
             (base_date - timedelta(days=2)).strftime('%Y-%m-%d'), 450.0),
            ("John Kamara", "Male", "Active", "+232-30-987654", (base_date - timedelta(days=5)).strftime('%Y-%m-%d'),
             1200.0),
            ("Fatmata Fofanah", "Female", "Pending", "+232-88-234567",
             (base_date - timedelta(days=12)).strftime('%Y-%m-%d'), 300.0),
            ("Samuel Bangura", "Male", "Inactive", "+232-76-345678",
             (base_date - timedelta(days=45)).strftime('%Y-%m-%d'), 850.0),
            ("Zainab Sesay", "Female", "Active", "+232-99-456789", (base_date - timedelta(days=1)).strftime('%Y-%m-%d'),
             150.0),
            ("Alhaji Conteh", "Male", "Active", "+232-77-567890", (base_date - timedelta(days=20)).strftime('%Y-%m-%d'),
             2100.0),
            ("Sia Mansaray", "Female", "Pending", "+232-33-678901",
             (base_date - timedelta(days=3)).strftime('%Y-%m-%d'), 95.0),
            ("Emmanuel Koroma", "Male", "Active", "+232-78-789012",
             (base_date - timedelta(days=8)).strftime('%Y-%m-%d'), 600.0),
            ("Bintu Turay", "Female", "Active", "+232-88-890123", (base_date - timedelta(days=32)).strftime('%Y-%m-%d'),
             1350.0),
            ("Mohamed Jalloh", "Male", "Inactive", "+232-76-901234",
             (base_date - timedelta(days=60)).strftime('%Y-%m-%d'), 500.0),
            ("Rebecca Dumbuya", "Female", "Active", "+232-30-112233",
             (base_date - timedelta(days=4)).strftime('%Y-%m-%d'), 420.0),
            ("Osman Kargbo", "Male", "Pending", "+232-77-445566", (base_date - timedelta(days=15)).strftime('%Y-%m-%d'),
             75.0),
            ("Grace Kanu", "Female", "Active", "+232-88-778899", (base_date - timedelta(days=18)).strftime('%Y-%m-%d'),
             110.0),
            ("Sahr Gando", "Male", "Active", "+232-99-223344", (base_date - timedelta(days=25)).strftime('%Y-%m-%d'),
             900.0),
            ("Aminata Barrie", "Female", "Inactive", "+232-33-556677",
             (base_date - timedelta(days=90)).strftime('%Y-%m-%d'), 1750.0),
            ("Peter Mansaray", "Male", "Active", "+232-76-889900", (base_date - timedelta(days=6)).strftime('%Y-%m-%d'),
             230.0),
            ("Kadiatu Bangura", "Female", "Active", "+232-77-114477",
             (base_date - timedelta(days=29)).strftime('%Y-%m-%d'), 310.0),
            ("Mustapha Cole", "Male", "Pending", "+232-30-552288", (base_date - timedelta(days=7)).strftime('%Y-%m-%d'),
             400.0),
            ("Lucy Tarawallie", "Female", "Active", "+232-88-993311",
             (base_date - timedelta(days=14)).strftime('%Y-%m-%d'), 125.0),
            ("Prince Williams", "Male", "Active", "+232-78-441199",
             (base_date - timedelta(days=22)).strftime('%Y-%m-%d'), 800.0)
        ]
        cursor.executemany('''
            INSERT INTO records (full_name, gender, status, contact_info, created_date, amount)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_data)
        conn.commit()
    conn.close()


# ==========================================
# 2. USER AUTHENTICATION MODULE (LOGIN)
# ==========================================
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("System Authorization - Login")
        self.root.geometry("400x320")
        self.root.configure(bg="#1e293b")
        self.root.resizable(False, False)

        tk.Label(root, text="SME Core Portal Auth", font=("Tahoma", 16, "bold"), fg="#ffffff", bg="#1e293b").pack(
            pady=20)

        frame_form = tk.Frame(root, bg="#1e293b")
        frame_form.pack(fill="x", padx=40)

        tk.Label(frame_form, text="Username / Email:", font=("Tahoma", 10), fg="#cbd5e1", bg="#1e293b").pack(anchor="w",
                                                                                                             pady=(5,
                                                                                                                   2))
        self.entry_user = tk.Entry(frame_form, font=("Tahoma", 11))
        self.entry_user.pack(fill="x", pady=2)
        self.entry_user.insert(0, "admin")

        tk.Label(frame_form, text="Password:", font=("Tahoma", 10), fg="#cbd5e1", bg="#1e293b").pack(anchor="w",
                                                                                                     pady=(10, 2))
        self.entry_pass = tk.Entry(frame_form, font=("Tahoma", 11), show="*")
        self.entry_pass.pack(fill="x", pady=2)
        self.entry_pass.insert(0, "admin123")

        btn_login = tk.Button(root, text="Secure Sign In", font=("Tahoma", 11, "bold"), bg="#10b981", fg="white",
                              command=self.handle_auth, height=1)
        btn_login.pack(fill="x", padx=40, pady=20)

        lbl_forgot = tk.Label(root, text="Forgot Password?", font=("Tahoma", 9, "underline"), fg="#94a3b8",
                              bg="#1e293b", cursor="hand2")
        lbl_forgot.pack()
        lbl_forgot.bind("<Button-1>", lambda e: messagebox.showinfo("Recovery",
                                                                    "Password recovery template: Contact IT System Administrator."))

    def handle_auth(self):
        user = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if user == "admin" and password == "admin123":
            self.root.destroy()
            launch_main_dashboard()
        else:
            messagebox.showerror("Auth Error", "Invalid Username or Password credential set!")


# ==========================================
# 3. CORE ANALYTICAL DASHBOARD MANAGEMENT
# ==========================================
class MainDashboard:
    def __init__(self, window):
        self.window = window
        self.window.title("SME Digital Public Service Dashboard")
        self.window.geometry("1100x700")
        self.window.minsize(1000, 650)
        self.window.configure(bg="#f4f6f9")

        self.setup_ui_layout()
        self.load_data_from_db()

    def setup_ui_layout(self):
        frame_banner = tk.Frame(self.window, bg="#1e293b")
        frame_banner.pack(fill="x", padx=15, pady=15)

        lbl_title = tk.Label(frame_banner, text="National MSME Analytical Hub", font=("Tahoma", 16, "bold"),
                             fg="#ffffff", bg="#1e293b")
        lbl_title.pack(pady=(5, 2))
        lbl_sub = tk.Label(frame_banner,
                           text="Structured Architecture Framework Compliance Dashboard • SDG 8 Solution Engine",
                           font=("Tahoma", 9, "italic"), fg="#94a3b8", bg="#1e293b")
        lbl_sub.pack(pady=(0, 5))

        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.tab_records = tk.Frame(notebook, bg="#f4f6f9")
        self.tab_charts = tk.Frame(notebook, bg="#f4f6f9")
        self.tab_reports = tk.Frame(notebook, bg="#f4f6f9")

        notebook.add(self.tab_records, text=" Records Database Module ")
        notebook.add(self.tab_charts, text=" Data Visualization Insights ")
        notebook.add(self.tab_reports, text=" PDF Report Generation ")

        # --- SUB-MODULE A: RECORDS MANAGER DATA SHEET TAB UI ---
        frame_search_filter = tk.LabelFrame(self.tab_records, text=" Query Search & Dynamic Filtering Filters ",
                                            font=("Tahoma", 9, "bold"), bg="#ffffff")
        frame_search_filter.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_search_filter, text="Search (Name/ID):", bg="#ffffff").grid(row=0, column=0, padx=5, pady=5,
                                                                                   sticky="w")
        self.var_search = tk.StringVar()
        self.entry_search = tk.Entry(frame_search_filter, textvariable=self.var_search, width=20)
        self.entry_search.grid(row=0, column=1, padx=5, pady=5)
        self.var_search.trace_add("write", lambda *args: self.load_data_from_db())

        tk.Label(frame_search_filter, text="Gender:", bg="#ffffff").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.combo_gender = ttk.Combobox(frame_search_filter, values=["All", "Male", "Female"], width=10,
                                         state="readonly")
        self.combo_gender.current(0)
        self.combo_gender.grid(row=0, column=3, padx=5, pady=5)
        self.combo_gender.bind("<<ComboboxSelected>>", lambda e: self.load_data_from_db())

        tk.Label(frame_search_filter, text="Status:", bg="#ffffff").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.combo_status = ttk.Combobox(frame_search_filter, values=["All", "Active", "Inactive", "Pending"], width=10,
                                         state="readonly")
        self.combo_status.current(0)
        self.combo_status.grid(row=0, column=5, padx=5, pady=5)
        self.combo_status.bind("<<ComboboxSelected>>", lambda e: self.load_data_from_db())

        tk.Label(frame_search_filter, text="Date Interval:", bg="#ffffff").grid(row=0, column=6, padx=5, pady=5,
                                                                                sticky="w")
        self.combo_date = ttk.Combobox(frame_search_filter, values=["All Time", "Daily", "Weekly", "Monthly", "Yearly"],
                                       width=10, state="readonly")
        self.combo_date.current(0)
        self.combo_date.grid(row=0, column=7, padx=5, pady=5)
        self.combo_date.bind("<<ComboboxSelected>>", lambda e: self.load_data_from_db())

        frame_table_box = tk.Frame(self.tab_records)
        frame_table_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        cols = ("id", "name", "gender", "status", "contact", "date", "amount")
        self.record_table = ttk.Treeview(frame_table_box, columns=cols, show="headings")

        self.record_table.heading("id", text="Record ID")
        self.record_table.heading("name", text="Full Name")
        self.record_table.heading("gender", text="Gender")
        self.record_table.heading("status", text="Status")
        self.record_table.heading("contact", text="Contact Info")
        self.record_table.heading("date", text="Date Created")
        self.record_table.heading("amount", text="Value (Le)")

        for col in cols:
            self.record_table.column(col, anchor="center" if col != "name" else "w")

        scrollbar = ttk.Scrollbar(frame_table_box, orient="vertical", command=self.record_table.yview)
        self.record_table.configure(yscrollcommand=scrollbar.set)
        self.record_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- SUB-MODULE B: DATA VISUALIZATION TAB DESIGN ---
        self.frame_chart_canvas = tk.Frame(self.tab_charts, bg="#ffffff")
        self.frame_chart_canvas.pack(fill="both", expand=True, padx=15, pady=15)

        btn_refresh_charts = tk.Button(self.tab_charts, text="🔄 Recompute Graphs Analytics",
                                       font=("Tahoma", 10, "bold"), bg="#1e293b", fg="white",
                                       command=self.render_visualization_graphs)
        btn_refresh_charts.pack(pady=10)

        # --- SUB-MODULE C: PDF DOCUMENT REPORT TAB ---
        frame_pdf_control = tk.LabelFrame(self.tab_reports, text=" Compile Hardcopy Documentation Ledger ",
                                          font=("Tahoma", 10, "bold"), bg="#ffffff")
        frame_pdf_control.pack(anchor="center", padx=20, pady=20)

        tk.Label(frame_pdf_control, text="Select Report Target Interval Timeline Window:", font=("Tahoma", 10),
                 bg="#ffffff").pack(anchor="w", pady=5)
        self.combo_report_type = ttk.Combobox(frame_pdf_control,
                                              values=["Weekly Report", "Monthly Report", "Yearly Report"],
                                              state="readonly", font=("Tahoma", 11), width=25)
        self.combo_report_type.current(1)
        self.combo_report_type.pack(pady=10)

        btn_generate_pdf = tk.Button(frame_pdf_control, text="📥 Generate Compliant PDF Report",
                                     font=("Tahoma", 11, "bold"), bg="#10b981", fg="white",
                                     command=self.compile_pdf_document, height=2)
        btn_generate_pdf.pack(fill="x", pady=10)

    def load_data_from_db(self):
        for item in self.record_table.get_children():
            self.record_table.delete(item)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        query = "SELECT id, full_name, gender, status, contact_info, created_date, amount FROM records WHERE 1=1"
        params = []

        search_val = self.var_search.get().strip()
        if search_val:
            query += " AND (full_name LIKE ? OR id LIKE ?)"
            params.extend([f"%{search_val}%", f"%{search_val}%"])

        gender_val = self.combo_gender.get()
        if gender_val != "All":
            query += " AND gender = ?"
            params.append(gender_val)

        status_val = self.combo_status.get()
        if status_val != "All":
            query += " AND status = ?"
            params.append(status_val)

        date_filter = self.combo_date.get()
        now_date = datetime.now()
        if date_filter == "Daily":
            query += " AND created_date = ?"
            params.append(now_date.strftime('%Y-%m-%d'))
        elif date_filter == "Weekly":
            start_week = (now_date - timedelta(days=7)).strftime('%Y-%m-%d')
            query += " AND created_date >= ?"
            params.append(start_week)
        elif date_filter == "Monthly":
            start_month = (now_date - timedelta(days=30)).strftime('%Y-%m-%d')
            query += " AND created_date >= ?"
            params.append(start_month)
        elif date_filter == "Yearly":
            start_year = (now_date - timedelta(days=365)).strftime('%Y-%m-%d')
            query += " AND created_date >= ?"
            params.append(start_year)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        for row in rows:
            self.record_table.insert("", "end", values=row)
        conn.close()

    def render_visualization_graphs(self):
        for widget in self.frame_chart_canvas.winfo_children():
            widget.destroy()

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT status, COUNT(*) FROM records GROUP BY status")
        status_counts = dict(cursor.fetchall())

        cursor.execute("SELECT gender, COUNT(*) FROM records GROUP BY gender")
        gender_counts = dict(cursor.fetchall())

        cursor.execute(
            "SELECT strftime('%W', created_date) as wk, COUNT(*) FROM records GROUP BY wk ORDER BY wk DESC LIMIT 5")
        timeline_counts = cursor.fetchall()
        conn.close()

        statuses = ["Active", "Pending", "Inactive"]
        status_vals = [status_counts.get(s, 0) for s in statuses]

        genders = ["Male", "Female"]
        gender_vals = [gender_counts.get(g, 0) for g in genders]

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 4))
        fig.patch.set_facecolor('#ffffff')

        ax1.bar(statuses, status_vals, color=['#10b981', '#f59e0b', '#ef4444'])
        ax1.set_title("Records by Status", fontname="Tahoma", fontsize=10, fontweight="bold")
        ax1.grid(axis='y', linestyle='--', alpha=0.5)

        ax2.pie(gender_vals, labels=genders, autopct='%1.1f%%', colors=['#3b82f6', '#ec4899'], startangle=90)
        ax2.set_title("Gender Metrics Split", fontname="Tahoma", fontsize=10, fontweight="bold")

        if timeline_counts:
            weeks = [f"Wk {x[0]}" for x in reversed(timeline_counts)]
            counts = [x[1] for x in reversed(timeline_counts)]
            ax3.plot(weeks, counts, marker='o', color='#6366f1', linewidth=2)
        else:
            ax3.plot(["Start"], [0], marker='o')
        ax3.set_title("Weekly Registration Trends", fontname="Tahoma", fontsize=10, fontweight="bold")
        ax3.grid(True, linestyle='--', alpha=0.5)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_chart_canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def compile_pdf_document(self):
        report_scope = self.combo_report_type.get()
        target_filename = f"SME_{report_scope.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"

        now = datetime.now()
        if "Weekly" in report_scope:
            days_back = 7
        elif "Monthly" in report_scope:
            days_back = 30
        else:
            days_back = 365

        start_date_boundary = (now - timedelta(days=days_back)).strftime('%Y-%m-%d')

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, full_name, gender, status, created_date, amount 
            FROM records 
            WHERE created_date >= ? 
            ORDER BY created_date DESC
        ''', (start_date_boundary,))
        records_subset = cursor.fetchall()
        conn.close()

        doc = SimpleDocTemplate(target_filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40,
                                bottomMargin=40)
        story = []
        styles = getSampleStyleSheet()

        title_style = styles['Heading1']
        title_style.fontName = 'Helvetica-Bold'
        title_style.textColor = colors.HexColor("#1e293b")

        story.append(Paragraph(f"Public Service Management Report - {report_scope}", title_style))
        story.append(Spacer(1, 12))

        meta_text = f"<b>Generated Date:</b> {now.strftime('%Y-%m-%d %H:%M:%S')}<br/>" \
                    f"<b>Reporting Date Window Range:</b> {start_date_boundary} to {now.strftime('%Y-%m-%d')}<br/>" \
                    f"<b>Total Evaluated Records Volume:</b> {len(records_subset)}"
        story.append(Paragraph(meta_text, styles['Normal']))
        story.append(Spacer(1, 20))

        table_data = [["ID", "Full Name", "Gender", "Status", "Date Created", "Amount Value"]]
        for item in records_subset:
            table_data.append([str(item[0]), item[1], item[2], item[3], item[4], f"Le {item[5]:,.2f}"])

        report_table = Table(table_data, colWidths=[40, 150, 70, 70, 90, 90])
        report_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))

        story.append(report_table)

        try:
            doc.build(story)
            messagebox.showinfo("PDF Created", f"Report saved to:\n{os.path.abspath(target_filename)}")
        except Exception as err:
            messagebox.showerror("Export Error", f"The PDF compiler ran into an issue:\n{str(err)}")


def launch_main_dashboard():
    main_window = tk.Tk()
    app = MainDashboard(main_window)
    main_window.mainloop()


if __name__ == "__main__":
    init_database()
    auth_root = tk.Tk()
    login_system = LoginWindow(auth_root)
    auth_root.mainloop()