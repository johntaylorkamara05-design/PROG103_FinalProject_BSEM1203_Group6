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

    # Create the primary analytical table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS msme_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            status TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    """)

    # Check if data exists; if empty, pre-populate 20 academic rows
    cursor.execute("SELECT COUNT(*) FROM msme_records")
    if cursor.fetchone()[0] == 0:
        sample_data = [
            ("Alhaji Kamara", "Male", "Active", "+232-76-112233"),
            ("Fatmata Bangura", "Female", "Active", "+232-33-445566"),
            ("Mohamed Sesay", "Male", "Pending", "+232-77-889900"),
            ("Isatu Conteh", "Female", "Inactive", "+232-88-224466"),
            ("Zainab Turay", "Female", "Active", "+232-30-555777"),
            ("Sorie Fofanah", "Male", "Active", "+232-76-998877"),
            ("Mariama Koroma", "Female", "Pending", "+232-77-111222"),
            ("Osman Mansaray", "Male", "Inactive", "+232-33-333444"),
            ("Kadiatu Jalloh", "Female", "Active", "+232-88-555666"),
            ("Ibrahim Kargbo", "Male", "Active", "+232-76-444555"),
            ("Aminata Tarawally", "Female", "Active", "+232-30-123456"),
            ("Samuel Conteh", "Male", "Pending", "+232-77-654321"),
            ("Ramatu Barrie", "Female", "Inactive", "+232-33-987654"),
            ("Abdulai Cole", "Male", "Active", "+232-88-789123"),
            ("Fatu Kanu", "Female", "Active", "+232-76-321987"),
            ("Mustapha Kamara", "Male", "Active", "+232-77-456789"),
            ("Mabinty Sesay", "Female", "Pending", "+232-30-789456"),
            ("Emmanuel King", "Male", "Inactive", "+232-33-159263"),
            ("Sia Dumbuya", "Female", "Active", "+232-88-357159"),
            ("Abu Bakarr", "Male", "Active", "+232-76-258369")
        ]
        cursor.executemany("INSERT INTO msme_records (name, gender, status, contact) VALUES (?, ?, ?, ?)", sample_data)
        conn.commit()
    conn.close()


# ==========================================
# 2. APPLICATION LOGIN CONTROLLER (GATEWAY)
# ==========================================
def login_verify():
    username = entry_user.get()
    password = entry_pass.get()

    # Structured credentials evaluation
    if username == "admin" and password == "admin123":
        login_window.destroy()  # Dismantle authentication layout
        launch_dashboard()  # Initialize main application
    else:
        messagebox.showerror("Access Denied", "Invalid Administrative Credentials.")


# ==========================================
# 3. CORE FINANCIAL CALCULATOR (LOGIC)
# ==========================================
def process_financial_performance():
    try:
        # Fetch data strings and convert to float elements
        sales = float(entry_sales.get())
        expenses = float(entry_expenses.get())

        # Mathematical algorithm execution
        net_margin = sales - expenses

        # Structural conditional logic mapping to business performance
        if net_margin > 0:
            result_text = f"Profit Attained: +Le {net_margin:,.2f}"
            lbl_financial_result.config(text=result_text, fg="#196F3D")  # Emerald Green for Profit
        elif net_margin < 0:
            result_text = f"Loss Recorded: -Le {abs(net_margin):,.2f}"
            lbl_financial_result.config(text=result_text, fg="#943126")  # Deep Red for Loss
        else:
            result_text = "Operational Balance: Break-even (Le 0.00)"
            lbl_financial_result.config(text=result_text, fg="#2E4053")  # Slate Grey

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values for Sales and Expenses.")


