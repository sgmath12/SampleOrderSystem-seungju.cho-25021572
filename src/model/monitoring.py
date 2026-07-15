def count_orders_by_status(orders):
    counts = {}
    for order in orders:
        if order.status == "REJECTED":
            continue
        counts[order.status] = counts.get(order.status, 0) + 1
    return counts


def reserved_quantity_for_sample(orders, sample_id):
    return sum(
        order.quantity
        for order in orders
        if order.sample_id == sample_id and order.status == "RESERVED"
    )


def inventory_status(inventory: int, reserved_quantity: int) -> str:
    if inventory == 0:
        return "고갈"
    if inventory < reserved_quantity:
        return "부족"
    return "여유"
