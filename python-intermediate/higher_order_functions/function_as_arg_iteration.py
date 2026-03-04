# bills = [115, 120, 42]

bills = [i for i in range(10)]

def total_bills(func, bills, label):
    new_bills = []

    for bill in bills:
        total = func(bill)
        new_bills.append(
            f"Bill number {bill} - Total amount owed with {label} is ${total:.2f}."
        )

    return new_bills

def add_tax(total):
    return total + (total * 0.09)

def add_tip(total):
    return total + (total * 0.20)


bills_w_tax = total_bills(add_tax, bills, "9% tax")
bills_w_tip = total_bills(add_tip, bills, "20% tip")

print(bills_w_tax)
print(bills_w_tip)