from tkinter import *
from tkinter import messagebox

sales = []
expenses = []

# Function 1
def add_sale():
    if amount_entry.get() == "":
        messagebox.showerror("Error", "Enter amount")
        return

    amount = float(amount_entry.get())
    sales.append(amount)

    output.insert(END, f"Sale Added: Le {amount}\n")

    amount_entry.delete(0, END)

# Function 2
def add_expense():
    if amount_entry.get() == "":
        messagebox.showerror("Error", "Enter amount")
        return

    amount = float(amount_entry.get())
    expenses.append(amount)

    output.insert(END, f"Expense Added: Le {amount}\n")

    amount_entry.delete(0, END)

# Function 3
def view_records():

    output.insert(END, "\nSALES RECORDS\n")

    for sale in sales:
        output.insert(END, f"Le {sale}\n")

    output.insert(END, "\nEXPENSE RECORDS\n")

    for expense in expenses:
        output.insert(END, f"Le {expense}\n")

# Function 4
def calculate_profit():

    total_sales = 0
    total_expenses = 0

    for sale in sales:
        total_sales += sale

    for expense in expenses:
        total_expenses += expense

    profit = total_sales - total_expenses

    output.insert(END, "\n----- REPORT -----\n")
    output.insert(END, f"Total Sales = Le {total_sales}\n")
    output.insert(END, f"Total Expenses = Le {total_expenses}\n")

    if profit > 0:
        output.insert(END, f"Profit = Le {profit}\n")

    elif profit < 0:
        output.insert(END, f"Loss = Le {abs(profit)}\n")

    else:
        output.insert(END, "No Profit No Loss\n")

# Function 5
def clear_data():

    sales.clear()
    expenses.clear()

    output.delete(1.0, END)

# GUI Window

root = Tk()
root.title("Sales and Expense Tracker")
root.geometry("600x500")

title = Label(root,
              text="Sales and Expense Tracker",
              font=("Arial",16,"bold"))
title.pack(pady=10)

Label(root,text="Enter Amount").pack()

amount_entry = Entry(root,width=30)
amount_entry.pack()

Button(root,
       text="Add Sale",
       width=20,
       command=add_sale).pack(pady=5)

Button(root,
       text="Add Expense",
       width=20,
       command=add_expense).pack(pady=5)

Button(root,
       text="View Records",
       width=20,
       command=view_records).pack(pady=5)

Button(root,
       text="Calculate Profit",
       width=20,
       command=calculate_profit).pack(pady=5)

Button(root,
       text="Clear",
       width=20,
       command=clear_data).pack(pady=5)

Button(root,
       text="Exit",
       width=20,
       command=root.destroy).pack(pady=5)

output = Text(root,
              width=60,
              height=12)

output.pack(pady=10)

root.mainloop()