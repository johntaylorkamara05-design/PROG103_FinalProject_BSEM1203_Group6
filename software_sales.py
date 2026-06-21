PRICE = 99
quantity = int(input("Enter the quantity purchased: "))
discount = 0
cost_price = PRICE * quantity
if quantity < 10:
    final_cost = cost_price - discount
elif quantity >= 10 and quantity <= 19:
    discount = (10 / 100) * cost_price
    final_cost = cost_price - discount
elif quantity >= 20 and quantity <= 49:
    discount = (20 / 100) * cost_price
    final_cost = cost_price - discount

elif quantity >= 50 and quantity <= 99:
    discount = (30 / 100) * cost_price
    final_cost = cost_price - discount
else:
    discount = (40 / 100) * cost_price
    final_cost = cost_price - discount

print(f"Discount Amount: le{discount}")
print(f"Final Cost: le{final_cost}")