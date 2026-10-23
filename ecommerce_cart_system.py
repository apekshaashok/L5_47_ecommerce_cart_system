"""E-commerce cart system: items, discounts, hashing and receipts."""

import hashlib
import os
import secrets

cart_items = {
    "ITEM1": {"name": "Wireless Mouse", "price": 25.0, "qty": 2},
    "ITEM2": {"name": "Mechanical Keyboard", "price": 80.0, "qty": 1},
    "ITEM3": {"name": "USB-C Hub", "price": 45.0, "qty": 3},
}

AUDIT_LOG = []


def add_item_to_cart(item_id, name, price, qty=1, audit_log=None):
    """Add a new item to the cart and log it. Return False if it exists."""
    if audit_log is None:
        audit_log = AUDIT_LOG
    if item_id in cart_items:
        return False
    cart_items[item_id] = {"name": name, "price": price, "qty": qty}
    audit_log.append(f"Added {item_id} with price {price:.2f}")
    return True


def calculate_cart_total():
    """Return the total value (price x qty) of everything in the cart."""
    return sum(d["price"] * d["qty"] for d in cart_items.values())


def remove_item_from_cart(item_id):
    """Remove an item from the cart. Return True if it was present."""
    return cart_items.pop(item_id, None) is not None


def check_cart_status(item_id):
    """Return True if the item is in the cart with a positive quantity."""
    item = cart_items.get(item_id)
    if item is None:
        return False
    return item["qty"] > 0


def calculate_discounted_total(item_id, discount_rate):
    """Return the item's price after applying a discount rate (0 to 1)."""
    if not 0 <= discount_rate <= 1:
        raise ValueError("discount_rate must be between 0 and 1")
    base_price = cart_items[item_id]["price"]
    return base_price * (1 - discount_rate)


def generate_item_hash(item_id):
    """Return a SHA-256 hex digest identifying the item."""
    return hashlib.sha256(item_id.encode()).hexdigest()


def generate_checkout_pin():
    """Return a random 4-digit checkout PIN."""
    return 1000 + secrets.randbelow(9000)


def export_cart_receipt(filename="receipt.txt"):
    """Write the cart contents to a receipt file."""
    with open(filename, "w", encoding="utf-8") as receipt:
        receipt.write(str(cart_items))
    print("Receipt saved to:", filename)


def get_cart_summary(items):
    """Return the total quantity of items with a positive quantity."""
    return sum(d["qty"] for d in items.values() if d["qty"] > 0)


def main():
    """Run a short demo of the cart system."""
    payment_gateway_key = os.environ.get("PAYMENT_GATEWAY_KEY")
    add_item_to_cart("ITEM4", "Monitor Stand", 35.0, 1)
    remove_item_from_cart("ITEM2")
    print("Is ITEM1 in cart:", check_cart_status("ITEM1"))
    discounted = calculate_discounted_total("ITEM1", 0.10)
    print("Discounted Price:", discounted)
    print("Item Hash:", generate_item_hash("ITEM1"))
    print("Checkout PIN:", generate_checkout_pin())
    export_cart_receipt()
    print("Total items:", get_cart_summary(cart_items))
    print("Gateway key configured:", payment_gateway_key is not None)


if __name__ == "__main__":
    main()
