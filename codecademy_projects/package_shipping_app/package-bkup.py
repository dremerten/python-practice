sales_tax = 0.0725

PREMIUM_SHIPPING_COST = 120.00
taxed_premium_shipping = PREMIUM_SHIPPING_COST * (1 + sales_tax)


def ground_shipping_cost(weight: float) -> float:
    if weight <= 2:
        cost = weight * 1.50 + 20.00
    elif weight <= 6:
        cost = weight * 3.00 + 20.00
    elif weight <= 10:
        cost = weight * 4.00 + 20.00
    else:
        cost = weight * 4.75 + 20.00

    return cost * (1 + sales_tax)


def drone_shipping_cost(weight: float) -> float:
    if weight <= 2:
        cost = weight * 4.50
    elif weight <= 6:
        cost = weight * 9.00
    elif weight <= 10:
        cost = weight * 12.00
    else:
        cost = weight * 14.25

    return cost * (1 + sales_tax)


try:
    weight = round(
        float(input("\nPlease enter the weight of your package in lbs: ")),
        2
    )
except ValueError:
    raise ValueError("Weight must be a numeric value")

ground_result = ground_shipping_cost(weight)
drone_result = drone_shipping_cost(weight)


print(
    f"\n"
    f"=============== Shipping Cost Per Tier ===============\n"
    f"\n"
    f"Package weight: {weight:.2f} lbs\n"
    f"Prices include sales tax\n"
    f"\n"
    f"Ground Shipping:         ${ground_result:.2f}\n"
    f"Premium Ground Shipping: ${taxed_premium_shipping:.2f}\n"
    f"Drone Shipping:          ${drone_result:.2f}\n"
)