# ==========================================
# 4. RE-QUERY DATABASE WITH FILTERS
# ==========================================
def refresh_table_view():
    # Clear existing rows in Treeview
    for item in tree.get_children():
        tree.delete(item)

    gender_filter = combo_gender.get()
    status_filter = combo_status.get()

    conn = sqlite3.connect("msme_sales.db")
    cursor = conn.cursor()

    # Dynamic SQL String Construction
    query = "SELECT * FROM msme_records WHERE 1=1"
    params = []

    if gender_filter != "All Genders":
        query += " AND gender = ?"
        params.append(gender_filter)
    if status_filter != "All Statuses":
        query += " AND status = ?"
        params.append(status_filter)

    cursor.execute(query, params)
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()


# ==========================================
# 5. MATPLOTLIB CANVAS GENERATION
# ==========================================
def render_charts(parent_frame):
    # Fetch statistical aggregations from SQLite
    conn = sqlite3.connect("msme_sales.db")
    cursor = conn.cursor()

    cursor.execute("SELECT status, COUNT(*) FROM msme_records GROUP BY status")
    status_data = dict(cursor.fetchall())

    cursor.execute("SELECT gender, COUNT(*) FROM msme_records GROUP BY gender")
    gender_data = dict(cursor.fetchall())
    conn.close()

    # Initialize Matplotlib Subplot Architecture
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 2.8), dpi=100)
    fig.tight_layout(pad=3.0)

    # Draw Bar Chart (Status Analysis)
    statuses = list(status_data.keys())
    status_counts = list(status_data.values())
    ax1.bar(statuses, status_counts, color=["#1F4E79", "#F39C12", "#7F8C8D"])
    ax1.set_title("Operator Status Metrics", fontsize=9, fontweight='bold', fontname='Tahoma')
    ax1.tick_params(labelsize=8)

    # Draw Pie Chart (Gender Segment Distribution)
    genders = list(gender_data.keys())
    gender_counts = list(gender_data.values())
    ax2.pie(gender_counts, labels=genders, autopct='%1.1f%%', startangle=90, colors=["#E74C3C", "#2980B9"],
            textprops={'fontsize': 8, 'fontname': 'Tahoma'})
    ax2.set_title("Gender Breakdown", fontsize=9, fontweight='bold', fontname='Tahoma')

    # Mount Canvas inside Tkinter Widget Node Hierarchy
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# ==========================================
# 6. MAIN APPLICATION WORKSPACE LAYOUT
# ==========================================
def launch_dashboard():
    global tree, combo_gender, combo_status, entry_sales, entry_expenses, lbl_financial_result

    main_window = tk.Tk()
    main_window.title("MSME Public Service Management & Analytical Hub")
    main_window.geometry("780 edged canvas fixed size setup")
    main_window.geometry("820x600")

    # Root layout notebook container
    notebook = ttk.Notebook(main_window)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Tab 1: Directory Setup
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text=" Operator Record Directory ")

    # Filter Pane Widget Node
    frame_filters = ttk.LabelFrame(tab1, text=" Dynamic Database Filter Engine ")
    frame_filters.pack(fill=tk.X, padx=10, pady=10, ipady=5)

    combo_gender = ttk.Combobox(frame_filters, values=["All Genders", "Male", "Female"], state="readonly")
    combo_gender.set("All Genders")
    combo_gender.pack(side=tk.LEFT, padx=10, pady=5)

    combo_status = ttk.Combobox(frame_filters, values=["All Statuses", "Active", "Pending", "Inactive"],
                                state="readonly")
    combo_status.set("All Statuses")
    combo_status.pack(side=tk.LEFT, padx=10, pady=5)

    btn_filter = tk.Button(frame_filters, text="Apply Query Filter", command=refresh_table_view, bg="#1F4E79",
                           fg="white", font=("Tahoma", 9, "bold"))
    btn_filter.pack(side=tk.LEFT, padx=10, pady=5)

    # Table Grid Presentation
    tree = ttk.Treeview(tab1, columns=("ID", "Name", "Gender", "Status", "Contact"), show="headings")
    tree.heading("ID", text="Record ID")
    tree.heading("Name", text="Full Name")
    tree.heading("Gender", text="Gender Alignment")
    tree.heading("Status", text="Activity Status")
    tree.heading("Contact", text="Contact Node Connection")

    tree.column("ID", width=70, anchor=tk.CENTER)
    tree.column("Name", width=180, anchor=tk.W)
    tree.column("Gender", width=120, anchor=tk.CENTER)
    tree.column("Status", width=100, anchor=tk.CENTER)
    tree.column("Contact", width=150, anchor=tk.W)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Tab 2: Visualizations Analytics
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text=" Matplotlib Analytics Insights ")

    frame_charts = ttk.Frame(tab2)
    frame_charts.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Tab 3: NEW COMPLIANT FINANCIAL REVENUE CALCULATOR MODULE
    tab3 = ttk.Frame(notebook)
    notebook.add(tab3, text=" Business Revenue Analytics (P&L) ")

    frame_calc = ttk.LabelFrame(tab3, text=" Perform Financial Performance Audit ")
    frame_calc.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    lbl_instructions = tk.Label(frame_calc,
                                text="Input monthly operation margins below to analyze macro profit trends:",
                                font=("Tahoma", 10, "italic"), fg="#555555")
    lbl_instructions.pack(pady=15)

    # Form Layout Setup
    frame_form = tk.Frame(frame_calc)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Total Monthly Sales (Revenue): Le ", font=("Tahoma", 10, "bold")).grid(row=0, column=0,
                                                                                                      sticky=tk.E,
                                                                                                      pady=10)
    entry_sales = tk.Entry(frame_form, font=("Tahoma", 10), width=20)
    entry_sales.grid(row=0, column=1, pady=10)

    tk.Label(frame_form, text="Total Monthly Expenses: Le ", font=("Tahoma", 10, "bold")).grid(row=1, column=0,
                                                                                               sticky=tk.E, pady=10)
    entry_expenses = tk.Entry(frame_form, font=("Tahoma", 10), width=20)
    entry_expenses.grid(row=1, column=1, pady=10)

    btn_compute = tk.Button(frame_calc, text="Calculate Business Standing", command=process_financial_performance,
                            bg="#1F4E79", fg="white", font=("Tahoma", 10, "bold"), padx=10, pady=5)
    btn_compute.pack(pady=20)

    lbl_financial_result = tk.Label(frame_calc, text="Awaiting Data Entries...", font=("Tahoma", 14, "bold"),
                                    fg="#555555")
    lbl_financial_result.pack(pady=15)

    # Initial data runs and interface draws
    refresh_table_view()
    render_charts(frame_charts)

    main_window.mainloop()


