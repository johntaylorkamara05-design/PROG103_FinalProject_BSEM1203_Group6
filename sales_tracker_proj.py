import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ==========================================
# 1. DATABASE INITIALIZATION & SCHEMA SETUP
# ==========================================
def init_database():
    conn = sqlite3.connect("msme_sales.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS msme_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            status TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM msme_records")
    if cursor.fetchone()[0] == 0:
        sample_data = [
            ("Mariama Kallon", "Female", "Active", "+232-77-123456"),
            ("John Kamara", "Male", "Active", "+232-30-987654"),
            ("Fatmata Fofanah", "Female", "Pending", "+232-88-234567"),
            ("Samuel Bangura", "Male", "Inactive", "+232-76-345678"),
            ("Zainab Sesay", "Female", "Active", "+232-99-456789"),
            ("Alhaji Conteh", "Male", "Active", "+232-77-567890"),
            ("Sia Mansaray", "Female", "Pending", "+232-33-678901"),
            ("Emmanuel Koroma", "Male", "Active", "+232-78-789012"),
            ("Bintu Turay", "Female", "Active", "+232-88-890123"),
            ("Mohamed Jalloh", "Male", "Inactive", "+232-76-901234"),
            ("Rebecca Dumbuya", "Female", "Active", "+232-30-112233"),
            ("Osman Kargbo", "Male", "Pending", "+232-77-445566"),
            ("Grace Kanu", "Female", "Active", "+232-88-778899"),
            ("Sahr Gando", "Male", "Active", "+232-99-223344"),
            ("Aminata Barrie", "Female", "Inactive", "+232-33-556677"),
            ("Peter Mansaray", "Male", "Active", "+232-76-889900"),
            ("Kadiatu Bangura", "Female", "Active", "+232-77-114477"),
            ("Mustapha Cole", "Male", "Pending", "+232-30-552288"),
            ("Lucy Tarawallie", "Female", "Active", "+232-88-993311"),
            ("Prince Williams", "Male", "Active", "+232-76-441199")
        ]
        cursor.executemany("INSERT INTO msme_records (name, gender, status, contact) VALUES (?, ?, ?, ?)", sample_data)
        conn.commit()
    conn.close()


# ==========================================
# 2. APPLICATION LOGIN CONTROLLER
# ==========================================
def login_verify():
    username = entry_user.get()
    password = entry_pass.get()

    if username == "admin" and password == "admin123":
        login_window.destroy()
        launch_dashboard()
    else:
        messagebox.showerror("Access Denied", "Invalid Administrative Credentials.")


# ==========================================
# 3. CORE FINANCIAL CALCULATOR (P&L LOGIC)
# ==========================================
def process_financial_performance():
    try:
        sales = float(entry_sales.get())
        expenses = float(entry_expenses.get())
        net_margin = sales - expenses

        if net_margin > 0:
            result_text = f"Profit Attained: +Le {net_margin:,.2f}"
            lbl_financial_result.config(text=result_text, fg="#107C41")
        elif net_margin < 0:
            result_text = f"Loss Recorded: -Le {abs(net_margin):,.2f}"
            lbl_financial_result.config(text=result_text, fg="#A80000")
        else:
            result_text = "Operational Balance: Break-even (Le 0.00)"
            lbl_financial_result.config(text=result_text, fg="#242424")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values for Sales and Expenses.")


# ==========================================
# 4. DATABASE QUERIES & DYNAMIC FILTERING
# ==========================================
def refresh_table_view(event=None):
    for item in tree.get_children():
        tree.delete(item)

    search_query = entry_search.get().strip()
    gender_filter = combo_gender.get()
    status_filter = combo_status.get()

    conn = sqlite3.connect("msme_sales.db")
    cursor = conn.cursor()

    query = "SELECT * FROM msme_records WHERE 1=1"
    params = []

    if search_query:
        query += " AND (name LIKE ? OR id LIKE ?)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])
    if gender_filter != "All":
        query += " AND gender = ?"
        params.append(gender_filter)
    if status_filter != "All":
        query += " AND status = ?"
        params.append(status_filter)

    cursor.execute(query, params)
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()


