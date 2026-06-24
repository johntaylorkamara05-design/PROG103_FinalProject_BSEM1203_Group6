# PROG103: Principles of Structured Programming
# Assignment 1: Small Business Sales Calculator
# Student Name: [John .W. Taylor-Kamara]
# Student ID: [905005639]

# CONSTANTS (Required for Assignment)
GST_RATE = 0.15  # 15% Sales Tax for Sierra Leone


# FUNCTION 1: Logic Processing (Calculates item total)
def calculate_item_total(price, quantity):
    """Calculates the subtotal for a single line item."""
    return price * quantity


# FUNCTION 2: Formatted Output (Displays the receipt)
def display_receipt(sales_items, grand_total):
    """Prints a clear, formatted terminal-based receipt."""
    print("\n" + "=" * 40)
    print("      SMALL BUSINESS SALES RECEIPT")
    print("=" * 40)
    print(f"{'Item':<15} {'Qty':<5} {'Price':<10} {'Total':<10}")
    print("-" * 40)

    for item in sales_items:
        print(f"{item['name']:<15} {item['qty']:<5} {item['price']:<10.2f} {item['sub']:<10.2f}")

    tax = grand_total * GST_RATE
    final_amount = grand_total + tax

    print("-" * 40)
    print(f"{'Subtotal:':<30} {grand_total:>8.2f}")
    print(f"{'GST (15%):':<30} {tax:>8.2f}")
    print(f"{'GRAND TOTAL:':<30} {final_amount:>8.2f}")
    print("=" * 40)
    print("   Thank you for supporting local business!")
    print("=" * 40)


def main():
    # Variables and Data Types
    all_sales = []
    running_total = 0.0

    print("--- Welcome to the Small Business Sales Calculator ---")

    # ITERATION: Loop to process multiple records
    while True:
        try:
            name = input("\nEnter item name (or type 'done' to finish): ").strip()
            if name.lower() == 'done':
                break

            # Input and Data Type Conversion
            price = float(input(f"Enter price for {name}: "))
            qty = int(input(f"Enter quantity for {name}: "))

            # Using the modular function
            item_subtotal = calculate_item_total(price, qty)
            running_total += item_subtotal

            # Storing record in a dictionary
            all_sales.append({
                'name': name,
                'price': price,
                'qty': qty,
                'sub': item_subtotal
            })

            print(f"Added {name} to sale.")

        except ValueError:
            print("Invalid input! Please enter numbers for price and quantity.")

    # DECISION: Check if any sales were made before printing
    if len(all_sales) > 0:
        display_receipt(all_sales, running_total)
    else:
        print("No sales recorded. System exiting.")


# Start the program
if __name__ == "__main__":
    main()