# ==========================================
# 7. MAIN START ENTRY POINT
# ==========================================
if __name__ == "__main__":
    init_database()

    # Launch Gateway Login Dialog Portal Framework
    login_window = tk.Tk()
    login_window.title("System Gateway Authorization")
    login_window.geometry("340x220")
    login_window.resizable(False, False)

    tk.Label(login_window, text="Administrative Access Portal", font=("Tahoma", 12, "bold"), fg="#1F4E79").pack(pady=15)

    frame_fields = tk.Frame(login_window)
    frame_fields.pack(pady=5)

    tk.Label(frame_fields, text="Username:", font=("Tahoma", 9, "bold")).grid(row=0, column=0, sticky=tk.E, pady=5,
                                                                              padx=5)
    entry_user = tk.Entry(frame_fields, font=("Tahoma", 9))
    entry_user.grid(row=0, column=1, pady=5)

    tk.Label(frame_fields, text="Password:", font=("Tahoma", 9, "bold")).grid(row=1, column=0, sticky=tk.E, pady=5,
                                                                              padx=5)
    entry_pass = tk.Entry(frame_fields, font=("Tahoma", 9), show="*")
    entry_pass.grid(row=1, column=1, pady=5)

    btn_login = tk.Button(login_window, text="Authorize Security Clear", command=login_verify, bg="#1F4E79", fg="white",
                          font=("Tahoma", 9, "bold"), padx=10, pady=3)
    btn_login.pack(pady=15)

    login_window.mainloop()