# ==========================================
# 5. MATPLOTLIB LIVE GRAPH DATA INJECTION
# ==========================================
def render_charts():
    for widget in frame_charts_container.winfo_children():
        widget.destroy()

    conn = sqlite3.connect("msme_sales.db")
    cursor = conn.cursor()
    cursor.execute("SELECT status, COUNT(*) FROM msme_records GROUP BY status")
    status_data = dict(cursor.fetchall())
    cursor.execute("SELECT gender, COUNT(*) FROM msme_records GROUP BY gender")
    gender_data = dict(cursor.fetchall())
    conn.close()

    # Defaults for empty sets
    for s in ["Active", "Pending", "Inactive"]: status_data.setdefault(s, 0)
    for g in ["Male", "Female"]: gender_data.setdefault(g, 0)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(11, 4), dpi=100)
    fig.tight_layout(pad=3.5)

    # 1. Bar Chart
    ax1.bar(["Active", "Pending", "Inactive"], [status_data["Active"], status_data["Pending"], status_data["Inactive"]],
            color=["#107C41", "#F39C12", "#E74C3C"])
    ax1.set_title("Records by Status", fontsize=10, fontweight='bold', fontname='Segoe UI')
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    ax1.tick_params(labelsize=9)

    # 2. Pie Chart
    ax2.pie([gender_data.get("Male", 0), gender_data.get("Female", 0)], labels=["Male", "Female"], autopct='%1.1f%%',
            startangle=90, colors=["#3B82F6", "#EC4899"])
    ax2.set_title("Gender Metrics Split", fontsize=10, fontweight='bold', fontname='Segoe UI')

    # 3. Line Graph
    ax3.plot(["Wk 20", "Wk 21", "Wk 22", "Wk 23", "Wk 24"], [2, 2, 4, 3, 6], marker='o', color='#6366F1', linewidth=2)
    ax3.set_title("Weekly Registration Trends", fontsize=10, fontweight='bold', fontname='Segoe UI')
    ax3.grid(linestyle='--', alpha=0.5)
    ax3.tick_params(labelsize=9)

    canvas = FigureCanvasTkAgg(fig, master=frame_charts_container)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# ==========================================
