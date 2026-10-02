from decimal import Decimal
from rest_framework.exceptions import ValidationError

def calculate_order_totals(order, tax_percentage):
    # calculate subtotal
    subtotal = Decimal("0")
    for item in order.order_items.all():
        item_total = item.unit_price * item.quantity
        subtotal += item_total

    discount_amount = Decimal("0")
    # calculate discount if there is any
    if order.promo_code:
        promo = order.promo_code

        # Check minimum order amount
        if promo.min_amount is not None and subtotal < promo.min_amount:
           raise ValidationError({
                "promo_code": [
                    f"This promo code requires a minimum order "
                    f"of ${promo.min_amount}."
                ]
            })

        if promo.discount_type == "PERCENT":
            discount_amount = (
                subtotal
                * promo.discount_value
                / Decimal("100")
            )

        elif promo.discount_type == "FIXED":
            discount_amount = promo.discount_value

        # Discount cannot be greater than subtotal
        discount_amount = min(discount_amount, subtotal)

    # calculate tax
    taxable_amount = subtotal - discount_amount
    tax_amount = taxable_amount * Decimal(tax_percentage) / Decimal("100")

    # calculate total
    total = taxable_amount + tax_amount

    return subtotal, discount_amount, tax_amount, total
