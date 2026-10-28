#!/usr/bin/env python3
"""
Production-Ready Vending Machine Application
=============================================
A robust, object-oriented simulation of an automated retail vending machine
featuring inventory tracking, resilient payment handling, cash-change calculation,
and formatted tax invoice generation.

Author: Senior Python Engineer
License: MIT
"""

from __future__ import annotations

import datetime
from decimal import Decimal, ROUND_HALF_UP
import sys
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# Currency helper: strictly format Decimal to two decimal places
def format_currency(amount: Decimal) -> str:
    """Format a Decimal amount to standard USD currency string ($X.XX)."""
    return f"${amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"


@dataclass
class Product:
    """Represents a product item stocked in the vending machine."""

    code: str
    name: str
    price: Decimal
    stock: int
    category: str

    def is_in_stock(self) -> bool:
        """Check if at least one unit of the product is available."""
        return self.stock > 0

    def decrement_stock(self) -> bool:
        """
        Reduce the stock by 1 upon successful purchase.
        Returns True if successful, False if out of stock.
        """
        if self.is_in_stock():
            self.stock -= 1
            return True
        return False

    def restock(self, quantity: int) -> None:
        """Increase stock quantity."""
        if quantity > 0:
            self.stock += quantity


@dataclass
class Invoice:
    """Encapsulates the financial and metadata details of a completed purchase."""

    invoice_number: str
    machine_id: str
    business_name: str
    tax_id: str
    timestamp: datetime.datetime
    item_code: str
    item_name: str
    item_category: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    tax_rate: Decimal
    tax_amount: Decimal
    total_due: Decimal
    amount_paid: Decimal
    change_returned: Decimal