# 6. MAIN APP INTERFACE CANVAS LAYOUT
# ==========================================
def launch_dashboard():
    global tree, entry_search, combo_gender, combo_status, entry_sales, entry_expenses, lbl_financial_result, frame_charts_container

    main_window = tk.Tk()
    main_window.title("SME Digital Public Service Dashboard")
    main_window.geometry("1020x650")

    # Beautiful Deep Blue Corporate Header Panel
    header_frame = tk.Frame(main_window, bg="#1E293B", height=70)
    header_frame.pack(fill=tk.X, side=tk.TOP)
    header_frame.pack_propagate(False)

    lbl_title = tk.Label(header_frame, text="National MSME Analytical Hub", font=("Segoe UI", 16, "bold"), fg="white",
                         bg="#1E293B")
    lbl_title.pack(pady=(8, 2))
    lbl_subtitle = tk.Label(header_frame,
                            text="Structured Architecture Framework Compliance Dashboard • SDG 8 Solution Engine",
                            font=("Segoe UI", 9, "italic"), fg="#94A3B8", bg="#1E293B")
    lbl_subtitle.pack()

    # Notebook Tabs Structure
    style = ttk.Style()
    style.configure("TNotebook.Tab", font=("Segoe UI", 9), padding=[8, 4])
    notebook = ttk.Notebook(main_window)
    notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    # ---- TAB 1: DIRECTORY MODULE ----
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Records Database Module")

    # Filters Bar Frame Layout
    filter_frame = ttk.LabelFrame(tab1, text=" Query Search & Dynamic Filtering Filters ")
    filter_frame.pack(fill=tk.X, padx=10, pady=10, ipady=5)

    tk.Label(filter_frame, text="Search (Name/ID):", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(10, 2))
    entry_search = tk.Entry(filter_frame, font=("Segoe UI", 9), width=15)
    entry_search.pack(side=tk.LEFT, padx=5)
    entry_search.bind("<KeyRelease>", refresh_table_view)

    tk.Label(filter_frame, text="Gender:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(15, 2))
    combo_gender = ttk.Combobox(filter_frame, values=["All", "Male", "Female"], state="readonly", width=8)
    combo_gender.set("All")
    combo_gender.pack(side=tk.LEFT, padx=5)
    combo_gender.bind("<<ComboboxSelected>>", refresh_table_view)

    tk.Label(filter_frame, text="Status:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(15, 2))
    combo_status = ttk.Combobox(filter_frame, values=["All", "Active", "Pending", "Inactive"], state="readonly",
                                width=10)
    combo_status.set("All")
    combo_status.pack(side=tk.LEFT, padx=5)
    combo_status.bind("<<ComboboxSelected>>", refresh_table_view)

    tk.Label(filter_frame, text="Date Interval:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(15, 2))
    combo_date = ttk.Combobox(filter_frame, values=["All Time"], state="readonly", width=10)
    combo_date.set("All Time")
    combo_date.pack(side=tk.LEFT, padx=5)

    # Clean Grid View Representation Layout
    tree_frame = tk.Frame(tab1)
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Gender", "Status", "Contact"), show="headings")
    tree.heading("ID", text="Record ID")
    tree.heading("Name", text="Full Name")
    tree.heading("Gender", text="Gender")
    tree.heading("Status", text="Status")
    tree.heading("Contact", text="Contact Info")

    tree.column("ID", width=80, anchor=tk.CENTER)
    tree.column("Name", width=220, anchor=tk.W)
    tree.column("Gender", width=130, anchor=tk.CENTER)
    tree.column("Status", width=120, anchor=tk.CENTER)
    tree.column("Contact", width=180, anchor=tk.W)

    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # ---- TAB 2: ANALYTICS VISUALIZATION ----
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Data Visualization Insights")

    frame_charts_container = tk.Frame(tab2)
    frame_charts_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    btn_recompute = tk.Button(tab2, text="🔄 Recompute Graphs Analytics", command=render_charts, bg="#1E293B",
                              fg="white", font=("Segoe UI", 9, "bold"), padx=10, pady=4)
    btn_recompute.pack(pady=10)

    # ---- TAB 3: PROFIT & LOSS CALCULATOR ENGINE ----
    tab3 = ttk.Frame(notebook)
    notebook.add(tab3, text="Business Profitability Calculator")

    calc_frame = ttk.LabelFrame(tab3, text=" Financial Audit Processing Terminal ")
    calc_frame.pack(padx=30, pady=30, fill=tk.BOTH, expand=True)

    lbl_calc_desc = tk.Label(calc_frame,
                             text="Enter financial tracking variables to evaluate operational margin profiles:",
                             font=("Segoe UI", 10, "italic"), fg="#475569")
    lbl_calc_desc.pack(pady=20)

    form_grid = tk.Frame(calc_frame)
    form_grid.pack(pady=10)

    tk.Label(form_grid, text="Total Monthly Sales Revenue: Le ", font=("Segoe UI", 11, "bold")).grid(row=0, column=0,
                                                                                                     sticky=tk.E,
                                                                                                     pady=15)
    entry_sales = tk.Entry(form_grid, font=("Segoe UI", 11), width=22)
    entry_sales.grid(row=0, column=1, pady=15)

    tk.Label(form_grid, text="Total Operating Expenditures: Le ", font=("Segoe UI", 11, "bold")).grid(row=1, column=0,
                                                                                                      sticky=tk.E,
                                                                                                      pady=15)
    entry_expenses = tk.Entry(form_grid, font=("Segoe UI", 11), width=22)
    entry_expenses.grid(row=1, column=1, pady=15)

    btn_calc = tk.Button(calc_frame, text="Execute P&L Calculation", command=process_financial_performance,
                         bg="#107C41", fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=6)
    btn_calc.pack(pady=25)

    lbl_financial_result = tk.Label(calc_frame, text="Awaiting Financial Entry Sequences...",
                                    font=("Segoe UI", 14, "bold"), fg="#475569")
    lbl_financial_result.pack(pady=10)

    # Initialize view strings and generate matplotlib graphs
    refresh_table_view()
    render_charts()
    main_window.mainloop()


# ==========================================
# 7. HIGH-FIDELITY LOGIN DIALOG WINDOW
# ==========================================
if __name__ == "__main__":
    init_database()

    login_window = tk.Tk()
    login_window.title("System Authorization - Login")
    login_window.geometry("380x280")
    login_window.configure(bg="#1E293B")  # Matched Dark Canvas Background
    login_window.resizable(False, False)

    tk.Label(login_window, text="SME Core Portal Auth", font=("Segoe UI", 16, "bold"), fg="white", bg="#1E293B").pack(
        pady=(25, 20))

    fields_frame = tk.Frame(login_window, bg="#1E293B")
    fields_frame.pack(pady=5)

    tk.Label(fields_frame, text="Username / Email:", font=("Segoe UI", 10, "bold"), fg="#94A3B8", bg="#1E293B").grid(
        row=0, column=0, sticky=tk.W, pady=5)
    entry_user = tk.Entry(fields_frame, font=("Segoe UI", 11), width=26)
    entry_user.grid(row=1, column=0, pady=(2, 10))
    entry_user.insert(0, "admin")  # Convenience default injection

    tk.Label(fields_frame, text="Password:", font=("Segoe UI", 10, "bold"), fg="#94A3B8", bg="#1E293B").grid(row=2,
                                                                                                             column=0,
                                                                                                             sticky=tk.W,
                                                                                                             pady=5)
    entry_pass = tk.Entry(fields_frame, font=("Segoe UI", 11), width=26, show="*")
    entry_pass.grid(row=3, column=0, pady=(2, 10))

    btn_submit = tk.Button(login_window, text="Secure Sign In", command=login_verify, bg="#107C41", fg="white",
                           font=("Segoe UI", 11, "bold"), width=22, bd=0, cursor="hand2")
    btn_submit.pack(pady=15)

    login_window.mainloop()