# National MSME Analytical Hub & Public Service Dashboard

An enterprise-grade Python desktop GUI application designed to streamline the administration, data tracking, and economic evaluation of Micro, Small, and Medium Enterprises (MSMEs). This system serves as a functional software prototype built to address **Sustainable Development Goal 8 (SDG 8: Decent Work and Economic Growth)** by providing public service coordinators with digital tools to monitor local marketplace health.

## 👥 Group Project Details
* **Course:** Structured Programming (PROG103)
* **Class Section:** BSEM1203 (Bachelor of Science in Software Engineering with Multimedia)
* **Group:** Group 6
* **Academic Institution Location:** Freetown, Sierra Leone

---

## 🚀 Key Features

* **Secure Administrative Gateway:** Fully gated entry window requiring credential verification (`admin` / `admin123`) before loading backend data channels.
* **Relational Database Directory:** Driven by an embedded `sqlite3` relational database managing localized business operator records (ID, Name, Gender, Operational Status, Contact Information).
* **Live Dynamic Filtering:** Event-bound reactive filtering matrix that live-updates the dataset view instantly upon typing searches or selecting dropdown variables.
* **Data Visualization Insights Canvas:** Integrated `Matplotlib` graphics engine plotting a three-axis statistical layout directly inside the dashboard (Status Bar Chart, Gender Split Pie Chart, and Onboarding Line Graph).
* **Business Profitability Calculator Engine:** A built-in P&L terminal evaluating operational transaction profiles using a numeric calculation engine (`Net Margin = Sales - Expenses`) with clear color-coded conditional output states.

---

## 🛠️ Technology Stack & Architecture

* **Language:** Python 3.13
* **GUI Framework:** Tkinter & TTK (Themed Tkinter Canvas Layouts)
* **Database Engine:** SQLite3 Relational Database
* **Data Analytics:** Matplotlib (Embedded via `FigureCanvasTkAgg`)
* **Environment Management:** Isolated Python Virtual Environment (`.venv`)

---

## 💻 Installation & Setup

### Prerequisites
Ensure you have Python 3.13 installed on your machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/johntaylorkamara05-design/PROG103_FinalProject_BSEM1203_Group6.git](https://github.com/johntaylorkamara05-design/PROG103_FinalProject_BSEM1203_Group6.git)
cd PROG103_FinalProject_BSEM1203_Group6