class InvoiceGenerator:
    """Generates formatted, publication-grade text receipts and tax invoices."""

    RECEIPT_WIDTH: int = 54

    @classmethod
    def generate_receipt_text(cls, invoice: Invoice) -> str:
        """
        Render a structured ASCII Tax Invoice suitable for printing
        or direct terminal display.
        """
        w = cls.RECEIPT_WIDTH
        border_double = "=" * w
        border_single = "-" * w
        border_dash = "- " * (w // 2)

        timestamp_str = invoice.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        tax_pct_str = f"{(invoice.tax_rate * Decimal('100')).quantize(Decimal('0.01'))}%"

        lines: List[str] = [
            border_double,
            invoice.business_name.center(w),
            "AUTOMATED RETAIL POINT OF SALE".center(w),
            f"Machine ID: {invoice.machine_id}".center(w),
            f"VAT / Tax Reg: {invoice.tax_id}".center(w),
            border_single,
            f" INVOICE #:  {invoice.invoice_number}",
            f" DATE/TIME:  {timestamp_str}",
            f" PAYMENT:    CASH / SMART TENDER",
            border_dash,
            f"{'ITEM DESCRIPTION':<28} {'QTY':>4} {'PRICE':>9} {'TOTAL':>9}",
            border_dash,
            (
                f"[{invoice.item_code}] {invoice.item_name:<23.23} "
                f"{invoice.quantity:>4} "
                f"{format_currency(invoice.unit_price):>9} "
                f"{format_currency(invoice.subtotal):>9}"
            ),
            f"  Category: {invoice.item_category}",
            border_single,
            f"{'Subtotal (Excl. Tax):':<38} {format_currency(invoice.subtotal):>14}",
            f"{f'Sales Tax / VAT ({tax_pct_str}):':<38} {format_currency(invoice.tax_amount):>14}",
            border_single,
            f"{'TOTAL AMOUNT DUE:':<38} {format_currency(invoice.total_due):>14}",
            f"{'TOTAL AMOUNT TENDERED:':<38} {format_currency(invoice.amount_paid):>14}",
            f"{'CHANGE RETURNED:':<38} {format_currency(invoice.change_returned):>14}",
            border_double,
        ]

        # Denomination Breakdown for change if change > 0
        if invoice.change_returned > Decimal("0.00"):
            lines.append(" CHANGE BREAKDOWN:")
            breakdown = cls._calculate_denominations(invoice.change_returned)
            for denom_name, count in breakdown.items():
                lines.append(f"   • {denom_name:<18} x {count}")
            lines.append(border_single)

        lines.extend([
            "Thank you for choosing Apex Refreshments!".center(w),
            "Please retain this receipt for your records.".center(w),
            "Customer Support: support@apexvending.com".center(w),
            f"BARCODE: *{invoice.invoice_number.replace('-', '')}*".center(w),
            border_double,
        ])

        return "\n".join(lines)

    @staticmethod
    def _calculate_denominations(amount: Decimal) -> Dict[str, int]:
        """Break down monetary change into standard currency denominations."""
        denominations: List[Tuple[str, Decimal]] = [
            ("$20 Bill", Decimal("20.00")),
            ("$10 Bill", Decimal("10.00")),
            ("$5 Bill", Decimal("5.00")),
            ("$1 Bill", Decimal("1.00")),
            ("Quarter ($0.25)", Decimal("0.25")),
            ("Dime ($0.10)", Decimal("0.10")),
            ("Nickel ($0.05)", Decimal("0.05")),
            ("Penny ($0.01)", Decimal("0.01")),
        ]

        rem = amount
        result: Dict[str, int] = {}
        for name, value in denominations:
            if rem >= value:
                count = int(rem // value)
                if count > 0:
                    result[name] = count
                    rem = (rem - (value * count)).quantize(Decimal("0.01"))
        return result


class VendingMachine:
    """
    Core Domain Model: Manages inventory, pricing, tax calculations,
    and handles purchasing transactions.
    """

    def __init__(
        self,
        machine_id: str = "VM-NYC-8402",
        business_name: str = "Apex Refreshment Technologies Inc.",
        tax_id: str = "US-TAX-894-209-11",
        tax_rate: Decimal = Decimal("0.0825"),  # 8.25% Standard Sales Tax
    ) -> None:
        self.machine_id = machine_id
        self.business_name = business_name
        self.tax_id = tax_id
        self.tax_rate = tax_rate
        self.inventory: Dict[str, Product] = {}
        self.invoices_history: List[Invoice] = []
        self._initialize_catalog()

    def _initialize_catalog(self) -> None:
        """Populate initial catalog with diverse categories and stock levels."""
        catalog_data = [
            ("A1", "Glacier Spring Water", Decimal("1.50"), 8, "Drinks"),
            ("A2", "Cold Brew Espresso", Decimal("2.75"), 5, "Drinks"),
            ("B1", "Artisan Sea Salt Chips", Decimal("2.25"), 6, "Snacks"),
            ("B2", "Organic Trail Mix", Decimal("2.50"), 4, "Snacks"),
            ("C1", "Dark Chocolate Bar", Decimal("2.00"), 5, "Candy"),
            ("C2", "Sour Berry Gummies", Decimal("1.75"), 7, "Candy"),
            ("D1", "Almond Butter Croissant", Decimal("3.25"), 3, "Bakery"),
            ("D2", "Double Fudge Muffin", Decimal("3.00"), 0, "Bakery"),  # Out-of-stock edge case
        ]
        for code, name, price, stock, category in catalog_data:
            self.inventory[code] = Product(
                code=code,
                name=name,
                price=price,
                stock=stock,
                category=category,
            )

    def get_product(self, code: str) -> Optional[Product]:
        """Retrieve a product by its code (case-insensitive)."""
        return self.inventory.get(code.strip().upper())

    def get_all_products(self) -> List[Product]:
        """Return all catalog products sorted by code."""
        return sorted(self.inventory.values(), key=lambda p: p.code)

    def calculate_totals(self, unit_price: Decimal, quantity: int = 1) -> Tuple[Decimal, Decimal, Decimal]:
        """
        Given a unit price and quantity:
        Returns (subtotal, tax_amount, total_due) rounded to 2 decimal places.
        """
        subtotal = (unit_price * quantity).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        tax_amount = (subtotal * self.tax_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total_due = subtotal + tax_amount
        return subtotal, tax_amount, total_due

    def process_purchase(self, product: Product, amount_paid: Decimal) -> Invoice:
        """
        Executes the purchase transaction:
        - Decrements stock
        - Calculates change
        - Records and returns a finalized Invoice
        """
        if not product.is_in_stock():
            raise ValueError(f"Product '{product.name}' is out of stock.")

        subtotal, tax_amount, total_due = self.calculate_totals(product.price, 1)

        if amount_paid < total_due:
            shortfall = total_due - amount_paid
            raise ValueError(
                f"Insufficient funds: {format_currency(amount_paid)} paid, "
                f"but {format_currency(total_due)} is due (Short by {format_currency(shortfall)})."
            )

        # Decrement inventory stock
        if not product.decrement_stock():
            raise RuntimeError("Failed to decrement inventory stock.")

        change = (amount_paid - total_due).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        invoice_id = f"INV-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

        invoice = Invoice(
            invoice_number=invoice_id,
            machine_id=self.machine_id,
            business_name=self.business_name,
            tax_id=self.tax_id,
            timestamp=datetime.datetime.now(),
            item_code=product.code,
            item_name=product.name,
            item_category=product.category,
            quantity=1,
            unit_price=product.price,
            subtotal=subtotal,
            tax_rate=self.tax_rate,
            tax_amount=tax_amount,
            total_due=total_due,
            amount_paid=amount_paid,
            change_returned=change,
        )

        self.invoices_history.append(invoice)
        return invoice


class VendingMachineCLI:
    """User Interface & Interactive Command Loop for terminal execution."""

    def __init__(self, machine: VendingMachine) -> None:
        self.machine = machine

    def display_banner(self) -> None:
        """Display stylish terminal header."""
        print("\n" + "=" * 68)
        print("    ★ WELCOME TO APEX SMART VENDING KIOSK ★    ".center(68))
        print("          Cold Drinks • Gourmet Snacks • Sweet Confections         ".center(68))
        print(f"       Kiosk Unit: {self.machine.machine_id}  |  Tax Rate: 8.25%       ".center(68))
        print("=" * 68)

    def display_menu(self) -> None:
        """Render a clean tabular catalog of all available items."""
        print("\n" + "┌" + "─" * 66 + "┐")
        print(f"│ {'CODE':<6} {'CATEGORY':<10} {'ITEM NAME':<26} {'PRICE':>8} {'STATUS / STOCK':>11} │")
        print("├" + "─" * 66 + "┤")

        current_category = ""
        for prod in self.machine.get_all_products():
            if current_category != prod.category:
                current_category = prod.category

            stock_label = f"{prod.stock} in stock" if prod.stock > 0 else "OUT OF STOCK"
            status_display = stock_label if prod.stock > 0 else "SOLD OUT"

            print(
                f"│ {prod.code:<6} {prod.category:<10} {prod.name:<26} "
                f"{format_currency(prod.price):>8} "
                f"{status_display:>11} │"
            )

        print("└" + "─" * 66 + "┘")

    def prompt_product_selection(self) -> Optional[Product]:
        """Prompt user for a valid product code with error feedback."""
        while True:
            raw_input = input("\nEnter product code to purchase (or 'M' for main menu): ").strip().upper()

            if raw_input in ("M", "MENU", "BACK", "EXIT", "Q"):
                return None

            product = self.machine.get_product(raw_input)
            if not product:
                print(f"❌ Error: Product code '{raw_input}' not found. Please review the menu and try again.")
                continue

            if not product.is_in_stock():
                print(f"⚠️  Sorry: [{product.code}] '{product.name}' is currently OUT OF STOCK. Please choose another item.")
                continue

            return product

    def handle_payment_flow(self, product: Product) -> Optional[Decimal]:
        """
        Interactive payment handling loop:
        Supports single lump-sum payments or incremental coin/bill insertions.
        Allows cancellation with immediate refund.
        """
        subtotal, tax, total_due = self.machine.calculate_totals(product.price, 1)

        print("\n" + "-" * 50)
        print(f"Selected Item: [{product.code}] {product.name}")
        print(f"Price (Pre-Tax):     {format_currency(subtotal)}")
        print(f"Sales Tax (8.25%):   {format_currency(tax)}")
        print(f"Total Amount Due:    {format_currency(total_due)}")
        print("-" * 50)
        print("Payment Options:")
        print(" • Enter a lump-sum amount (e.g. 5.00)")
        print(" • Or insert bills/coins gradually (e.g. 1.00, 0.25)")
        print(" • Enter 'C' or 'CANCEL' to cancel transaction and retrieve money.")
        print("-" * 50)

        accumulated = Decimal("0.00")

        while accumulated < total_due:
            needed = total_due - accumulated
            prompt_msg = (
                f"Inserted: {format_currency(accumulated)} | Remaining Due: {format_currency(needed)}\n"
                f"Insert money ($) or 'C' to cancel: "
            )
            raw_val = input(prompt_msg).strip()

            if raw_val.upper() in ("C", "CANCEL"):
                if accumulated > Decimal("0.00"):
                    print(f"\n🔄 Transaction cancelled. Returning tendered funds: {format_currency(accumulated)}")
                else:
                    print("\n🔄 Transaction cancelled.")
                return None

            # Clean currency symbols if user typed '$'
            cleaned = raw_val.replace("$", "").replace(",", "")
            try:
                inserted = Decimal(cleaned)
                if inserted <= Decimal("0.00"):
                    print("❌ Please insert a positive monetary value.")
                    continue
                # Round to cents
                inserted = inserted.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                accumulated += inserted
                print(f"✔ Accepted: {format_currency(inserted)}")
            except Exception:
                print(f"❌ Invalid money format '{raw_val}'. Please enter a valid dollar amount (e.g., 1.00, 2.50).")

        return accumulated

    def execute_purchase_cycle(self) -> None:
        """Run a single complete purchase cycle."""
        self.display_menu()
        product = self.prompt_product_selection()
        if not product:
            return

        tendered = self.handle_payment_flow(product)
        if tendered is None:
            return

        try:
            invoice = self.machine.process_purchase(product, tendered)
            print("\n🎉 Purchase successful! Dispensing item...")
            print(f"🎁 Dispatched: 1x [{invoice.item_code}] {invoice.item_name}!")
            print("\n" + "🧾 GENERATING OFFICIAL TAX INVOICE...".center(54))
            receipt = InvoiceGenerator.generate_receipt_text(invoice)
            print(receipt)
        except Exception as err:
            print(f"\n❌ Transaction error: {err}")

    def run(self) -> None:
        """Main application lifecycle loop."""
        self.display_banner()

        while True:
            print("\n" + "─" * 40)
            print("MAIN CONTROLS:")
            print(" [1] Browse Catalog & Purchase Item")
            print(" [2] View Restock / Inventory Status")
            print(" [3] View Transaction Receipt History")
            print(" [4] Exit Machine")
            print("─" * 40)

            choice = input("Please select an option (1-4): ").strip()

            if choice == "1":
                self.execute_purchase_cycle()
            elif choice == "2":
                self.display_inventory_status()
            elif choice == "3":
                self.display_invoice_history()
            elif choice in ("4", "Q", "QUIT", "EXIT"):
                print("\nThank you for using Apex Smart Vending. Have a wonderful day! Goodbye.\n")
                break
            else:
                print("❌ Invalid selection. Please enter 1, 2, 3, or 4.")

    def display_inventory_status(self) -> None:
        """Administrative inspection view of stock counts."""
        print("\n=== SYSTEM INVENTORY AUDIT ===")
        total_units = 0
        for p in self.machine.get_all_products():
            total_units += p.stock
            print(f"• [{p.code}] {p.name:<25} Stock: {p.stock:>2} units | Price: {format_currency(p.price)}")
        print(f"Total units across machine: {total_units}")

    def display_invoice_history(self) -> None:
        """View summary of all processed invoices in the session."""
        print("\n=== SESSION TRANSACTION AUDIT LOG ===")
        if not self.machine.invoices_history:
            print("No purchases have been finalized yet during this session.")
            return

        for inv in self.machine.invoices_history:
            print(
                f"• {inv.invoice_number} | {inv.timestamp.strftime('%H:%M:%S')} | "
                f"[{inv.item_code}] {inv.item_name} | Paid: {format_currency(inv.amount_paid)} | "
                f"Change: {format_currency(inv.change_returned)}"
            )


# Unit Tests for automated verification
def run_self_tests() -> None:
    """Validate core calculations, edge cases, and business logic."""
    vm = VendingMachine()
    
    # Test 1: Code retrieval
    water = vm.get_product("A1")
    assert water is not None, "Product A1 should exist"
    assert water.name == "Glacier Spring Water"
    
    # Test 2: Case insensitivity
    assert vm.get_product("a1") == water, "Product lookup must be case-insensitive"

    # Test 3: Tax calculation accuracy
    subtotal, tax, total = vm.calculate_totals(Decimal("2.00"), 1)
    # 2.00 * 0.0825 = 0.165 -> rounds to 0.17
    assert subtotal == Decimal("2.00")
    assert tax == Decimal("0.17")
    assert total == Decimal("2.17")

    # Test 4: Out of stock detection
    muffin = vm.get_product("D2")
    assert muffin is not None and not muffin.is_in_stock()
    try:
        vm.process_purchase(muffin, Decimal("10.00"))
        raise AssertionError("Should have raised error for out of stock item")
    except ValueError:
        pass  # expected

    # Test 5: Successful purchase & change calculation
    initial_stock = water.stock
    invoice = vm.process_purchase(water, Decimal("5.00"))
    assert water.stock == initial_stock - 1, "Stock must decrement"
    assert invoice.total_due == Decimal("1.62")  # 1.50 + 0.12 tax
    assert invoice.change_returned == Decimal("3.38")  # 5.00 - 1.62

    # Test 6: Receipt string generation contains essential fields
    receipt = InvoiceGenerator.generate_receipt_text(invoice)
    assert invoice.invoice_number in receipt
    assert "Apex Refreshment Technologies Inc." in receipt
    assert "CHANGE BREAKDOWN" in receipt

    print("✔ All self-tests passed successfully.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_tests()
    else:
        app = VendingMachineCLI(VendingMachine())
        try:
            app.run()
        except KeyboardInterrupt:
            print("\n\nSession terminated by user. Goodbye!")
